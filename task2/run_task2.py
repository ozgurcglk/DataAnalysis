# run_task2.py
# Task 2 - Ana çalıştırma scripti - Kodu buradan çalıştırabilirsiniz.
# -ozgur

"""
Task 2 için exploratory data analysis scripti.
Tüm analizleri çalıştırır ve görselleştirmeleri oluşturur.
"""

from data_loader import load_dataset, preprocess_data
from analysis import (
    segment_users_by_first_day_engagement,
    analyze_session_duration_trends,
    analyze_retention_by_segment,
    analyze_monetization_segments,
    analyze_match_completion_trends,
    analyze_platform_country_comparison,
    analyze_win_rate_trends
)
from visualization import (
    plot_segment_distribution,
    plot_session_duration_trends,
    plot_retention_by_segment,
    plot_monetization_segments,
    plot_match_completion_trends,
    plot_platform_country_comparison,
    plot_win_rate_trends
)
import os
import glob


def cleanup_old_graphs():
    """
    Eski grafikleri temizler. Her çalıştırmada yeni grafikler oluşturulur.
    """
    graphs_dir = "task2/graphs"
    
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


def analysis_1_first_day_engagement(df):
    """
    Analiz 1: First-day engagement bazlı user segmentation.
    
    Kullanım: Task 2 - First-day engagement segmentation
    """
    print("\n" + "="*60)
    print("ANALİZ 1: First-Day Engagement Segmentation")
    print("="*60)
    
    user_segments = segment_users_by_first_day_engagement(df)
    
    # Segment istatistikleri
    segment_stats = user_segments['segment'].value_counts()
    print("\nSegment Dağılımı:")
    for segment, count in segment_stats.items():
        percentage = (count / len(user_segments)) * 100
        print(f"  {segment}: {count:,} kullanıcı ({percentage:.2f}%)")
    
    # Grafik oluştur
    plot_segment_distribution(
        user_segments,
        "task2/graphs/task2_first_day_engagement_segmentation.png"
    )
    
    return user_segments


def analysis_2_session_duration_trends(df):
    """
    Analiz 2: Session duration trendleri analizi.
    
    Kullanım: Task 2 - Session duration trends
    """
    print("\n" + "="*60)
    print("ANALİZ 2: Session Duration Trends")
    print("="*60)
    
    trend_data = analyze_session_duration_trends(df)
    
    # Günlük trend özeti
    daily_trend = trend_data['daily_trend']
    print(f"\nGünlük Ortalama Session Duration:")
    print(f"  İlk gün: {daily_trend['avg_session_duration'].iloc[0]:.2f} saniye")
    print(f"  Son gün: {daily_trend['avg_session_duration'].iloc[-1]:.2f} saniye")
    print(f"  Ortalama: {daily_trend['avg_session_duration'].mean():.2f} saniye")
    
    # Kullanıcı lifetime'ına göre trend özeti (days since install)
    lifetime_trend = trend_data['lifetime_trend']
    print(f"\nDays Since Install'a Göre Session Duration:")
    print(f"  Day 0: {lifetime_trend[lifetime_trend['days_since_install'] == 0]['avg_session_duration'].values[0]:.2f} saniye")
    print(f"  Day 7: {lifetime_trend[lifetime_trend['days_since_install'] == 7]['avg_session_duration'].values[0] if len(lifetime_trend[lifetime_trend['days_since_install'] == 7]) > 0 else 'N/A'}")
    print(f"  Day 14: {lifetime_trend[lifetime_trend['days_since_install'] == 14]['avg_session_duration'].values[0] if len(lifetime_trend[lifetime_trend['days_since_install'] == 14]) > 0 else 'N/A'}")
    
    # Grafik oluştur
    plot_session_duration_trends(
        trend_data,
        "task2/graphs/task2_session_duration_trends.png"
    )
    
    return trend_data


