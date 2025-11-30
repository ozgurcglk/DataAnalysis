# run_task1.py
# Task 1 - Ana çalıştırma scripti - Kodu buradan çalıştırabilirsiniz.
# -ozgur

"""
Task 1'in tüm alt sorularını (a-f) sırasıyla çalıştıran ana script.
Her soru için gerekli simülasyonları yapar ve sonuçları ekrana basar.
"""

from config import VARIANT_A, VARIANT_B, VariantConfig
from simulation import simulate_variant, calculate_dau_with_mixed_sources, exponential_retention, calculate_revenue
from retention_model import RetentionModel
from visualization import create_all_visualizations, plot_dau_comparison, plot_revenue_comparison, plot_cumulative_revenue
import numpy as np
import os
import glob


def task1_a():
    """
    Task 1a: 15. günün sonunda A ve B varyantlarının DAU sayılarını karşılaştır.
    
    Kullanım: Task 1 - Soru a
    """
    print("\n" + "="*60)
    print("TASK 1A: DAU Karşılaştırması (15. Gün)")
    print("="*60)
    
    days = 15
    result_a = simulate_variant(VARIANT_A, days)
    result_b = simulate_variant(VARIANT_B, days)
    
    dau_a = result_a['dau'][-1]
    dau_b = result_b['dau'][-1]
    
    print(f"\nVariant A - 15. Gün DAU: {dau_a:,.0f}")
    print(f"Variant B - 15. Gün DAU: {dau_b:,.0f}")
    
    if dau_a > dau_b:
        diff = ((dau_a - dau_b) / dau_b) * 100
        print(f"\nVariant A, Variant B'den %{diff:.2f} daha yüksek DAU'ya sahip.")
    else:
        diff = ((dau_b - dau_a) / dau_a) * 100
        print(f"\nVariant B, Variant A'dan %{diff:.2f} daha yüksek DAU'ya sahip.")
    
    # Grafik oluştur - Task 1a: Which variant will have the most daily active users after 15 days?
    retention_model_a = RetentionModel(VARIANT_A.retention_points)
    retention_model_b = RetentionModel(VARIANT_B.retention_points)
    plot_dau_comparison(result_a, result_b, days, 
                       "Task 1a: DAU Comparison - Which variant has most DAU after 15 days?", 
                       "task1/graphs/task1a_dau_comparison_15days.png")


def task1_b():
    """
    Task 1b: 15. günün sonunda A ve B varyantlarının toplam revenue'larını karşılaştır.
    
    Kullanım: Task 1 - Soru b
    """
    print("\n" + "="*60)
    print("TASK 1B: Total Revenue Karşılaştırması (15. Gün)")
    print("="*60)
    
    days = 15
    result_a = simulate_variant(VARIANT_A, days)
    result_b = simulate_variant(VARIANT_B, days)
    
    total_revenue_a = np.sum(result_a['total_revenue'])
    total_revenue_b = np.sum(result_b['total_revenue'])
    
    print(f"\nVariant A - Toplam Revenue (15 gün): ${total_revenue_a:,.2f}")
    print(f"Variant B - Toplam Revenue (15 gün): ${total_revenue_b:,.2f}")
    
    if total_revenue_a > total_revenue_b:
        diff = ((total_revenue_a - total_revenue_b) / total_revenue_b) * 100
        print(f"\nVariant A, Variant B'den %{diff:.2f} daha yüksek revenue'ya sahip.")
    else:
        diff = ((total_revenue_b - total_revenue_a) / total_revenue_a) * 100
        print(f"\nVariant B, Variant A'dan %{diff:.2f} daha yüksek revenue'ya sahip.")
    
    # Grafik oluştur - Task 1b: Which variant will earn the most total money by Day 15?
    plot_cumulative_revenue(result_a, result_b, days, 
                           "Task 1b: Cumulative Revenue - Which variant earns most money by Day 15?", 
                           "task1/graphs/task1b_total_revenue_comparison_15days.png")


