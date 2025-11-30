# visualization.py
# Task 2 - Visualization modülü
# -ozgur

"""
Task 2 için görselleştirme fonksiyonları.
Segmentasyon, trend analizleri ve karşılaştırmalar için grafikler oluşturur.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from typing import Dict, Optional

# Seaborn style ayarla
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_segment_distribution(user_segments: pd.DataFrame, save_path: Optional[str] = None):
    """
    User segment dağılımını gösteren grafik.
    
    Args:
        user_segments: Segment DataFrame (user_id, segment)
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 2 - First-day engagement segmentation visualization
    """
    segment_counts = user_segments['segment'].value_counts()
    
    plt.figure(figsize=(10, 6))
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    bars = plt.bar(segment_counts.index, segment_counts.values, color=colors[:len(segment_counts)])
    
    # Değerleri bar'ların üzerine yaz
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.xlabel('Segment', fontsize=12)
    plt.ylabel('User Count', fontsize=12)
    plt.title('User Distribution by First-Day Engagement Segment', fontsize=14, fontweight='bold')
    plt.xticks(rotation=0)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_session_duration_trends(trend_data: Dict[str, pd.DataFrame], save_path: Optional[str] = None):
    """
    Session duration trendlerini gösteren grafik.
    
    Args:
        trend_data: Trend analizi sonuçları (daily_trend, lifetime_trend)
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 2 - Session duration trends visualization
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Günlük trend
    daily_trend = trend_data['daily_trend']
    axes[0].plot(daily_trend['date'], daily_trend['avg_session_duration'], 
                 linewidth=2, color='#2E86AB', marker='o', markersize=4)
    axes[0].set_xlabel('Date', fontsize=11)
    axes[0].set_ylabel('Avg Session Duration (seconds)', fontsize=11)
    axes[0].set_title('Daily Average Session Duration Trend', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)
    
    # Kullanıcı lifetime'ına göre trend (days since install)
    lifetime_trend = trend_data['lifetime_trend']
    axes[1].plot(lifetime_trend['days_since_install'], lifetime_trend['avg_session_duration'],
                 linewidth=2, color='#A23B72', marker='s', markersize=4)
    axes[1].set_xlabel('Days Since Install', fontsize=11)
    axes[1].set_ylabel('Avg Session Duration (seconds)', fontsize=11)
    axes[1].set_title('Session Duration Trend by Days Since Install', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('Session Duration Trends Analysis', fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_retention_by_segment(retention_df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Segment bazlı retention eğrilerini gösteren grafik.
    
    Args:
        retention_df: Retention DataFrame (segment, day, retention_rate)
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 2 - Retention analysis visualization
    """
    plt.figure(figsize=(12, 7))
    
    segments = retention_df['segment'].unique()
    colors = {'High Engagement': '#2E86AB', 'Medium Engagement': '#A23B72', 'Low Engagement': '#F18F01'}
    
    for segment in segments:
        segment_data = retention_df[retention_df['segment'] == segment].sort_values('day')
        plt.plot(segment_data['day'], segment_data['retention_rate'] * 100,
                label=segment, linewidth=2.5, marker='o', markersize=5,
                color=colors.get(segment, '#000000'))
    
    plt.xlabel('Days Since Install', fontsize=12)
    plt.ylabel('Retention Rate (%)', fontsize=12)
    plt.title('Retention Curves by Engagement Segment', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_monetization_segments(monetization_df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Monetization segment dağılımını gösteren grafik.
    
    Args:
        monetization_df: Monetization segment DataFrame
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 2 - Monetization segmentation visualization
    """
    segment_counts = monetization_df['monetization_segment'].value_counts()
    
    plt.figure(figsize=(12, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(segment_counts)))
    bars = plt.barh(segment_counts.index, segment_counts.values, color=colors)
    
    # Değerleri bar'ların üzerine yaz
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width):,}',
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.xlabel('User Count', fontsize=12)
    plt.ylabel('Monetization Segment', fontsize=12)
    plt.title('User Distribution by Monetization Segment', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_match_completion_trends(completion_data: Dict[str, pd.DataFrame], save_path: Optional[str] = None):
    """
    Match completion rate trendlerini gösteren grafik.
    
    Args:
        completion_data: Completion trend DataFrame'leri
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 2 - Match completion trends visualization
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Günlük trend
    daily_trend = completion_data['daily_trend']
    axes[0].plot(daily_trend['event_date'], daily_trend['completion_rate'] * 100,
                 linewidth=2, color='#06A77D', marker='o', markersize=4)
    axes[0].set_xlabel('Date', fontsize=11)
    axes[0].set_ylabel('Completion Rate (%)', fontsize=11)
    axes[0].set_title('Daily Match Completion Rate Trend', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)
    
    # Kullanıcı lifetime'ına göre trend (days since install)
    lifetime_trend = completion_data['lifetime_trend']
    axes[1].plot(lifetime_trend['days_since_install'], lifetime_trend['completion_rate'] * 100,
                 linewidth=2, color='#F18F01', marker='s', markersize=4)
    axes[1].set_xlabel('Days Since Install', fontsize=11)
    axes[1].set_ylabel('Completion Rate (%)', fontsize=11)
    axes[1].set_title('Match Completion Rate Trend by Days Since Install', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('Match Completion Trends Analysis', fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_platform_country_comparison(comparison_data: Dict[str, pd.DataFrame], save_path: Optional[str] = None):
    """
    Platform ve country karşılaştırmalarını gösteren grafikler.
    
    Args:
        comparison_data: Platform ve country istatistikleri
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 2 - Platform and country comparison visualization
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    platform_stats = comparison_data['platform_stats']
    country_stats = comparison_data['country_stats']
    
    # Platform bazlı user count
    axes[0, 0].bar(platform_stats['platform'], platform_stats['user_id'], color='#2E86AB')
    axes[0, 0].set_xlabel('Platform', fontsize=11)
    axes[0, 0].set_ylabel('Unique Users', fontsize=11)
    axes[0, 0].set_title('User Count by Platform', fontsize=12, fontweight='bold')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # Platform bazlı revenue
    x_pos = np.arange(len(platform_stats))
    width = 0.35
    axes[0, 1].bar(x_pos - width/2, platform_stats['iap_revenue'], width, label='IAP Revenue', color='#06A77D')
    axes[0, 1].bar(x_pos + width/2, platform_stats['ad_revenue'], width, label='Ad Revenue', color='#F18F01')
    axes[0, 1].set_xlabel('Platform', fontsize=11)
    axes[0, 1].set_ylabel('Revenue ($)', fontsize=11)
    axes[0, 1].set_title('Revenue by Platform', fontsize=12, fontweight='bold')
    axes[0, 1].set_xticks(x_pos)
    axes[0, 1].set_xticklabels(platform_stats['platform'], rotation=45)
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Top 10 Country bazlı user count
    axes[1, 0].barh(country_stats['country'], country_stats['user_id'], color='#A23B72')
    axes[1, 0].set_xlabel('Unique Users', fontsize=11)
    axes[1, 0].set_ylabel('Country', fontsize=11)
    axes[1, 0].set_title('Top 10 Countries by User Count', fontsize=12, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3, axis='x')
    
    # Top 10 Country bazlı revenue
    axes[1, 1].barh(country_stats['country'], country_stats['total_revenue'], color='#F18F01')
    axes[1, 1].set_xlabel('Total Revenue ($)', fontsize=11)
    axes[1, 1].set_ylabel('Country', fontsize=11)
    axes[1, 1].set_title('Top 10 Countries by Revenue', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='x')
    
    plt.suptitle('Platform and Country Comparison Analysis', fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_win_rate_trends(win_rate_data: Dict[str, pd.DataFrame], save_path: Optional[str] = None):
    """
    Win rate trendlerini gösteren grafik.
    
    Args:
        win_rate_data: Win rate trend DataFrame'leri
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 2 - Win rate trends visualization
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Günlük trend
    daily_trend = win_rate_data['daily_trend']
    axes[0].plot(daily_trend['event_date'], daily_trend['overall_win_rate'] * 100,
                 linewidth=2, color='#2E86AB', marker='o', markersize=4)
    axes[0].set_xlabel('Date', fontsize=11)
    axes[0].set_ylabel('Win Rate (%)', fontsize=11)
    axes[0].set_title('Daily Win Rate Trend', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)
    
    # Kullanıcı lifetime'ına göre trend (days since install)
    lifetime_trend = win_rate_data['lifetime_trend']
    axes[1].plot(lifetime_trend['days_since_install'], lifetime_trend['overall_win_rate'] * 100,
                 linewidth=2, color='#A23B72', marker='s', markersize=4)
    axes[1].set_xlabel('Days Since Install', fontsize=11)
    axes[1].set_ylabel('Win Rate (%)', fontsize=11)
    axes[1].set_title('Win Rate Trend by Days Since Install', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('Win Rate Trends Analysis', fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()

