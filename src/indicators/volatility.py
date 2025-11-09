"""
Volatilite Göstergeleri

Bu modül volatilite (dalgalanma) bazlı teknik göstergeleri hesaplar:
- Bollinger Bands
- ATR (Average True Range) - gelecekte
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict


def calculate_bollinger_bands(
    data: pd.DataFrame,
    period: int = 20,
    std_dev: float = 2.0,
    column: str = 'Close'
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Bollinger Bands - Bollinger Bantları
    
    Bollinger Bands Nedir?
    ---------------------
    Fiyatın hareketli ortalama etrafındaki standart sapmasını gösteren volatilite göstergesi.
    3 çizgiden oluşur: Orta (SMA), Üst Band, Alt Band
    
    Nasıl Yorumlanır?
    ----------------
    1. Band Daraldığında (Squeeze):
       - Volatilite düşük
       - Büyük hamle gelebilir (patlama beklenir)
    
    2. Band Genişlediğinde:
       - Volatilite yüksek
       - Güçlü trend var
    
    3. Fiyat Pozisyonu:
       - Fiyat Üst Band'a dokundu: Aşırı alım, düzeltme gelebilir
       - Fiyat Alt Band'a dokundu: Aşırı satım, toparlanma gelebilir
       - Fiyat Orta Band üstünde: Yükseliş trendi
       - Fiyat Orta Band altında: Düşüş trendi
    
    4. Band Walk:
       - Fiyat sürekli Üst Band'da: Çok güçlü yükseliş
       - Fiyat sürekli Alt Band'da: Çok güçlü düşüş
    
    Matematiksel Açıklama:
    ---------------------
    Middle Band = SMA(20)
    Upper Band = SMA(20) + (2 * Standard Deviation)
    Lower Band = SMA(20) - (2 * Standard Deviation)
    
    Args:
        data (pd.DataFrame): Fiyat verileri
        period (int): Periyot (genellikle 20)
        std_dev (float): Standart sapma çarpanı (genellikle 2)
        column (str): Hangi sütun kullanılacak
    
    Returns:
        tuple: (upper_band, middle_band, lower_band)
    
    Örnek:
        >>> data = fetch_stock_data('THYAO')
        >>> upper, middle, lower = calculate_bollinger_bands(data)
        >>> current_price = data['Close'].iloc[-1]
        >>> 
        >>> if current_price >= upper.iloc[-1]:
        ...     print("Ust banda dokundu - Asiri alim!")
    """
    
    # Orta Band = Simple Moving Average
    middle_band = data[column].rolling(window=period).mean()
    
    # Standart sapma hesapla
    rolling_std = data[column].rolling(window=period).std()
    
    # Üst ve Alt Bandları hesapla
    upper_band = middle_band + (rolling_std * std_dev)
    lower_band = middle_band - (rolling_std * std_dev)
    
    return upper_band, middle_band, lower_band


def interpret_bollinger_bands(
    price: float,
    upper: float,
    middle: float,
    lower: float,
    prev_price: float = None
) -> Dict[str, any]:
    """
    Bollinger Bands değerlerini yorumlar.
    
    Args:
        price (float): Mevcut fiyat
        upper (float): Üst band
        middle (float): Orta band
        lower (float): Alt band
        prev_price (float): Önceki fiyat (band kesişimi için)
    
    Returns:
        dict: Yorum ve sinyal
    """
    
    if pd.isna(upper) or pd.isna(middle) or pd.isna(lower):
        return {
            'signal': 'HOLD',
            'strength': 0,
            'description': 'Yetersiz veri',
            'position': 'N/A'
        }
    
    # Band genişliği (volatilite)
    band_width = ((upper - lower) / middle) * 100
    
    # Fiyatın banda göre pozisyonu (0-100 arası normalize)
    # 50 = Orta band, 100 = Üst band, 0 = Alt band
    price_position = ((price - lower) / (upper - lower)) * 100
    
    # Sinyal tespiti
    if price_position >= 95:  # Üst banda çok yakın
        signal = 'SELL'
        strength = 70
        position = 'UST BAND - ASIRI ALIM'
        description = f'Fiyat ust banda dokundu ({price:.2f} TL). Duzeltme gelebilir.'
    
    elif price_position <= 5:  # Alt banda çok yakın
        signal = 'BUY'
        strength = 70
        position = 'ALT BAND - ASIRI SATIM'
        description = f'Fiyat alt banda dokundu ({price:.2f} TL). Toparlanma firsati.'
    
    elif price_position > 70:  # Üst bölge
        signal = 'HOLD_SELL'
        strength = 40
        position = 'UST BOLGE'
        description = f'Fiyat ust bolgede ({price:.2f} TL). Dikkatli olun.'
    
    elif price_position < 30:  # Alt bölge
        signal = 'HOLD_BUY'
        strength = 40
        position = 'ALT BOLGE'
        description = f'Fiyat alt bolgede ({price:.2f} TL). Potansiyel firsat.'
    
    elif price > middle:  # Orta üstü
        signal = 'HOLD_BUY'
        strength = 20
        position = 'ORTA UST - YUKSELIS'
        description = f'Fiyat orta bandin ustunde ({price:.2f} TL). Yukselis trendi.'
    
    else:  # Orta altı
        signal = 'HOLD_SELL'
        strength = 20
        position = 'ORTA ALT - DUSUS'
        description = f'Fiyat orta bandin altinda ({price:.2f} TL). Dusus trendi.'
    
    return {
        'signal': signal,
        'strength': int(strength),
        'description': description,
        'position': position,
        'band_width': round(band_width, 2),
        'price_position': round(price_position, 1),
        'upper_band': round(upper, 2),
        'middle_band': round(middle, 2),
        'lower_band': round(lower, 2)
    }


# Test fonksiyonu
if __name__ == "__main__":
    print("=" * 60)
    print("VOLATILITE GOSTERGELERI - TEST")
    print("=" * 60)
    
    from src.data.fetcher import fetch_stock_data
    
    print("\n[TEST] THYAO verisi cekiliyor...")
    data = fetch_stock_data('THYAO', period='3mo')
    
    if data is not None:
        print(f"[OK] {len(data)} gunluk veri cekildi\n")
        
        print("="*60)
        print("[TEST] Bollinger Bands Hesaplama")
        print("="*60)
        
        upper, middle, lower = calculate_bollinger_bands(data)
        current_price = data['Close'].iloc[-1]
        
        print(f"\nSon 5 gun Bollinger Bands:")
        for i in range(-5, 0):
            print(f"  {data.index[i].date()}: Alt={lower.iloc[i]:.2f}, Orta={middle.iloc[i]:.2f}, Ust={upper.iloc[i]:.2f}, Fiyat={data['Close'].iloc[i]:.2f}")
        
        print(f"\n[YORUM] Guncel Durum:")
        bb_interp = interpret_bollinger_bands(
            current_price,
            upper.iloc[-1],
            middle.iloc[-1],
            lower.iloc[-1]
        )
        print(f"  Fiyat: {current_price:.2f} TL")
        print(f"  Sinyal: {bb_interp['signal']}")
        print(f"  Guc: {bb_interp['strength']}/100")
        print(f"  Pozisyon: {bb_interp['position']}")
        print(f"  Band Genisligi: {bb_interp['band_width']:.2f}%")
        print(f"  Aciklama: {bb_interp['description']}")
        
        print("\n" + "="*60)
        print("[OK] TEST TAMAMLANDI!")
        print("="*60)
    else:
        print("[HATA] Veri cekilemedi")