def task1_c():
    """
    Task 1c: 30 gün sonra bakarsak seçimimiz değişir mi?
    
    Kullanım: Task 1 - Soru c
    """
    print("\n" + "="*60)
    print("TASK 1C: 30 Gün Sonra Revenue Karşılaştırması")
    print("="*60)
    
    days = 30
    result_a = simulate_variant(VARIANT_A, days)
    result_b = simulate_variant(VARIANT_B, days)
    
    total_revenue_a = np.sum(result_a['total_revenue'])
    total_revenue_b = np.sum(result_b['total_revenue'])
    
    print(f"\nVariant A - Toplam Revenue (30 gün): ${total_revenue_a:,.2f}")
    print(f"Variant B - Toplam Revenue (30 gün): ${total_revenue_b:,.2f}")
    
    if total_revenue_a > total_revenue_b:
        diff = ((total_revenue_a - total_revenue_b) / total_revenue_b) * 100
        print(f"\nVariant A, Variant B'den %{diff:.2f} daha yüksek revenue'ya sahip.")
        print("30 gün sonra da Variant A kazanıyor.")
    else:
        diff = ((total_revenue_b - total_revenue_a) / total_revenue_a) * 100
        print(f"\nVariant B, Variant A'dan %{diff:.2f} daha yüksek revenue'ya sahip.")
        print("30 gün sonra seçim değişti: Variant B kazanıyor.")
    
    # Grafik oluştur - Task 1c: If we look at total money earned by Day 30, does our choice change?
    plot_cumulative_revenue(result_a, result_b, days, 
                           "Task 1c: Cumulative Revenue - Does choice change at Day 30?", 
                           "task1/graphs/task1c_revenue_comparison_30days.png")


def task1_d():
    """
    Task 1d: 15. günden itibaren 10 günlük sale (purchase rate %1 artışı).
    Bu sale hangi varyantın 30. güne kadar daha fazla para kazanmasını sağlar?
    
    Kullanım: Task 1 - Soru d
    """
    print("\n" + "="*60)
    print("TASK 1D: 10 Günlük Sale Senaryosu (15-24. Günler)")
    print("="*60)
    
    days = 30
    sale_start_day = 15
    sale_duration = 10
    purchase_rate_boost = 0.01  # %1 absolute artış (3.05% -> 4.05%, 3.15% -> 4.15%)
    
    # Önce normal simülasyonları yap (karşılaştırma için)
    result_a_normal = simulate_variant(VARIANT_A, days)
    result_b_normal = simulate_variant(VARIANT_B, days)
    total_revenue_a_normal = np.sum(result_a_normal['total_revenue'])
    total_revenue_b_normal = np.sum(result_b_normal['total_revenue'])
    
    # Sale ile simülasyonlar
    result_a_sale = simulate_variant(VARIANT_A, days)
    result_b_sale = simulate_variant(VARIANT_B, days)
    
    # Sale günlerinde (15-24) purchase ratio'yu %1 artır
    for day in range(sale_start_day - 1, min(sale_start_day - 1 + sale_duration, days)):
        dau_a = result_a_sale['dau'][day]
        dau_b = result_b_sale['dau'][day]
        
        # Purchase ratio'yu %1 absolute artır
        purchase_ratio_a_sale = VARIANT_A.daily_purchase_ratio + purchase_rate_boost
        purchase_ratio_b_sale = VARIANT_B.daily_purchase_ratio + purchase_rate_boost
        
        # Revenue'yu yeniden hesapla
        revenue_info_a = calculate_revenue(
            dau=np.array([dau_a]),
            daily_purchase_ratio=purchase_ratio_a_sale,
            ecpm=VARIANT_A.ecpm,
            ad_impressions_per_dau=VARIANT_A.ad_impressions_per_dau,
            average_purchase_amount=VARIANT_A.average_purchase_amount
        )
        revenue_info_b = calculate_revenue(
            dau=np.array([dau_b]),
            daily_purchase_ratio=purchase_ratio_b_sale,
            ecpm=VARIANT_B.ecpm,
            ad_impressions_per_dau=VARIANT_B.ad_impressions_per_dau,
            average_purchase_amount=VARIANT_B.average_purchase_amount
        )
        
        result_a_sale['iap_revenue'][day] = revenue_info_a['iap_revenue'][0]
        result_a_sale['ad_revenue'][day] = revenue_info_a['ad_revenue'][0]
        result_a_sale['total_revenue'][day] = revenue_info_a['total_revenue'][0]
        
        result_b_sale['iap_revenue'][day] = revenue_info_b['iap_revenue'][0]
        result_b_sale['ad_revenue'][day] = revenue_info_b['ad_revenue'][0]
        result_b_sale['total_revenue'][day] = revenue_info_b['total_revenue'][0]
    
    total_revenue_a_sale = np.sum(result_a_sale['total_revenue'])
    total_revenue_b_sale = np.sum(result_b_sale['total_revenue'])
    
    print(f"\nNormal Senaryo (30 gün):")
    print(f"  Variant A: ${total_revenue_a_normal:,.2f}")
    print(f"  Variant B: ${total_revenue_b_normal:,.2f}")
    winner_normal = "A" if total_revenue_a_normal > total_revenue_b_normal else "B"
    
    print(f"\nSale Senaryosu (30 gün, 15-24. günlerde %1 purchase rate artışı):")
    print(f"  Variant A: ${total_revenue_a_sale:,.2f}")
    print(f"  Variant B: ${total_revenue_b_sale:,.2f}")
    
    if total_revenue_a_sale > total_revenue_b_sale:
        diff = ((total_revenue_a_sale - total_revenue_b_sale) / total_revenue_b_sale) * 100
        winner_sale = "A"
        print(f"\nSale ile Variant A, Variant B'den %{diff:.2f} daha yüksek revenue'ya sahip.")
    else:
        diff = ((total_revenue_b_sale - total_revenue_a_sale) / total_revenue_a_sale) * 100
        winner_sale = "B"
        print(f"\nSale ile Variant B, Variant A'dan %{diff:.2f} daha yüksek revenue'ya sahip.")
    
    if winner_normal != winner_sale:
        print(f"\nSONUÇ: Sale ile kazanan varyant değişti! Normal: Variant {winner_normal}, Sale: Variant {winner_sale}")
    else:
        print(f"\nSONUÇ: Sale ile kazanan varyant değişmedi. Her iki durumda da Variant {winner_sale} kazanıyor.")
    
    # Grafik oluştur - Task 1d: What if we run a 10-day sale starting on Day 15?
    plot_cumulative_revenue(result_a_sale, result_b_sale, days, 
                           "Task 1d: Cumulative Revenue with 10-day Sale (Day 15-24)", 
                           "task1/graphs/task1d_sale_scenario_30days.png")


