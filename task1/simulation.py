# simulation.py
# Task 1 - Simulation fonksiyonları
# -ozgur

"""
DAU (Daily Active Users) ve revenue hesaplamalarını yapan modül.
Retention modelini kullanarak günlük aktif kullanıcı sayısını ve gelirleri hesaplar.
"""

import numpy as np
from typing import Dict, Callable, Optional
from retention_model import RetentionModel
from config import VariantConfig


def calculate_dau(retention_model: RetentionModel, daily_new_users: int, days: int) -> np.ndarray:
    """
    Her gün için DAU (Daily Active Users) hesaplar.
    Cohort analizi yaparak her günün aktif kullanıcı sayısını bulur.
    
    Args:
        retention_model: Retention modeli instance'ı
        daily_new_users: Her gün gelen yeni kullanıcı sayısı
        days: Simüle edilecek gün sayısı
    
    Returns:
        Her gün için DAU değerlerini içeren array
    
    Kullanım: Task 1 - Soru a, c, d, e, f
    """
    dau = np.zeros(days)
    
    # Her gün için, o gün gelen yeni kullanıcılar ve önceki günlerden gelen kullanıcılar
    for current_day in range(1, days + 1):
        total_dau = 0
        
        # Her önceki günün cohort'unun bugünkü katkısını hesapla
        for cohort_day in range(1, current_day + 1):
            # Bu cohort'tan bugün kaç kullanıcı aktif?
            days_since_cohort = current_day - cohort_day + 1
            retention_rate = retention_model.get_retention(days_since_cohort)
            active_from_cohort = daily_new_users * retention_rate
            total_dau += active_from_cohort
        
        dau[current_day - 1] = total_dau
    
    return dau


def simulate_variant(variant_config: VariantConfig, days: int) -> Dict[str, np.ndarray]:
    """
    Bir varyant için simülasyon çalıştırır.
    DAU ve revenue hesaplamalarını yapar.
    
    Args:
        variant_config: Varyant konfigürasyonu
        days: Simüle edilecek gün sayısı
    
    Returns:
        DAU ve revenue bilgilerini içeren dictionary
    
    Kullanım: Task 1 - Tüm sorular (a-f)
    """
    # Retention modelini oluştur
    retention_model = RetentionModel(variant_config.retention_points)
    
    # DAU hesapla
    dau = calculate_dau(retention_model, variant_config.daily_new_users, days)
    
    # Revenue hesapla
    revenue_info = calculate_revenue(
        dau=dau,
        daily_purchase_ratio=variant_config.daily_purchase_ratio,
        ecpm=variant_config.ecpm,
        ad_impressions_per_dau=variant_config.ad_impressions_per_dau,
        average_purchase_amount=variant_config.average_purchase_amount
    )
    
    return {
        'dau': dau,
        'iap_revenue': revenue_info['iap_revenue'],
        'ad_revenue': revenue_info['ad_revenue'],
        'total_revenue': revenue_info['total_revenue']
    }


def calculate_revenue(
    dau: np.ndarray,
    daily_purchase_ratio: float,
    ecpm: float,
    ad_impressions_per_dau: float,
    average_purchase_amount: float
) -> Dict[str, np.ndarray]:
    """
    Her gün için revenue hesaplar.
    IAP (In-App Purchase) ve Ad revenue'larını ayrı ayrı hesaplar.
    
    Args:
        dau: Her gün için DAU değerleri
        daily_purchase_ratio: Günlük satın alma oranı
        ecpm: eCPM değeri ($)
        ad_impressions_per_dau: DAU başına ad impression sayısı
        average_purchase_amount: Ortalama satın alma tutarı ($)
    
    Returns:
        IAP, Ad ve Total revenue array'lerini içeren dictionary
    
    Kullanım: Task 1 - Soru b, c, d, e, f
    """
    # IAP Revenue = DAU * daily_purchase_ratio * average_purchase_amount
    iap_revenue = dau * daily_purchase_ratio * average_purchase_amount
    
    # Ad Impressions = DAU * ad_impressions_per_dau
    ad_impressions = dau * ad_impressions_per_dau
    
    # Ad Revenue = (Ad Impressions / 1000) * eCPM
    ad_revenue = (ad_impressions / 1000.0) * ecpm
    
    # Total Revenue
    total_revenue = iap_revenue + ad_revenue
    
    return {
        'iap_revenue': iap_revenue,
        'ad_revenue': ad_revenue,
        'total_revenue': total_revenue
    }


