# analysis.py
# Task 2 - Analysis modülü
# -ozgur

"""
Task 2 için exploratory data analysis fonksiyonları.
User segmentation, trend analizleri ve yaratıcı analizler bu modülde yer alır.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List


def segment_users_by_first_day_engagement(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kullanıcıları ilk gün engagement'lerine göre segmentlere ayırır.
    
    İlk gün metrikleri:
    - Session count
    - Session duration
    - Match count
    - Revenue
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        Segment bilgilerini içeren DataFrame (user_id ve segment)
    
    Kullanım: Task 2 - First-day engagement segmentation
    """
    # Her kullanıcının ilk gün verilerini al
    first_day = df[df['days_since_install'] == 0].copy()
    
    # Kullanıcı bazında ilk gün metriklerini hesapla
    first_day_metrics = first_day.groupby('user_id').agg({
        'total_session_count': 'sum',
        'total_session_duration': 'sum',
        'match_start_count': 'sum',
        'total_revenue': 'sum'
    }).reset_index()
    
    # Segmentasyon için threshold'ları belirle (percentile bazlı)
    session_count_q33 = first_day_metrics['total_session_count'].quantile(0.33)
    session_count_q66 = first_day_metrics['total_session_count'].quantile(0.66)
    
    session_duration_q33 = first_day_metrics['total_session_duration'].quantile(0.33)
    session_duration_q66 = first_day_metrics['total_session_duration'].quantile(0.66)
    
    match_count_q33 = first_day_metrics['match_start_count'].quantile(0.33)
    match_count_q66 = first_day_metrics['match_start_count'].quantile(0.66)
    
    # Segmentasyon fonksiyonu
    def assign_segment(row):
        score = 0
        
        # Session count puanı
        if row['total_session_count'] >= session_count_q66:
            score += 3
        elif row['total_session_count'] >= session_count_q33:
            score += 2
        else:
            score += 1
        
        # Session duration puanı
        if row['total_session_duration'] >= session_duration_q66:
            score += 3
        elif row['total_session_duration'] >= session_duration_q33:
            score += 2
        else:
            score += 1
        
        # Match count puanı
        if row['match_start_count'] >= match_count_q66:
            score += 3
        elif row['match_start_count'] >= match_count_q33:
            score += 2
        else:
            score += 1
        
        # Segment belirleme
        if score >= 8:
            return 'High Engagement'
        elif score >= 5:
            return 'Medium Engagement'
        else:
            return 'Low Engagement'
    
    first_day_metrics['segment'] = first_day_metrics.apply(assign_segment, axis=1)
    
    return first_day_metrics[['user_id', 'segment']]


def analyze_session_duration_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Session duration'ın zaman içindeki trendlerini analiz eder.
    Hem gün bazlı hem de kullanıcı yaşına göre trendleri hesaplar.
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        Trend analizi sonuçlarını içeren DataFrame
    
    Kullanım: Task 2 - Session duration trends analysis
    """
    # Gün bazlı ortalama session duration
    daily_avg_duration = df.groupby('event_date').agg({
        'avg_session_duration': 'mean',
        'total_session_duration': 'mean',
        'total_session_count': 'sum'
    }).reset_index()
    daily_avg_duration.columns = ['date', 'avg_session_duration', 'avg_total_duration', 'total_sessions']
    
    # Kullanıcı lifetime'ına göre (days_since_install) session duration trendi
    lifetime_duration = df.groupby('days_since_install').agg({
        'avg_session_duration': 'mean',
        'total_session_duration': 'mean',
        'user_id': 'nunique'
    }).reset_index()
    lifetime_duration.columns = ['days_since_install', 'avg_session_duration', 'avg_total_duration', 'unique_users']
    
    return {
        'daily_trend': daily_avg_duration,
        'lifetime_trend': lifetime_duration
    }


def analyze_retention_by_segment(df: pd.DataFrame, user_segments: pd.DataFrame) -> pd.DataFrame:
    """
    Segment bazlı retention analizi yapar.
    Her segment için gün bazlı retention oranlarını hesaplar.
    
    Args:
        df: Preprocessed DataFrame
        user_segments: User segmentation DataFrame (user_id, segment)
    
    Returns:
        Segment bazlı retention DataFrame
    
    Kullanım: Task 2 - Retention analysis by segment
    """
    # Segment bilgilerini ana DataFrame'e ekle
    df_with_segment = df.merge(user_segments, on='user_id', how='left')
    
    # Her segment için gün bazlı aktif kullanıcı sayısı
    retention_by_segment = df_with_segment.groupby(['segment', 'days_since_install']).agg({
        'user_id': 'nunique'
    }).reset_index()
    retention_by_segment.columns = ['segment', 'day', 'active_users']
    
    # Her segment için Day 0'daki kullanıcı sayısını bul
    day0_users = df_with_segment[df_with_segment['days_since_install'] == 0].groupby('segment')['user_id'].nunique().reset_index()
    day0_users.columns = ['segment', 'day0_users']
    
    # Retention oranını hesapla
    retention_by_segment = retention_by_segment.merge(day0_users, on='segment')
    retention_by_segment['retention_rate'] = retention_by_segment['active_users'] / retention_by_segment['day0_users']
    
    return retention_by_segment


def analyze_monetization_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kullanıcıları monetization davranışlarına göre segmentlere ayırır.
    IAP vs Ad revenue bazlı segmentasyon.
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        Monetization segment bilgilerini içeren DataFrame
    
    Kullanım: Task 2 - Monetization segmentation
    """
    # Kullanıcı bazında toplam revenue hesapla
    user_revenue = df.groupby('user_id').agg({
        'iap_revenue': 'sum',
        'ad_revenue': 'sum',
        'total_revenue': 'sum'
    }).reset_index()
    
    # Segmentasyon: IAP-focused, Ad-focused, Mixed, Non-paying
    def assign_monetization_segment(row):
        total_rev = row['total_revenue']
        iap_rev = row['iap_revenue']
        ad_rev = row['ad_revenue']
        
        if total_rev == 0:
            return 'Non-paying'
        elif iap_rev > 0 and ad_rev == 0:
            return 'IAP-focused'
        elif ad_rev > 0 and iap_rev == 0:
            return 'Ad-focused'
        elif iap_rev > ad_rev:
            return 'Mixed (IAP-dominant)'
        else:
            return 'Mixed (Ad-dominant)'
    
    user_revenue['monetization_segment'] = user_revenue.apply(assign_monetization_segment, axis=1)
    
    return user_revenue[['user_id', 'monetization_segment', 'iap_revenue', 'ad_revenue', 'total_revenue']]