def task1_e():
    """
    Task 1e: 20. günde yeni kullanıcı kaynağı ekleniyor.
    20. günden itibaren her gün: orijinal kaynaktan 12,000, yeni kaynaktan 8,000 kullanıcı geliyor.
    Yeni kullanıcılar için retention formülleri:
    - Variant A (New): Retention = 0.58 * e^(-0.12(x-1))
    - Variant B (New): Retention = 0.52 * e^(-0.10(x-1))
    30. güne kadar hangi varyant daha fazla para kazanır?
    
    Kullanım: Task 1 - Soru e
    """
    print("\n" + "="*60)
    print("TASK 1E: Yeni Kullanıcı Kaynağı Senaryosu (20. Günden İtibaren)")
    print("="*60)
    
    days = 30
    new_source_start_day = 20
    # İlk 19 gün: Her gün 20K kullanıcı (tek kaynak, eski retention)
    # 20. günden itibaren: Her gün 12K eski kaynak + 8K yeni kaynak = 20K toplam
    daily_new_users_old = 12000  # 20. günden itibaren eski kaynaktan
    daily_new_users_new = 8000   # 20. günden itibaren yeni kaynaktan
    daily_new_users_before = 20000  # İlk 19 gün (tek kaynak)
    
    # Retention modelleri ve fonksiyonları
    retention_model_a_old = RetentionModel(VARIANT_A.retention_points)
    retention_model_b_old = RetentionModel(VARIANT_B.retention_points)
    
    def retention_a_new(day: int) -> float:
        return exponential_retention(day, 0.58, 0.12)
    
    def retention_b_new(day: int) -> float:
        return exponential_retention(day, 0.52, 0.10)
    
    # DAU hesapla
    dau_a = calculate_dau_with_mixed_sources(
        retention_model_old=retention_model_a_old,
        retention_func_new=retention_a_new,
        daily_new_users_old=daily_new_users_old,
        daily_new_users_new=daily_new_users_new,
        days=days,
        new_source_start_day=new_source_start_day,
        daily_new_users_before_new_source=daily_new_users_before
    )
    
    dau_b = calculate_dau_with_mixed_sources(
        retention_model_old=retention_model_b_old,
        retention_func_new=retention_b_new,
        daily_new_users_old=daily_new_users_old,
        daily_new_users_new=daily_new_users_new,
        days=days,
        new_source_start_day=new_source_start_day,
        daily_new_users_before_new_source=daily_new_users_before
    )
    
    # Revenue hesapla
    revenue_info_a = calculate_revenue(
        dau=dau_a,
        daily_purchase_ratio=VARIANT_A.daily_purchase_ratio,
        ecpm=VARIANT_A.ecpm,
        ad_impressions_per_dau=VARIANT_A.ad_impressions_per_dau,
        average_purchase_amount=VARIANT_A.average_purchase_amount
    )
    
    revenue_info_b = calculate_revenue(
        dau=dau_b,
        daily_purchase_ratio=VARIANT_B.daily_purchase_ratio,
        ecpm=VARIANT_B.ecpm,
        ad_impressions_per_dau=VARIANT_B.ad_impressions_per_dau,
        average_purchase_amount=VARIANT_B.average_purchase_amount
    )
    
    total_revenue_a = np.sum(revenue_info_a['total_revenue'])
    total_revenue_b = np.sum(revenue_info_b['total_revenue'])
    
    print(f"\nVariant A - Toplam Revenue (30 gün, yeni kaynak ile): ${total_revenue_a:,.2f}")
    print(f"Variant B - Toplam Revenue (30 gün, yeni kaynak ile): ${total_revenue_b:,.2f}")
    
    if total_revenue_a > total_revenue_b:
        diff = ((total_revenue_a - total_revenue_b) / total_revenue_b) * 100
        print(f"\nYeni kaynak ile Variant A, Variant B'den %{diff:.2f} daha yüksek revenue'ya sahip.")
    else:
        diff = ((total_revenue_b - total_revenue_a) / total_revenue_a) * 100
        print(f"\nYeni kaynak ile Variant B, Variant A'dan %{diff:.2f} daha yüksek revenue'ya sahip.")
    
    # Grafik oluştur - Task 1e: On Day 20 we add a new user source
    result_a_dict = {
        'dau': dau_a,
        'total_revenue': revenue_info_a['total_revenue'],
        'iap_revenue': revenue_info_a['iap_revenue'],
        'ad_revenue': revenue_info_a['ad_revenue']
    }
    result_b_dict = {
        'dau': dau_b,
        'total_revenue': revenue_info_b['total_revenue'],
        'iap_revenue': revenue_info_b['iap_revenue'],
        'ad_revenue': revenue_info_b['ad_revenue']
    }
    plot_cumulative_revenue(result_a_dict, result_b_dict, days, 
                           "Task 1e: Cumulative Revenue with New User Source (Day 20+)", 
                           "task1/graphs/task1e_new_user_source_30days.png")


