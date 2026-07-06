from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import QueueService
from .forms import QueueServiceForm
from booking.models import Token, Booking
from users.models import UserProfile

@login_required(login_url='login')
def queue_list(request):
    """List all queue services."""
    queues = QueueService.objects.filter(is_active=True)
    
    context = {
        'queues': queues,
    }
    
    return render(request, 'queue/queue_list.html', context)

@login_required(login_url='login')
def queue_detail(request, queue_id):
    """View details of a specific queue and its current status."""
    queue = get_object_or_404(QueueService, id=queue_id)
    tokens = Token.objects.filter(queue=queue, status__in=['waiting', 'ready']).order_by('token_number')
    
    # Get currently being served token
    currently_served = Token.objects.filter(queue=queue, status='serving').first()
    
    # Calculate waiting time
    waiting_tokens_count = tokens.count()
    estimated_wait_time = waiting_tokens_count * queue.estimated_service_time
    
    context = {
        'queue': queue,
        'tokens': tokens,
        'currently_served': currently_served,
        'waiting_count': waiting_tokens_count,
        'estimated_wait_time': estimated_wait_time,
    }
    
    return render(request, 'queue/queue_detail.html', context)

@login_required(login_url='login')
def queue_api_status(request, queue_id):
    """API endpoint to get real-time queue status (JSON)."""
    queue = get_object_or_404(QueueService, id=queue_id)
    tokens = Token.objects.filter(queue=queue, status__in=['waiting', 'ready']).order_by('token_number')
    currently_served = Token.objects.filter(queue=queue, status='serving').first()
    
    data = {
        'queue_id': queue.id,
        'queue_name': queue.service_name,
        'waiting_count': tokens.count(),
        'estimated_service_time': queue.estimated_service_time,
        'total_wait_minutes': tokens.count() * queue.estimated_service_time,
        'currently_served_token': currently_served.token_number if currently_served else None,
    }
    
    return JsonResponse(data)

# Admin views
@login_required(login_url='login')
def admin_queue_list(request):
    """Admin: List all queue services managed by the admin."""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin_user:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    queues = QueueService.objects.filter(admin=request.user)
    
    context = {
        'queues': queues,
    }
    
    return render(request, 'queue/admin_queue_list.html', context)

@login_required(login_url='login')
def admin_queue_create(request):
    """Admin: Create a new queue service."""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin_user:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        form = QueueServiceForm(request.POST)
        if form.is_valid():
            queue = form.save(commit=False)
            queue.admin = request.user
            queue.save()
            messages.success(request, 'Queue service created successfully!')
            return redirect('admin_queue_list')
    else:
        form = QueueServiceForm()
    
    return render(request, 'queue/admin_queue_form.html', {'form': form, 'action': 'Create'})

@login_required(login_url='login')
def admin_queue_update(request, queue_id):
    """Admin: Update a queue service."""
    queue = get_object_or_404(QueueService, id=queue_id, admin=request.user)
    
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin_user:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        form = QueueServiceForm(request.POST, instance=queue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Queue service updated successfully!')
            return redirect('admin_queue_list')
    else:
        form = QueueServiceForm(instance=queue)
    
    return render(request, 'queue/admin_queue_form.html', {'form': form, 'action': 'Update', 'queue': queue})

@login_required(login_url='login')
def admin_queue_detail(request, queue_id):
    """Admin: View detailed queue status with all tokens."""
    queue = get_object_or_404(QueueService, id=queue_id, admin=request.user)
    
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin_user:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    tokens = Token.objects.filter(queue=queue).order_by('-token_number')
    
    context = {
        'queue': queue,
        'tokens': tokens,
    }
    
    return render(request, 'queue/admin_queue_detail.html', context)

@login_required(login_url='login')
def admin_serve_next(request, queue_id):
    """Admin: Move queue forward - mark current token as completed and next as serving."""
    queue = get_object_or_404(QueueService, id=queue_id, admin=request.user)
    
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin_user:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    # Mark currently serving token as completed and award points
    current = Token.objects.filter(queue=queue, status='serving').first()
    if current:
        completed_token_number = current.token_number
        current.status = 'completed'
        current.save()
        
        # Award reward points
        from booking.views import award_reward_points
        reward = award_reward_points(current)
        if reward:
            messages.info(request, f'Awarded {reward.points_earned} points to {current.user.username}')
        
        # Shift all tokens with higher numbers down by 1
        tokens_to_shift = Token.objects.filter(
            queue=queue, 
            token_number__gt=completed_token_number
        ).order_by('token_number')
        
        for token in tokens_to_shift:
            token.token_number -= 1
            token.save()
    
    # Get next waiting token and mark as serving
    next_token = Token.objects.filter(queue=queue, status='waiting').order_by('token_number').first()
    if next_token:
        next_token.status = 'serving'
        next_token.save()
        messages.success(request, f'Now serving Token #{next_token.token_number}')
    else:
        messages.info(request, 'No more tokens waiting.')
    
    return redirect('admin_queue_detail', queue_id=queue_id)

@login_required(login_url='login')
def admin_verify_qr(request, queue_id):
    """Admin: Verify QR code and mark token as ready."""
    queue = get_object_or_404(QueueService, id=queue_id, admin=request.user)
    
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin_user:
        messages.error(request, 'Access denied! Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        token_number = request.POST.get('token_number')
        try:
            token = Token.objects.get(queue=queue, token_number=token_number)
            if token.status == 'waiting':
                # Check if user should get notification
                ahead_count = Token.objects.filter(
                    queue=queue,
                    token_number__lt=token.token_number,
                    status__in=['waiting', 'ready']
                ).count()
                
                token.status = 'ready'
                token.save()
                messages.success(request, f'Token #{token_number} verified and marked as ready!')
            else:
                messages.warning(request, f'Token #{token_number} is not in waiting status.')
        except Token.DoesNotExist:
            messages.error(request, 'Token not found!')
    
    return redirect('admin_queue_detail', queue_id=queue_id)