def analyze_match_completion_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Match completion rate'lerinin zaman içindeki trendlerini analiz eder.
    Match start vs match end oranlarını hesaplar.
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        Match completion trend DataFrame
    
    Kullanım: Task 2 - Match completion trends
    """
    # Gün bazlı match completion rate
    daily_match_stats = df.groupby('event_date').agg({
        'match_start_count': 'sum',
        'match_end_count': 'sum'
    }).reset_index()
    
    daily_match_stats['completion_rate'] = (
        daily_match_stats['match_end_count'] / daily_match_stats['match_start_count'].replace(0, 1)
    )
    
    # Kullanıcı lifetime'ına göre (days_since_install) match completion rate
    lifetime_match_stats = df.groupby('days_since_install').agg({
        'match_start_count': 'sum',
        'match_end_count': 'sum'
    }).reset_index()
    
    lifetime_match_stats['completion_rate'] = (
        lifetime_match_stats['match_end_count'] / lifetime_match_stats['match_start_count'].replace(0, 1)
    )
    
    return {
        'daily_trend': daily_match_stats,
        'lifetime_trend': lifetime_match_stats
    }


def analyze_platform_country_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """
    Platform ve country bazlı karşılaştırma analizi yapar.
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        Platform ve country karşılaştırma DataFrame'leri
    
    Kullanım: Task 2 - Platform and country analysis
    """
    # Platform bazlı metrikler
    platform_stats = df.groupby('platform').agg({
        'user_id': 'nunique',
        'total_session_count': 'sum',
        'total_session_duration': 'mean',
        'total_revenue': 'sum',
        'iap_revenue': 'sum',
        'ad_revenue': 'sum',
        'win_rate': 'mean'
    }).reset_index()
    
    # Country bazlı metrikler (top 10)
    country_stats = df.groupby('country').agg({
        'user_id': 'nunique',
        'total_session_count': 'sum',
        'total_session_duration': 'mean',
        'total_revenue': 'sum',
        'iap_revenue': 'sum',
        'ad_revenue': 'sum',
        'win_rate': 'mean'
    }).reset_index().sort_values('user_id', ascending=False).head(10)
    
    return {
        'platform_stats': platform_stats,
        'country_stats': country_stats
    }


def analyze_win_rate_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Win rate'lerin zaman içindeki trendlerini analiz eder.
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        Win rate trend DataFrame
    
    Kullanım: Task 2 - Win rate trends analysis
    """
    # Gün bazlı win rate
    daily_win_rate = df.groupby('event_date').agg({
        'victory_count': 'sum',
        'defeat_count': 'sum',
        'win_rate': 'mean'
    }).reset_index()
    
    daily_win_rate['overall_win_rate'] = (
        daily_win_rate['victory_count'] / (daily_win_rate['victory_count'] + daily_win_rate['defeat_count']).replace(0, 1)
    )
    
    # Kullanıcı lifetime'ına göre (days_since_install) win rate
    lifetime_win_rate = df.groupby('days_since_install').agg({
        'victory_count': 'sum',
        'defeat_count': 'sum',
        'win_rate': 'mean'
    }).reset_index()
    
    lifetime_win_rate['overall_win_rate'] = (
        lifetime_win_rate['victory_count'] / (lifetime_win_rate['victory_count'] + lifetime_win_rate['defeat_count']).replace(0, 1)
    )
    
    return {
        'daily_trend': daily_win_rate,
        'lifetime_trend': lifetime_win_rate
    }

