# config.py
# Task 1 - Configuration dosyası
# -ozgur

"""
Task 1 için tüm varyant konfigürasyonlarını içeren modül.
Retention noktaları, monetizasyon parametreleri ve diğer varyant ayarları burada tanımlanır.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class VariantConfig:
    """
    Her bir varyant için config yapısı.
    Retention noktaları sırasıyla [1, 3, 7, 14] günlerindeki retention oranlarını içeriyor.
    
    Kullanım: Task 1 - Tüm sorular (a-f)
    """
    name: str
    retention_points: List[float]  # [Day 1, Day 3, Day 7, Day 14] retention değerleri
    daily_purchase_ratio: float  # Günlük satın alma oranı (örn: 0.0305 = %3.05)
    ecpm: float  # eCPM değeri ($)
    ad_impressions_per_dau: float  # DAU başına ad impression sayısı
    daily_new_users: int = 20000  # Her gün gelen yeni kullanıcı sayısı
    average_purchase_amount: float = 1.0  # Ortalama satın alma tutarı ($) - PDF'de belirtilmemiş, varsayılan


# Variant A konfigürasyonu
VARIANT_A = VariantConfig(
    name="Variant A",
    retention_points=[0.53, 0.27, 0.17, 0.06],  # Day 1, 3, 7, 14 retention değerleri (PDF'den)
    daily_purchase_ratio=0.0305,  # %3.05
    ecpm=9.80,
    ad_impressions_per_dau=2.3,
    daily_new_users=20000,
    average_purchase_amount=1.0
)

# Variant B konfigürasyonu
VARIANT_B = VariantConfig(
    name="Variant B",
    retention_points=[0.48, 0.25, 0.19, 0.09],  # Day 1, 3, 7, 14 retention değerleri (PDF'den)
    daily_purchase_ratio=0.0315,  # %3.15
    ecpm=10.80,
    ad_impressions_per_dau=1.6,
    daily_new_users=20000,
    average_purchase_amount=1.0
)

