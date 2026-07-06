from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from queuing.models import QueueService
from .models import Token, Booking, Notification, Reward
from .forms import BookTokenForm

@login_required(login_url='login')
def book_token(request, queue_id):
    """Book a token (slot) in a queue."""
    queue = get_object_or_404(QueueService, id=queue_id, is_active=True)
    
    if request.method == 'POST':
        # Check if user already has an active booking in this queue
        existing_token = Token.objects.filter(
            queue=queue,
            user=request.user,
            status__in=['waiting', 'ready', 'serving']
        ).first()
        
        if existing_token:
            messages.warning(request, f'You already have an active token #{existing_token.token_number} in this queue!')
            return redirect('token_detail', token_id=existing_token.id)
        
        # Priority booking logic
        user_priority = request.user.profile.get_priority_score()
        
        # Get all waiting tokens
        waiting_tokens = Token.objects.filter(queue=queue, status__in=['waiting', 'ready']).order_by('token_number')
        
        # Find the best position for priority user
        if user_priority >= 50 and waiting_tokens.exists():  # High priority threshold
            # Insert before the last 3 tokens if possible
            insert_position = max(1, waiting_tokens.count() - 2)
            tokens_to_shift = waiting_tokens[insert_position-1:]
            
            # Shift token numbers
            for token in tokens_to_shift:
                token.token_number += 1
                token.save()
            
            token_number = insert_position
        else:
            # Normal booking - get next token number
            last_token = Token.objects.filter(queue=queue).order_by('-token_number').first()
            token_number = (last_token.token_number + 1) if last_token else 1
        
        # Create new token
        token = Token.objects.create(
            queue=queue,
            user=request.user,
            token_number=token_number,
            status='waiting'
        )
        
        # Create booking record
        booking = Booking.objects.create(
            user=request.user,
            queue=queue,
            token=token
        )
        
        # Send notification (when 3 or fewer people ahead)
        send_notification_if_needed(token)
        
        messages.success(request, f'Token booked successfully! Your token number is {token_number}.')
        return redirect('token_detail', token_id=token.id)
    
    return render(request, 'booking/book_token.html', {'queue': queue})

@login_required(login_url='login')
def token_detail(request, token_id):
    """View details of a booked token, including QR code."""
    token = get_object_or_404(Token, id=token_id, user=request.user)
    position = token.get_position_in_queue()
    tokens_ahead = token.get_tokens_ahead()
    
    context = {
        'token': token,
        'position': position,
        'tokens_ahead': tokens_ahead,
        'estimated_wait_time': tokens_ahead * token.queue.estimated_service_time,
        'queue': token.queue,
    }
    
    return render(request, 'booking/token_detail.html', context)

@login_required(login_url='login')
def token_list(request):
    """List all tokens for the current user."""
    tokens = Token.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'tokens': tokens,
    }
    
    return render(request, 'booking/token_list.html', context)

@login_required(login_url='login')
def cancel_token(request, token_id):
    """Cancel a booked token."""
    token = get_object_or_404(Token, id=token_id, user=request.user)
    
    if token.status not in ['waiting', 'ready']:
        messages.error(request, 'Token cannot be cancelled in current status!')
        return redirect('token_detail', token_id=token_id)
    
    token.status = 'cancelled'
    token.save()
    
    messages.success(request, f'Token #{token.token_number} has been cancelled.')
    return redirect('token_list')

@login_required(login_url='login')
def token_api_position(request, token_id):
    """API endpoint to get real-time token position (JSON)."""
    token = get_object_or_404(Token, id=token_id)
    
    data = {
        'token_id': token.id,
        'token_number': token.token_number,
        'status': token.status,
        'position': token.get_position_in_queue(),
        'tokens_ahead': token.get_tokens_ahead(),
        'estimated_wait_minutes': token.get_tokens_ahead() * token.queue.estimated_service_time,
        'queue_name': token.queue.service_name,
    }
    
    return JsonResponse(data)