def analysis_3_retention_by_segment(df, user_segments):
    """
    Analiz 3: Segment bazlı retention analizi.
    
    Kullanım: Task 2 - Retention analysis by segment
    """
    print("\n" + "="*60)
    print("ANALİZ 3: Retention Analysis by Engagement Segment")
    print("="*60)
    
    retention_df = analyze_retention_by_segment(df, user_segments)
    
    # Her segment için retention özeti
    segments = retention_df['segment'].unique()
    print("\nSegment Bazlı Retention Oranları:")
    for segment in segments:
        segment_retention = retention_df[retention_df['segment'] == segment]
        print(f"\n  {segment}:")
        print(f"    Day 1: {segment_retention[segment_retention['day'] == 1]['retention_rate'].values[0] * 100:.2f}%")
        print(f"    Day 7: {segment_retention[segment_retention['day'] == 7]['retention_rate'].values[0] * 100:.2f}%" if len(segment_retention[segment_retention['day'] == 7]) > 0 else "    Day 7: N/A")
        print(f"    Day 14: {segment_retention[segment_retention['day'] == 14]['retention_rate'].values[0] * 100:.2f}%" if len(segment_retention[segment_retention['day'] == 14]) > 0 else "    Day 14: N/A")
    
    # Grafik oluştur
    plot_retention_by_segment(
        retention_df,
        "task2/graphs/task2_retention_by_segment.png"
    )
    
    return retention_df


def analysis_4_monetization_segments(df):
    """
    Analiz 4: Monetization segmentasyonu.
    
    Kullanım: Task 2 - Monetization segmentation
    """
    print("\n" + "="*60)
    print("ANALİZ 4: Monetization Segmentation")
    print("="*60)
    
    monetization_df = analyze_monetization_segments(df)
    
    # Segment istatistikleri
    segment_stats = monetization_df['monetization_segment'].value_counts()
    print("\nMonetization Segment Dağılımı:")
    for segment, count in segment_stats.items():
        percentage = (count / len(monetization_df)) * 100
        avg_revenue = monetization_df[monetization_df['monetization_segment'] == segment]['total_revenue'].mean()
        print(f"  {segment}: {count:,} kullanıcı ({percentage:.2f}%) - Ortalama Revenue: ${avg_revenue:.2f}")
    
    # Grafik oluştur
    plot_monetization_segments(
        monetization_df,
        "task2/graphs/task2_monetization_segmentation.png"
    )
    
    return monetization_df


def analysis_5_match_completion_trends(df):
    """
    Analiz 5: Match completion rate trendleri.
    
    Kullanım: Task 2 - Match completion trends
    """
    print("\n" + "="*60)
    print("ANALİZ 5: Match Completion Trends")
    print("="*60)
    
    completion_data = analyze_match_completion_trends(df)
    
    # Günlük trend özeti
    daily_trend = completion_data['daily_trend']
    print(f"\nGünlük Match Completion Rate:")
    print(f"  Ortalama: {daily_trend['completion_rate'].mean() * 100:.2f}%")
    print(f"  Min: {daily_trend['completion_rate'].min() * 100:.2f}%")
    print(f"  Max: {daily_trend['completion_rate'].max() * 100:.2f}%")
    
    # Kullanıcı lifetime'ına göre trend (days since install)
    lifetime_trend = completion_data['lifetime_trend']
    print(f"\nDays Since Install'a Göre Completion Rate:")
    print(f"  Day 0: {lifetime_trend[lifetime_trend['days_since_install'] == 0]['completion_rate'].values[0] * 100:.2f}%")
    print(f"  Day 7: {lifetime_trend[lifetime_trend['days_since_install'] == 7]['completion_rate'].values[0] * 100:.2f}%" if len(lifetime_trend[lifetime_trend['days_since_install'] == 7]) > 0 else "  Day 7: N/A")
    
    # Grafik oluştur
    plot_match_completion_trends(
        completion_data,
        "task2/graphs/task2_match_completion_trends.png"
    )
    
    return completion_data