def task1_f():
    """
    Task 1f: Hangisini önceliklendirmeli? (Sadece birini seçebilirsiniz)
    1. Run the temporary 10-day sale (from d)
    2. Add the new, permanent user source (from e)
    
    Hem 30 günlük hem de 60 günlük (2 ay) analiz yaparak karar veriyoruz.
    
    Kullanım: Task 1 - Soru f
    """
    print("\n" + "="*60)
    print("TASK 1F: Önceliklendirme Analizi (30 ve 60 Günlük Karşılaştırma)")
    print("="*60)
    
    days_30 = 30
    days_60 = 60
    
    # Senaryo 1: 10 günlük sale (d'den) - Hem 30 hem 60 gün için hesapla
    sale_start_day = 15
    sale_duration = 10
    purchase_rate_boost = 0.01  # %1 absolute artış
    
    def calculate_sale_revenue(days):
        """
        Sale senaryosunu hem Variant A'ya hem Variant B'ye uygular.
        Her iki varyantın sonuçlarını döndürür ve kazananı belirler.
        """
        result_a_sale = simulate_variant(VARIANT_A, days)
        result_b_sale = simulate_variant(VARIANT_B, days)
        
        for day in range(sale_start_day - 1, min(sale_start_day - 1 + sale_duration, days)):
            dau_a = result_a_sale['dau'][day]
            dau_b = result_b_sale['dau'][day]
            
            purchase_ratio_a_sale = VARIANT_A.daily_purchase_ratio + purchase_rate_boost
            purchase_ratio_b_sale = VARIANT_B.daily_purchase_ratio + purchase_rate_boost
            
            revenue_info_a = calculate_revenue(
                dau=np.array([dau_a]),
                daily_purchase_ratio=purchase_ratio_a_sale,
                ecpm=VARIANT_A.ecpm,
                ad_impressions_per_dau=VARIANT_A.ad_impressions_per_dau,
                average_purchase_amount=VARIANT_A.average_purchase_amount
            )
            revenue_info_b = calculate_revenue(
                dau=np.array([dau_b]),
                daily_purchase_ratio=purchase_ratio_b_sale,
                ecpm=VARIANT_B.ecpm,
                ad_impressions_per_dau=VARIANT_B.ad_impressions_per_dau,
                average_purchase_amount=VARIANT_B.average_purchase_amount
            )
            
            result_a_sale['total_revenue'][day] = revenue_info_a['total_revenue'][0]
            result_b_sale['total_revenue'][day] = revenue_info_b['total_revenue'][0]
        
        total_revenue_sale_a = np.sum(result_a_sale['total_revenue'])
        total_revenue_sale_b = np.sum(result_b_sale['total_revenue'])
        winner_sale = "A" if total_revenue_sale_a > total_revenue_sale_b else "B"
        total_revenue_sale = max(total_revenue_sale_a, total_revenue_sale_b)
        return total_revenue_sale, winner_sale, total_revenue_sale_a, total_revenue_sale_b, result_a_sale, result_b_sale
    
    total_revenue_sale_30, winner_sale_30, revenue_sale_a_30, revenue_sale_b_30, result_sale_a_30, result_sale_b_30 = calculate_sale_revenue(days_30)
    total_revenue_sale_60, winner_sale_60, revenue_sale_a_60, revenue_sale_b_60, result_sale_a_60, result_sale_b_60 = calculate_sale_revenue(days_60)
    
    # Senaryo 2: Yeni kullanıcı kaynağı (e'den) - Hem 30 hem 60 gün için hesapla
    new_source_start_day = 20
    daily_new_users_old = 12000
    daily_new_users_new = 8000
    daily_new_users_before = 20000  # İlk 19 gün
    
    retention_model_a_old = RetentionModel(VARIANT_A.retention_points)
    retention_model_b_old = RetentionModel(VARIANT_B.retention_points)
    
    def retention_a_new(day: int) -> float:
        return exponential_retention(day, 0.58, 0.12)
    
    def retention_b_new(day: int) -> float:
        return exponential_retention(day, 0.52, 0.10)
    
    def calculate_new_source_revenue(days):
        """
        Yeni kullanıcı kaynağı senaryosunu hem Variant A'ya hem Variant B'ye uygular.
        Her iki varyantın sonuçlarını döndürür ve kazananı belirler.
        """
        dau_a_new = calculate_dau_with_mixed_sources(
            retention_model_old=retention_model_a_old,
            retention_func_new=retention_a_new,
            daily_new_users_old=daily_new_users_old,
            daily_new_users_new=daily_new_users_new,
            days=days,
            new_source_start_day=new_source_start_day,
            daily_new_users_before_new_source=daily_new_users_before
        )
        
        dau_b_new = calculate_dau_with_mixed_sources(
            retention_model_old=retention_model_b_old,
            retention_func_new=retention_b_new,
            daily_new_users_old=daily_new_users_old,
            daily_new_users_new=daily_new_users_new,
            days=days,
            new_source_start_day=new_source_start_day,
            daily_new_users_before_new_source=daily_new_users_before
        )
        
        revenue_info_a_new = calculate_revenue(
            dau=dau_a_new,
            daily_purchase_ratio=VARIANT_A.daily_purchase_ratio,
            ecpm=VARIANT_A.ecpm,
            ad_impressions_per_dau=VARIANT_A.ad_impressions_per_dau,
            average_purchase_amount=VARIANT_A.average_purchase_amount
        )
        
        revenue_info_b_new = calculate_revenue(
            dau=dau_b_new,
            daily_purchase_ratio=VARIANT_B.daily_purchase_ratio,
            ecpm=VARIANT_B.ecpm,
            ad_impressions_per_dau=VARIANT_B.ad_impressions_per_dau,
            average_purchase_amount=VARIANT_B.average_purchase_amount
        )
        
        total_revenue_new_source_a = np.sum(revenue_info_a_new['total_revenue'])
        total_revenue_new_source_b = np.sum(revenue_info_b_new['total_revenue'])
        winner_new_source = "A" if total_revenue_new_source_a > total_revenue_new_source_b else "B"
        total_revenue_new_source = max(total_revenue_new_source_a, total_revenue_new_source_b)
        
        result_a_new = {
            'dau': dau_a_new,
            'total_revenue': revenue_info_a_new['total_revenue'],
            'iap_revenue': revenue_info_a_new['iap_revenue'],
            'ad_revenue': revenue_info_a_new['ad_revenue']
        }
        result_b_new = {
            'dau': dau_b_new,
            'total_revenue': revenue_info_b_new['total_revenue'],
            'iap_revenue': revenue_info_b_new['iap_revenue'],
            'ad_revenue': revenue_info_b_new['ad_revenue']
        }
        
        return total_revenue_new_source, winner_new_source, total_revenue_new_source_a, total_revenue_new_source_b, result_a_new, result_b_new
    
    total_revenue_new_source_30, winner_new_source_30, revenue_new_a_30, revenue_new_b_30, result_new_a_30, result_new_b_30 = calculate_new_source_revenue(days_30)
    total_revenue_new_source_60, winner_new_source_60, revenue_new_a_60, revenue_new_b_60, result_new_a_60, result_new_b_60 = calculate_new_source_revenue(days_60)
    
    # Karşılaştırma - 30 Günlük Analiz
    print("\n" + "="*60)
    print("30 GÜNLÜK ANALİZ")
    print("="*60)
    print("\n1. Temporary 10-day Sale (15-24. günler, purchase rate %1 artışı):")
    print(f"   Variant A Revenue: ${revenue_sale_a_30:,.2f}")
    print(f"   Variant B Revenue: ${revenue_sale_b_30:,.2f}")
    print(f"   Kazanan Varyant: {winner_sale_30} (${total_revenue_sale_30:,.2f})")
    
    print("\n2. New Permanent User Source (20. günden itibaren, 12K + 8K kullanıcı):")
    print(f"   Variant A Revenue: ${revenue_new_a_30:,.2f}")
    print(f"   Variant B Revenue: ${revenue_new_b_30:,.2f}")
    print(f"   Kazanan Varyant: {winner_new_source_30} (${total_revenue_new_source_30:,.2f})")
    
    print("\n" + "-" * 60)
    if total_revenue_sale_30 > total_revenue_new_source_30:
        diff_30 = ((total_revenue_sale_30 - total_revenue_new_source_30) / total_revenue_new_source_30) * 100
        print(f"30 Gün Sonuç: Sale senaryosu %{diff_30:.2f} daha fazla revenue üretiyor.")
    else:
        diff_30 = ((total_revenue_new_source_30 - total_revenue_sale_30) / total_revenue_sale_30) * 100
        print(f"30 Gün Sonuç: Yeni kaynak senaryosu %{diff_30:.2f} daha fazla revenue üretiyor.")
    
    # Karşılaştırma - 60 Günlük Analiz
    print("\n" + "="*60)
    print("60 GÜNLÜK ANALİZ (2 AY)")
    print("="*60)
    print("\n1. Temporary 10-day Sale (15-24. günler, purchase rate %1 artışı):")
    print(f"   Variant A Revenue: ${revenue_sale_a_60:,.2f}")
    print(f"   Variant B Revenue: ${revenue_sale_b_60:,.2f}")
    print(f"   Kazanan Varyant: {winner_sale_60} (${total_revenue_sale_60:,.2f})")
    
    print("\n2. New Permanent User Source (20. günden itibaren, 12K + 8K kullanıcı):")
    print(f"   Variant A Revenue: ${revenue_new_a_60:,.2f}")
    print(f"   Variant B Revenue: ${revenue_new_b_60:,.2f}")
    print(f"   Kazanan Varyant: {winner_new_source_60} (${total_revenue_new_source_60:,.2f})")
    
    print("\n" + "-" * 60)
    if total_revenue_sale_60 > total_revenue_new_source_60:
        diff_60 = ((total_revenue_sale_60 - total_revenue_new_source_60) / total_revenue_new_source_60) * 100
        print(f"60 Gün Sonuç: Sale senaryosu %{diff_60:.2f} daha fazla revenue üretiyor.")
    else:
        diff_60 = ((total_revenue_new_source_60 - total_revenue_sale_60) / total_revenue_sale_60) * 100
        print(f"60 Gün Sonuç: Yeni kaynak senaryosu %{diff_60:.2f} daha fazla revenue üretiyor.")
    
    # Final Öneri - 60 günlük analize göre
    print("\n" + "="*60)
    print("TERCİHİM:")
    print("="*60)
    
    # 60 günlük karşılaştırma
    if total_revenue_sale_60 > total_revenue_new_source_60:
        diff_60 = ((total_revenue_sale_60 - total_revenue_new_source_60) / total_revenue_new_source_60) * 100
        winner_60 = "Temporary 10-day Sale"
        print(f"\n60 günlük analiz sonucu: {winner_60} kazanıyor (%{diff_60:.2f} daha fazla revenue)")
    else:
        diff_60 = ((total_revenue_new_source_60 - total_revenue_sale_60) / total_revenue_sale_60) * 100
        winner_60 = "New Permanent User Source"
        print(f"\n60 günlük analiz sonucu: {winner_60} kazanıyor (%{diff_60:.2f} daha fazla revenue)")
    
    # Grafik oluştur - Task 1f: Which one should you prioritize?
    # Her iki seçenek için kazanan varyantların karşılaştırması
    if winner_sale_60 == "A":
        result_sale_winner_60 = result_sale_a_60
    else:
        result_sale_winner_60 = result_sale_b_60
    
    if winner_new_source_60 == "A":
        result_new_source_winner_60 = result_new_a_60
    else:
        result_new_source_winner_60 = result_new_b_60
    
    plot_cumulative_revenue(result_sale_winner_60, result_new_source_winner_60, days_60, 
                           f"Task 1f: Prioritization - Sale (Variant {winner_sale_60}) vs New Source (Variant {winner_new_source_60})", 
                           "task1/graphs/task1f_prioritization_60days.png")


