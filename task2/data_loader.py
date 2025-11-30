# data_loader.py
# Task 2 - Data loading modülü
# -ozgur

"""
Task 2 için dataset yükleme ve preprocessing fonksiyonları.
CSV.gz dosyalarını okur ve birleştirir.
Tarih dönüşümleri ve feature engineering işlemlerini yapar.
"""

import pandas as pd
import glob
import os
from typing import Optional


def load_dataset(data_dir: Optional[str] = None) -> pd.DataFrame:
    """
    Tüm CSV.gz dosyalarını yükler ve birleştirir.
    
    Args:
        data_dir: Dataset klasörünün yolu (None ise script'in bulunduğu dizine göre otomatik bulur)
    
    Returns:
        Birleştirilmiş DataFrame
    
    Kullanım: Task 2 - Dataset yükleme
    """
    # Eğer data_dir verilmemişse, script'in bulunduğu dizine göre bul
    if data_dir is None:
        # Script'in bulunduğu dizin (task2/)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "dataset")
    
    # Dataset klasörünün varlığını kontrol et
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Dataset klasörü bulunamadı: {data_dir}")
    
    # Dataset klasöründeki tüm CSV.gz dosyalarını bul
    pattern = os.path.join(data_dir, "*.csv.gz")
    csv_files = sorted(glob.glob(pattern))
    
    if not csv_files:
        raise FileNotFoundError(f"Dataset klasöründe CSV.gz dosyası bulunamadı: {data_dir}")
    
    print(f"Toplam {len(csv_files)} dosya bulundu. Yükleniyor...")
    
    # Tüm dosyaları oku ve birleştir
    dataframes = []
    for i, file_path in enumerate(csv_files, 1):
        try:
            df = pd.read_csv(file_path, compression='gzip')
            dataframes.append(df)
            if i % 5 == 0 or i == len(csv_files):
                print(f"  {i}/{len(csv_files)} dosya yüklendi...")
        except Exception as e:
            print(f"Uyarı: {file_path} yüklenirken hata oluştu: {e}")
            continue
    
    if not dataframes:
        raise ValueError("Hiçbir dosya yüklenemedi!")
    
    # Tüm DataFrame'leri birleştir
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    print(f"\nDataset yüklendi: {len(combined_df):,} satır, {len(combined_df.columns)} sütun")
    
    return combined_df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Dataset'i preprocessing yapar.
    Tarih sütunlarını datetime'a çevirir ve gerekli hesaplamaları yapar.
    
    Args:
        df: Ham DataFrame
    
    Returns:
        Preprocessed DataFrame
    
    Kullanım: Task 2 - Data preprocessing
    """
    df = df.copy()
    
    # Tarih sütunlarını datetime'a çevir
    if 'event_date' in df.columns:
        df['event_date'] = pd.to_datetime(df['event_date'])
    if 'install_date' in df.columns:
        df['install_date'] = pd.to_datetime(df['install_date'])
    
    # Days since install hesapla
    if 'event_date' in df.columns and 'install_date' in df.columns:
        df['days_since_install'] = (df['event_date'] - df['install_date']).dt.days
    
    # Session başına ortalama süre hesapla
    if 'total_session_count' in df.columns and 'total_session_duration' in df.columns:
        df['avg_session_duration'] = df['total_session_duration'] / df['total_session_count'].replace(0, 1)
    
    # Win rate hesapla
    if 'victory_count' in df.columns and 'defeat_count' in df.columns:
        total_matches = df['victory_count'] + df['defeat_count']
        df['win_rate'] = df['victory_count'] / total_matches.replace(0, 1)
    
    # Total revenue hesapla
    if 'iap_revenue' in df.columns and 'ad_revenue' in df.columns:
        df['total_revenue'] = df['iap_revenue'] + df['ad_revenue']
    
    return df