def analysis_6_platform_country_comparison(df):
    """
    Analiz 6: Platform ve country karşılaştırması.
    
    Kullanım: Task 2 - Platform and country comparison
    """
    print("\n" + "="*60)
    print("ANALİZ 6: Platform and Country Comparison")
    print("="*60)
    
    comparison_data = analyze_platform_country_comparison(df)
    
    # Platform istatistikleri
    platform_stats = comparison_data['platform_stats']
    print("\nPlatform İstatistikleri:")
    for _, row in platform_stats.iterrows():
        print(f"\n  {row['platform']}:")
        print(f"    Unique Users: {row['user_id']:,}")
        print(f"    Avg Session Duration: {row['total_session_duration']:.2f} saniye")
        print(f"    Total Revenue: ${row['total_revenue']:,.2f}")
        print(f"    Win Rate: {row['win_rate'] * 100:.2f}%")
    
    # Top 5 Country istatistikleri
    country_stats = comparison_data['country_stats'].head(5)
    print("\nTop 5 Country İstatistikleri:")
    for _, row in country_stats.iterrows():
        print(f"\n  {row['country']}:")
        print(f"    Unique Users: {row['user_id']:,}")
        print(f"    Total Revenue: ${row['total_revenue']:,.2f}")
    
    # Grafik oluştur
    plot_platform_country_comparison(
        comparison_data,
        "task2/graphs/task2_platform_country_comparison.png"
    )
    
    return comparison_data


def analysis_7_win_rate_trends(df):
    """
    Analiz 7: Win rate trendleri.
    
    Kullanım: Task 2 - Win rate trends
    """
    print("\n" + "="*60)
    print("ANALİZ 7: Win Rate Trends")
    print("="*60)
    
    win_rate_data = analyze_win_rate_trends(df)
    
    # Günlük trend özeti
    daily_trend = win_rate_data['daily_trend']
    print(f"\nGünlük Win Rate:")
    print(f"  Ortalama: {daily_trend['overall_win_rate'].mean() * 100:.2f}%")
    print(f"  Min: {daily_trend['overall_win_rate'].min() * 100:.2f}%")
    print(f"  Max: {daily_trend['overall_win_rate'].max() * 100:.2f}%")
    
    # Kullanıcı lifetime'ına göre trend (days since install)
    lifetime_trend = win_rate_data['lifetime_trend']
    print(f"\nDays Since Install'a Göre Win Rate:")
    print(f"  Day 0: {lifetime_trend[lifetime_trend['days_since_install'] == 0]['overall_win_rate'].values[0] * 100:.2f}%")
    print(f"  Day 7: {lifetime_trend[lifetime_trend['days_since_install'] == 7]['overall_win_rate'].values[0] * 100:.2f}%" if len(lifetime_trend[lifetime_trend['days_since_install'] == 7]) > 0 else "  Day 7: N/A")
    print(f"  Day 14: {lifetime_trend[lifetime_trend['days_since_install'] == 14]['overall_win_rate'].values[0] * 100:.2f}%" if len(lifetime_trend[lifetime_trend['days_since_install'] == 14]) > 0 else "  Day 14: N/A")
    
    # Grafik oluştur
    plot_win_rate_trends(
        win_rate_data,
        "task2/graphs/task2_win_rate_trends.png"
    )
    
    return win_rate_data


def main():
    """
    Tüm Task 2 analizlerini sırasıyla çalıştırır.
    """
    print("\n" + "="*60)
    print("VERTIGO DATA ANALYST CASE - TASK 2")
    print("="*60)
    
    # Eski grafikleri temizle
    cleanup_old_graphs()
    
    # Dataset'i yükle ve preprocess et
    print("\nDataset yükleniyor...")
    df = load_dataset()  # Otomatik olarak task2/dataset klasörünü bulur
    df = preprocess_data(df)
    
    print(f"\nDataset hazır: {len(df):,} satır")
    print(f"Tarih aralığı: {df['event_date'].min()} - {df['event_date'].max()}")
    print(f"Unique kullanıcı sayısı: {df['user_id'].nunique():,}")
    
    # Analizleri çalıştır
    user_segments = analysis_1_first_day_engagement(df)
    session_trends = analysis_2_session_duration_trends(df)
    retention_analysis = analysis_3_retention_by_segment(df, user_segments)
    monetization_segments = analysis_4_monetization_segments(df)
    completion_trends = analysis_5_match_completion_trends(df)
    platform_country = analysis_6_platform_country_comparison(df)
    win_rate_trends = analysis_7_win_rate_trends(df)
    
    print("\n" + "="*60)
    print("TASK 2 TAMAMLANDI - Grafikleri task2/graphs klasöründe görüntüleyebilirsiniz.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