def exponential_retention(day: int, base: float, decay: float) -> float:
    """
    Exponential retention formülü: Retention = base * e^(-decay * (day - 1))
    
    Args:
        day: Gün sayısı (1, 2, 3, ...)
        base: Başlangıç retention değeri
        decay: Decay parametresi
    
    Returns:
        Retention oranı (0-1 arası)
    
    Kullanım: Task 1 - Soru e (yeni kullanıcı kaynağı retention'ı)
    """
    if day <= 0:
        return 0.0
    retention = base * np.exp(-decay * (day - 1))
    return max(0.0, min(1.0, retention))


def calculate_dau_with_mixed_sources(
    retention_model_old: RetentionModel,
    retention_func_new: Callable[[int], float],
    daily_new_users_old: int,
    daily_new_users_new: int,
    days: int,
    new_source_start_day: int = 20,
    daily_new_users_before_new_source: int = None
) -> np.ndarray:
    """
    İki farklı kullanıcı kaynağı için DAU hesaplar.
    Belirli bir günden itibaren yeni kaynak eklenir.
    
    Args:
        retention_model_old: Eski kullanıcılar için retention modeli
        retention_func_new: Yeni kullanıcılar için retention fonksiyonu (day -> retention)
        daily_new_users_old: Yeni kaynak başladıktan sonra eski kaynaktan gelen günlük kullanıcı sayısı
        daily_new_users_new: Yeni kaynaktan gelen günlük kullanıcı sayısı
        days: Simüle edilecek gün sayısı
        new_source_start_day: Yeni kaynağın başladığı gün (1-indexed)
        daily_new_users_before_new_source: Yeni kaynak başlamadan önce gelen günlük kullanıcı sayısı
                                         (None ise daily_new_users_old + daily_new_users_new kullanılır)
    
    Returns:
        Her gün için DAU değerlerini içeren array
    
    Kullanım: Task 1 - Soru e
    """
    dau = np.zeros(days)
    
    # Yeni kaynak başlamadan önce gelen kullanıcı sayısı
    if daily_new_users_before_new_source is None:
        daily_new_users_before_new_source = daily_new_users_old + daily_new_users_new
    
    for current_day in range(1, days + 1):
        total_dau = 0
        
        # Yeni kaynak başlamadan önceki günlerden gelen kullanıcılar (tümü eski kaynak)
        for cohort_day in range(1, min(new_source_start_day, current_day + 1)):
            days_since_cohort = current_day - cohort_day + 1
            retention_rate = retention_model_old.get_retention(days_since_cohort)
            active_from_cohort = daily_new_users_before_new_source * retention_rate
            total_dau += active_from_cohort
        
        # Yeni kaynak başladıktan sonraki günlerden gelen kullanıcılar
        if current_day >= new_source_start_day:
            # Eski kaynaktan gelen kullanıcılar (20. günden itibaren)
            for cohort_day in range(new_source_start_day, current_day + 1):
                days_since_cohort = current_day - cohort_day + 1
                retention_rate = retention_model_old.get_retention(days_since_cohort)
                active_from_cohort = daily_new_users_old * retention_rate
                total_dau += active_from_cohort
            
            # Yeni kaynaktan gelen kullanıcılar (20. günden itibaren)
            for cohort_day in range(new_source_start_day, current_day + 1):
                days_since_cohort = current_day - cohort_day + 1
                retention_rate = retention_func_new(days_since_cohort)
                active_from_cohort = daily_new_users_new * retention_rate
                total_dau += active_from_cohort
        
        dau[current_day - 1] = total_dau
    
    return dau

