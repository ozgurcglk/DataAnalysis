# retention_model.py
# Task 1 - Retention Model sınıfı
# -ozgur

"""
Power Law retention modeli için curve fitting işlemlerini yapan modül.
scipy.optimize.curve_fit kullanarak verilen retention noktalarına (1, 3, 7, 14 günler) 
Power Law (a * t^b) eğrisi uydurur ve herhangi bir gün için retention oranını hesaplar.
"""

import numpy as np
from scipy.optimize import curve_fit


def power_law(t: float, a: float, b: float) -> float:
    """
    Power Law fonksiyonu: R(t) = a * t^b
    
    Args:
        t: Gün sayısı (1, 2, 3, ...)
        a: Scaling parametresi
        b: Exponent parametresi (genellikle negatif)
    
    Returns:
        Retention oranı (0-1 arası)
    """
    return a * (t ** b)


class RetentionModel:
    """
    Retention modeli sınıfı.
    Verilen retention noktalarına Power Law eğrisi uydurur ve 
    herhangi bir gün için retention oranını tahmin eder.
    
    Kullanım: Task 1 - Tüm sorular (a-f)
    """
    
    def __init__(self, retention_points: list[float], days: list[int] = None):
        """
        Retention modelini başlatır ve curve fitting yapar.
        
        Args:
            retention_points: Retention değerleri listesi [Day 1, Day 3, Day 7, Day 14]
            days: Retention noktalarının hangi günlerde olduğu (varsayılan: [1, 3, 7, 14])
        """
        if days is None:
            days = [1, 3, 7, 14]
        
        self.retention_points = np.array(retention_points)
        self.days = np.array(days)
        
        # Power Law parametrelerini fit et
        # İlk retention değerini a parametresinin başlangıç değeri olarak kullanıyoruz
        # b parametresi için -0.5 gibi bir başlangıç değeri kullanıyoruz (tipik retention eğrileri için)
        initial_a = retention_points[0] if retention_points[0] > 0 else 0.5
        initial_b = -0.5
        
        try:
            # Curve fitting yapılıyor
            # maxfev parametresi iterasyon sayısını artırıyor, daha iyi sonuç için
            popt, _ = curve_fit(
                power_law,
                self.days,
                self.retention_points,
                p0=[initial_a, initial_b],
                maxfev=5000,
                bounds=([0, -2], [2, 0])  # a: [0, 2], b: [-2, 0] aralığında
            )
            self.a, self.b = popt
        except Exception as e:
            # Eğer fitting başarısız olursa, basit bir yaklaşım kullan
            print(f"Warning: Curve fitting failed with error: {e}")
            print("Using fallback parameters")
            self.a = retention_points[0] if retention_points[0] > 0 else 0.5
            self.b = -0.5
    
    def get_retention(self, day: int) -> float:
        """
        Belirli bir gün için retention oranını döndürür.
        
        Args:
            day: Gün sayısı (1, 2, 3, ...)
        
        Returns:
            Retention oranı (0-1 arası)
        """
        if day <= 0:
            return 0.0
        
        retention = power_law(day, self.a, self.b)
        
        # Retention oranı 0-1 aralığında olmalı
        return max(0.0, min(1.0, retention))
    
    def get_retention_array(self, days: list[int]) -> np.ndarray:
        """
        Birden fazla gün için retention oranlarını döndürür.
        
        Args:
            days: Gün sayıları listesi
        
        Returns:
            Retention oranları array'i
        """
        return np.array([self.get_retention(day) for day in days])

