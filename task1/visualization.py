# visualization.py
# Task 1 - Visualization modülü
# -ozgur

"""
Task 1 için grafik oluşturma fonksiyonları.
DAU trendleri, revenue karşılaştırmaları ve retention eğrileri için görselleştirmeler.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Optional
import os


def plot_dau_comparison(
    result_a: Dict[str, np.ndarray],
    result_b: Dict[str, np.ndarray],
    days: int,
    title: str = "DAU Comparison",
    save_path: Optional[str] = None
):
    """
    Variant A ve B'nin DAU karşılaştırmasını gösteren grafik.
    
    Args:
        result_a: Variant A simülasyon sonuçları
        result_b: Variant B simülasyon sonuçları
        days: Gün sayısı
        title: Grafik başlığı
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 1 - Soru a, c, d, e, f
    """
    plt.figure(figsize=(12, 6))
    days_array = np.arange(1, days + 1)
    
    plt.plot(days_array, result_a['dau'], label='Variant A', linewidth=2, color='#2E86AB')
    plt.plot(days_array, result_b['dau'], label='Variant B', linewidth=2, color='#A23B72')
    
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Daily Active Users (DAU)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        # Klasörü oluştur (yoksa)
        dir_path = os.path.dirname(save_path)
        if dir_path:  # Klasör yolu varsa oluştur
            os.makedirs(dir_path, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_revenue_comparison(
    result_a: Dict[str, np.ndarray],
    result_b: Dict[str, np.ndarray],
    days: int,
    title: str = "Revenue Comparison",
    save_path: Optional[str] = None
):
    """
    Variant A ve B'nin revenue karşılaştırmasını gösteren grafik.
    
    Args:
        result_a: Variant A simülasyon sonuçları
        result_b: Variant B simülasyon sonuçları
        days: Gün sayısı
        title: Grafik başlığı
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 1 - Soru b, c, d, e, f
    """
    plt.figure(figsize=(12, 6))
    days_array = np.arange(1, days + 1)
    
    plt.plot(days_array, result_a['total_revenue'], label='Variant A', linewidth=2, color='#2E86AB')
    plt.plot(days_array, result_b['total_revenue'], label='Variant B', linewidth=2, color='#A23B72')
    
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Daily Revenue ($)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        # Klasörü oluştur (yoksa)
        dir_path = os.path.dirname(save_path)
        if dir_path:  # Klasör yolu varsa oluştur
            os.makedirs(dir_path, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_cumulative_revenue(
    result_a: Dict[str, np.ndarray],
    result_b: Dict[str, np.ndarray],
    days: int,
    title: str = "Cumulative Revenue Comparison",
    save_path: Optional[str] = None
):
    """
    Variant A ve B'nin kümülatif revenue karşılaştırmasını gösteren grafik.
    
    Args:
        result_a: Variant A simülasyon sonuçları
        result_b: Variant B simülasyon sonuçları
        days: Gün sayısı
        title: Grafik başlığı
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 1 - Soru b, c, d, e, f
    """
    plt.figure(figsize=(12, 6))
    days_array = np.arange(1, days + 1)
    
    cumulative_a = np.cumsum(result_a['total_revenue'])
    cumulative_b = np.cumsum(result_b['total_revenue'])
    
    plt.plot(days_array, cumulative_a, label='Variant A', linewidth=2, color='#2E86AB')
    plt.plot(days_array, cumulative_b, label='Variant B', linewidth=2, color='#A23B72')
    
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Cumulative Revenue ($)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        # Klasörü oluştur (yoksa)
        dir_path = os.path.dirname(save_path)
        if dir_path:  # Klasör yolu varsa oluştur
            os.makedirs(dir_path, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_retention_curves(
    retention_model_a,
    retention_model_b,
    max_days: int = 30,
    title: str = "Retention Curves Comparison",
    save_path: Optional[str] = None
):
    """
    Variant A ve B'nin retention eğrilerini gösteren grafik.
    
    Args:
        retention_model_a: Variant A retention modeli
        retention_model_b: Variant B retention modeli
        max_days: Maksimum gün sayısı
        title: Grafik başlığı
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 1 - Genel analiz
    """
    plt.figure(figsize=(12, 6))
    days_array = np.arange(1, max_days + 1)
    
    retention_a = np.array([retention_model_a.get_retention(day) for day in days_array])
    retention_b = np.array([retention_model_b.get_retention(day) for day in days_array])
    
    plt.plot(days_array, retention_a * 100, label='Variant A', linewidth=2, color='#2E86AB')
    plt.plot(days_array, retention_b * 100, label='Variant B', linewidth=2, color='#A23B72')
    
    # Retention noktalarını işaretle
    retention_days = [1, 3, 7, 14]
    retention_a_points = [retention_model_a.get_retention(d) * 100 for d in retention_days]
    retention_b_points = [retention_model_b.get_retention(d) * 100 for d in retention_days]
    
    plt.scatter(retention_days, retention_a_points, color='#2E86AB', s=100, zorder=5, marker='o')
    plt.scatter(retention_days, retention_b_points, color='#A23B72', s=100, zorder=5, marker='s')
    
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Retention Rate (%)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        # Klasörü oluştur (yoksa)
        dir_path = os.path.dirname(save_path)
        if dir_path:  # Klasör yolu varsa oluştur
            os.makedirs(dir_path, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def plot_revenue_breakdown(
    result_a: Dict[str, np.ndarray],
    result_b: Dict[str, np.ndarray],
    days: int,
    title: str = "Revenue Breakdown (IAP vs Ad)",
    save_path: Optional[str] = None
):
    """
    Variant A ve B'nin IAP ve Ad revenue karşılaştırmasını gösteren grafik.
    
    Args:
        result_a: Variant A simülasyon sonuçları
        result_b: Variant B simülasyon sonuçları
        days: Gün sayısı
        title: Grafik başlığı
        save_path: Kaydedilecek dosya yolu (None ise göstermez)
    
    Kullanım: Task 1 - Detaylı analiz
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    days_array = np.arange(1, days + 1)
    
    # Variant A
    axes[0].plot(days_array, result_a['iap_revenue'], label='IAP Revenue', linewidth=2, color='#06A77D')
    axes[0].plot(days_array, result_a['ad_revenue'], label='Ad Revenue', linewidth=2, color='#F18F01')
    axes[0].set_title('Variant A - Revenue Breakdown', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Revenue ($)', fontsize=11)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # Variant B
    axes[1].plot(days_array, result_b['iap_revenue'], label='IAP Revenue', linewidth=2, color='#06A77D')
    axes[1].plot(days_array, result_b['ad_revenue'], label='Ad Revenue', linewidth=2, color='#F18F01')
    axes[1].set_title('Variant B - Revenue Breakdown', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Day', fontsize=11)
    axes[1].set_ylabel('Revenue ($)', fontsize=11)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if save_path:
        # Klasörü oluştur (yoksa)
        dir_path = os.path.dirname(save_path)
        if dir_path:  # Klasör yolu varsa oluştur
            os.makedirs(dir_path, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    plt.close()


def create_all_visualizations(
    result_a: Dict[str, np.ndarray],
    result_b: Dict[str, np.ndarray],
    retention_model_a,
    retention_model_b,
    days: int,
    output_dir: str = "task1/graphs"
):
    """
    Tüm görselleştirmeleri oluşturur ve kaydeder.
    
    Args:
        result_a: Variant A simülasyon sonuçları
        result_b: Variant B simülasyon sonuçları
        retention_model_a: Variant A retention modeli
        retention_model_b: Variant B retention modeli
        days: Gün sayısı
        output_dir: Grafiklerin kaydedileceği klasör
    
    Kullanım: Task 1 - Tüm sorular için görselleştirme
    """
    # Klasörü oluştur
    os.makedirs(output_dir, exist_ok=True)
    
    # DAU karşılaştırması
    plot_dau_comparison(
        result_a, result_b, days,
        title=f"DAU Comparison - {days} Days",
        save_path=f"{output_dir}/dau_comparison_{days}d.png"
    )
    
    # Revenue karşılaştırması
    plot_revenue_comparison(
        result_a, result_b, days,
        title=f"Daily Revenue Comparison - {days} Days",
        save_path=f"{output_dir}/revenue_comparison_{days}d.png"
    )
    
    # Kümülatif revenue
    plot_cumulative_revenue(
        result_a, result_b, days,
        title=f"Cumulative Revenue Comparison - {days} Days",
        save_path=f"{output_dir}/cumulative_revenue_{days}d.png"
    )
    
    # Retention eğrileri
    plot_retention_curves(
        retention_model_a, retention_model_b,
        max_days=days,
        title="Retention Curves Comparison",
        save_path=f"{output_dir}/retention_curves.png"
    )
    
    # Revenue breakdown
    plot_revenue_breakdown(
        result_a, result_b, days,
        title=f"Revenue Breakdown (IAP vs Ad) - {days} Days",
        save_path=f"{output_dir}/revenue_breakdown_{days}d.png"
    )
    
    print(f"\nTüm grafikler '{output_dir}' klasörüne kaydedildi.")