def send_notification_if_needed(token):
    """Send notification when 3 or fewer people are ahead."""
    tokens_ahead = token.get_tokens_ahead()
    
    if tokens_ahead <= 3 and not token.notification_sent:
        try:
            user = token.user
            queue = token.queue
            message = f"Great news! You're next up in {queue.service_name}. Your token #{token.token_number} is about to be served. Only {tokens_ahead} people ahead of you."
            
            # Send email notification
            try:
                send_mail(
                    subject=f'Queue Notification - {queue.service_name}',
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except:
                pass
            
            # Create notification record
            Notification.objects.create(
                token=token,
                notification_type='email',
                message=message,
                is_sent=True
            )
            
            token.notification_sent = True
            token.save()
            
        except Exception as e:
            print(f"Error sending notification: {e}")

def check_and_send_notifications():
    """Background task to check and send notifications when users get closer to their turn."""
    # This could be run periodically by Celery or a cron job
    tokens = Token.objects.filter(
        status__in=['waiting', 'ready'],
        notification_sent=False
    )
    
    for token in tokens:
        send_notification_if_needed(token)


def award_reward_points(token, points=10):
    """Award reward points to user when token is completed."""
    try:
        user = token.user
        
        # Create reward record
        reward = Reward.objects.create(
            user=user,
            token=token,
            points_earned=points,
            reason='completion',
            description=f'Completed service at {token.queue.service_name}'
        )
        
        # Update user profile points
        user.profile.add_reward_points(points)
        
        return reward
    except Exception as e:
        print(f"Error awarding reward points: {e}")
        return None


@login_required(login_url='login')
def reward_dashboard(request):
    """Display user's reward points and history."""
    user_profile = request.user.profile
    rewards = Reward.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate statistics
    total_points = user_profile.reward_points
    total_completed = user_profile.completed_bookings
    total_rewards = rewards.count()
    avg_points_per_booking = total_points / total_completed if total_completed > 0 else 0
    
    context = {
        'user_profile': user_profile,
        'rewards': rewards,
        'total_points': total_points,
        'total_completed': total_completed,
        'total_rewards': total_rewards,
        'avg_points_per_booking': avg_points_per_booking,
        'priority_score': user_profile.get_priority_score(),
    }
    
    return render(request, 'booking/reward_dashboard.html', context)


def reward_graph(request):
    """Display the reward dataset visualization graph."""
    return render(request, 'booking/reward_graph.html')


@login_required(login_url='login')
def reward_list(request):
    """Display all rewards for the user."""
    rewards = Reward.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'rewards': rewards,
    }
    
    return render(request, 'booking/reward_list.html', context)

@login_required(login_url='login')
def verify_qr_completion(request):
    """User scans QR code to confirm service completion."""
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        if qr_data:
            try:
                # Parse QR data: "unique_id|token_number|queue_id"
                parts = qr_data.split('|')
                if len(parts) == 3:
                    unique_id, token_number, queue_id = parts
                    
                    token = Token.objects.get(
                        unique_id=unique_id,
                        token_number=token_number,
                        queue_id=queue_id,
                        user=request.user,
                        status='serving'  # Only serving tokens can be completed
                    )
                    
                    # Mark as completed and shift queue
                    completed_token_number = token.token_number
                    token.status = 'completed'
                    token.save()
                    
                    # Award reward points
                    reward = award_reward_points(token)
                    
                    # Shift all tokens with higher numbers down by 1
                    tokens_to_shift = Token.objects.filter(
                        queue=token.queue, 
                        token_number__gt=completed_token_number
                    ).order_by('token_number')
                    
                    for shift_token in tokens_to_shift:
                        shift_token.token_number -= 1
                        shift_token.save()
                    
                    messages.success(request, f'Service completed! You earned {reward.points_earned if reward else 0} reward points.')
                    return redirect('token_list')
                else:
                    messages.error(request, 'Invalid QR code format.')
            except Token.DoesNotExist:
                messages.error(request, 'Token not found or not authorized.')
            except Exception as e:
                messages.error(request, f'Error processing QR code: {str(e)}')
    
    return render(request, 'booking/verify_qr.html')