def cleanup_old_graphs():
    """
    Eski grafikleri temizler. Her çalıştırmada yeni grafikler oluşturulur.
    """
    graphs_dir = "task1/graphs"
    
    # Klasör yoksa oluştur
    os.makedirs(graphs_dir, exist_ok=True)
    
    # Tüm PNG dosyalarını bul ve sil
    pattern = os.path.join(graphs_dir, "*.png")
    old_graphs = glob.glob(pattern)
    
    # Alt klasörlerdeki PNG dosyalarını da bul
    pattern_recursive = os.path.join(graphs_dir, "**", "*.png")
    old_graphs.extend(glob.glob(pattern_recursive, recursive=True))
    
    deleted_count = 0
    for graph_file in old_graphs:
        try:
            os.remove(graph_file)
            deleted_count += 1
        except OSError:
            pass
    
    if deleted_count > 0:
        print(f"Eski grafikler temizlendi: {deleted_count} dosya silindi.")


def main():
    """
    Tüm Task 1 sorularını sırasıyla çalıştırır.
    Her çalıştırmada eski grafikleri temizleyip yenilerini oluşturur.
    """
    print("\n" + "="*60)
    print("VERTIGO DATA ANALYST CASE - TASK 1")
    print("="*60)
    
    # Eski grafikleri temizle
    cleanup_old_graphs()
    
    task1_a()
    task1_b()
    task1_c()
    task1_d()
    task1_e()
    task1_f()
    
    print("\n" + "="*60)
    print("TASK 1 TAMAMLANDI - Grafikleri task1/graphs klasöründe görüntüleyebilirsiniz.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

