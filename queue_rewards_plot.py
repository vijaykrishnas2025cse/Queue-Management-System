import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = r'C:\Users\Administrator\Downloads\queue_rewards_dataset_1000.csv'
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'queue_rewards_plots.png')


def load_data(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Points Earned'] = pd.to_numeric(df['Points Earned'], errors='coerce').fillna(0).astype(int)
    return df


def plot_summary(df, output_path):
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Queue Rewards Dataset Visualization', fontsize=18, weight='bold')

    # Status distribution
    status_counts = df['Status'].value_counts().sort_values(ascending=True)
    axes[0, 0].barh(status_counts.index, status_counts.values, color='#2a9d8f')
    axes[0, 0].set_title('Status Distribution')
    axes[0, 0].set_xlabel('Count')

    # Points earned histogram
    axes[0, 1].hist(df['Points Earned'], bins=20, color='#e76f51', edgecolor='black')
    axes[0, 1].set_title('Points Earned Histogram')
    axes[0, 1].set_xlabel('Points Earned')
    axes[0, 1].set_ylabel('Frequency')

    # Average points per place
    place_points = df.groupby('Place')['Points Earned'].mean().sort_values()
    axes[1, 0].barh(place_points.index, place_points.values, color='#264653')
    axes[1, 0].set_title('Average Points by Place')
    axes[1, 0].set_xlabel('Average Points')

    # Monthly completed count over time
    if 'Date' in df.columns and not df['Date'].isna().all():
        monthly = (
            df[df['Status'] == 'Completed']
            .set_index('Date')
            .resample('ME')['Status']
            .count()
        )
        axes[1, 1].plot(monthly.index, monthly.values, marker='o', color='#f4a261')
        axes[1, 1].set_title('Completed Tokens Over Time')
        axes[1, 1].set_xlabel('Month')
        axes[1, 1].set_ylabel('Completed Count')
        axes[1, 1].grid(True, linestyle='--', alpha=0.35)
    else:
        axes[1, 1].text(0.5, 0.5, 'No valid Date data available', ha='center', va='center')
        axes[1, 1].set_title('Completed Tokens Over Time')
        axes[1, 1].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


if __name__ == '__main__':
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f'Dataset not found at {DATA_PATH}')
    df = load_data(DATA_PATH)
    print('Loaded dataset with shape:', df.shape)
    plot_summary(df, OUTPUT_PATH)
    print('Saved plot image to', OUTPUT_PATH)
