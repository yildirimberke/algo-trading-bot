"""
Momentum Göstergeleri

Bu modül momentum bazlı teknik göstergeleri hesaplar:
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Stochastic Oscillator (gelecekte)
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict


def calculate_rsi(data: pd.DataFrame, period: int = 14, column: str = 'Close') -> pd.Series:
    """
    RSI (Relative Strength Index) - Göreceli Güç Endeksi
    
    RSI Nedir?
    ---------
    RSI, fiyatların ne kadar hızlı yükselip düştüğünü ölçen momentum göstergesidir.
    0-100 arasında değer alır.
    
    Nasıl Yorumlanır?
    ----------------
    - RSI > 70: Aşırı Alım Bölgesi (Overbought) - Düşüş gelebilir
    - RSI < 30: Aşırı Satım Bölgesi (Oversold) - Yükseliş gelebilir
    - RSI = 50: Nötr bölge
    - RSI yukarı kesiyor 30'u: AL sinyali
    - RSI aşağı kesiyor 70'i: SAT sinyali
    
    Matematiksel Açıklama:
    ---------------------
    RSI = 100 - (100 / (1 + RS))
    RS = Ortalama Kazanç / Ortalama Kayıp (son N periyod)
    
    Args:
        data (pd.DataFrame): Fiyat verileri
        period (int): RSI periyodu (genellikle 14)
        column (str): Hangi sütun kullanılacak (genellikle 'Close')
    
    Returns:
        pd.Series: RSI değerleri
    
    Örnek:
        >>> from src.data.fetcher import fetch_stock_data
        >>> data = fetch_stock_data('THYAO', period='6mo')
        >>> rsi = calculate_rsi(data)
        >>> print(f"Guncel RSI: {rsi.iloc[-1]:.2f}")
    
    Notlar:
        - İlk N satırda NaN olacaktır (yeterli veri yok)
        - Wilder's smoothing methodu kullanılır
        - Kısa periyot (7) daha volatil, uzun periyot (21) daha smooth
    """
    
    # Fiyat değişimlerini hesapla
    delta = data[column].diff()
    
    # Kazanç ve kayıpları ayır
    gain = delta.where(delta > 0, 0)  # Pozitif değişimler
    loss = -delta.where(delta < 0, 0)  # Negatif değişimler (pozitif yapıyoruz)
    
    # Wilder's Smoothing (EMA benzeri ama farklı)
    # İlk N günün ortalamasını al
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    
    # Sonraki günler için smoothing uygula
    for i in range(period, len(data)):
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (period - 1) + loss.iloc[i]) / period
    
    # RS (Relative Strength) hesapla
    rs = avg_gain / avg_loss
    
    # RSI hesapla
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(
    data: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
    column: str = 'Close'
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    MACD (Moving Average Convergence Divergence)
    
    MACD Nedir?
    ----------
    Hızlı ve yavaş hareketli ortalamaların arasındaki farkı gösteren trend takip göstergesi.
    Momentum ve trend yönünü birlikte gösterir.
    
    Nasıl Yorumlanır?
    ----------------
    1. MACD Çizgisi:
       - MACD > 0: Yükseliş trendi
       - MACD < 0: Düşüş trendi
    
    2. Sinyal Çizgisi Kesişimi:
       - MACD yukarı keser Signal'i: GÜÇLÜ AL sinyali (Bullish Crossover)
       - MACD aşağı keser Signal'i: GÜÇLÜ SAT sinyali (Bearish Crossover)
    
    3. Histogram:
       - Histogram > 0 ve artıyor: Yükseliş güçleniyor
       - Histogram < 0 ve azalıyor: Düşüş güçleniyor
       - Histogram sıfıra yaklaşıyor: Momentum zayıflıyor
    
    4. Divergence (Uyumsuzluk):
       - Fiyat yükseliyor ama MACD düşüyor: UYARI, düzeltme gelebilir
       - Fiyat düşüyor ama MACD yükseliyor: Toparlanma sinyali
    
    Matematiksel Açıklama:
    ---------------------
    MACD Line = EMA(12) - EMA(26)
    Signal Line = EMA(MACD, 9)
    Histogram = MACD Line - Signal Line
    
    Args:
        data (pd.DataFrame): Fiyat verileri
        fast (int): Hızlı EMA periyodu (genellikle 12)
        slow (int): Yavaş EMA periyodu (genellikle 26)
        signal (int): Sinyal çizgisi periyodu (genellikle 9)
        column (str): Hangi sütun kullanılacak
    
    Returns:
        tuple: (macd_line, signal_line, histogram)
    
    Örnek:
        >>> data = fetch_stock_data('THYAO')
        >>> macd, signal, histogram = calculate_macd(data)
        >>> 
        >>> # Kesişim kontrolü (AL/SAT sinyali)
        >>> if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] < signal.iloc[-2]:
        ...     print("BULLISH CROSSOVER - AL sinyali!")
    
    Notlar:
        - İlk 26+9=35 günde yeterli veri olmayabilir
        - Pozitif histogram = MACD sinyal üstünde = güçlü
        - Trend piyasalarda çok iyi çalışır
    """
    
    # EMA (Exponential Moving Average) hesapla
    ema_fast = data[column].ewm(span=fast, adjust=False).mean()
    ema_slow = data[column].ewm(span=slow, adjust=False).mean()
    
    # MACD Line = Hızlı EMA - Yavaş EMA
    macd_line = ema_fast - ema_slow
    
    # Signal Line = MACD'nin 9 günlük EMA'sı
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    
    # Histogram = MACD - Signal
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def interpret_rsi(rsi_value: float) -> Dict[str, any]:
    """
    RSI değerini yorumlar ve sinyal üretir.
    
    Args:
        rsi_value (float): Mevcut RSI değeri
    
    Returns:
        dict: Yorum ve sinyal bilgisi
    
    Örnek:
        >>> rsi = calculate_rsi(data).iloc[-1]
        >>> result = interpret_rsi(rsi)
        >>> print(result['signal'])  # 'BUY', 'SELL', 'HOLD'
        >>> print(result['description'])
    """
    
    if pd.isna(rsi_value):
        return {
            'signal': 'HOLD',
            'strength': 0,
            'description': 'Yetersiz veri',
            'zone': 'N/A'
        }
    
    # Bölge tespiti
    if rsi_value >= 70:
        zone = 'ASIRI ALIM'
        signal = 'SELL'
        strength = min(100, (rsi_value - 70) * 3)  # 70-80 arası 0-30 puan
    elif rsi_value <= 30:
        zone = 'ASIRI SATIM'
        signal = 'BUY'
        strength = min(100, (30 - rsi_value) * 3)  # 30-20 arası 0-30 puan
    elif rsi_value > 55:
        zone = 'YUKSELIS EGILIMI'
        signal = 'HOLD_BUY'
        strength = (rsi_value - 50) * 2
    elif rsi_value < 45:
        zone = 'DUSUS EGILIMI'
        signal = 'HOLD_SELL'
        strength = (50 - rsi_value) * 2
    else:
        zone = 'NOTR'
        signal = 'HOLD'
        strength = 0
    
    # Açıklama oluştur
    descriptions = {
        'ASIRI ALIM': f'RSI {rsi_value:.1f} - Asiri alim bolgesinde, duzeltme gelebilir.',
        'ASIRI SATIM': f'RSI {rsi_value:.1f} - Asiri satim bolgesinde, yukselis firsati.',
        'YUKSELIS EGILIMI': f'RSI {rsi_value:.1f} - Yukselis egilimli, pozitif momentum.',
        'DUSUS EGILIMI': f'RSI {rsi_value:.1f} - Dusus egilimli, negatif momentum.',
        'NOTR': f'RSI {rsi_value:.1f} - Notr bolgede, net sinyal yok.'
    }
    
    return {
        'signal': signal,
        'strength': int(strength),
        'description': descriptions[zone],
        'zone': zone,
        'value': round(rsi_value, 2)
    }


def interpret_macd(macd: float, signal: float, histogram: float, 
                   prev_macd: float = None, prev_signal: float = None) -> Dict[str, any]:
    """
    MACD değerlerini yorumlar ve sinyal üretir.
    
    Args:
        macd (float): Mevcut MACD değeri
        signal (float): Mevcut Signal değeri
        histogram (float): Mevcut Histogram değeri
        prev_macd (float): Önceki MACD (kesişim tespiti için)
        prev_signal (float): Önceki Signal (kesişim tespiti için)
    
    Returns:
        dict: Yorum ve sinyal bilgisi
    """
    
    if pd.isna(macd) or pd.isna(signal):
        return {
            'signal': 'HOLD',
            'strength': 0,
            'description': 'Yetersiz veri',
            'crossover': None
        }
    
    # Kesişim kontrolü
    crossover = None
    crossover_strength = 0
    
    if prev_macd is not None and prev_signal is not None:
        # Bullish Crossover (Yukarı kesişim - AL sinyali)
        if macd > signal and prev_macd <= prev_signal:
            crossover = 'BULLISH'
            crossover_strength = 80  # Güçlü sinyal
            signal_type = 'BUY'
        # Bearish Crossover (Aşağı kesişim - SAT sinyali)
        elif macd < signal and prev_macd >= prev_signal:
            crossover = 'BEARISH'
            crossover_strength = 80  # Güçlü sinyal
            signal_type = 'SELL'
        # Kesişim yok
        elif macd > signal:
            signal_type = 'HOLD_BUY'
            crossover_strength = min(50, abs(histogram) * 10)
        else:
            signal_type = 'HOLD_SELL'
            crossover_strength = min(50, abs(histogram) * 10)
    else:
        # Sadece mevcut durum
        if macd > signal:
            signal_type = 'HOLD_BUY'
            crossover_strength = min(50, abs(histogram) * 10)
        else:
            signal_type = 'HOLD_SELL'
            crossover_strength = min(50, abs(histogram) * 10)
    
    # Açıklama oluştur
    if crossover == 'BULLISH':
        description = f'MACD pozitif kesisme! GUCLU AL sinyali (Histogram: {histogram:.2f})'
    elif crossover == 'BEARISH':
        description = f'MACD negatif kesisme! GUCLU SAT sinyali (Histogram: {histogram:.2f})'
    elif macd > 0 and signal > 0:
        description = f'MACD pozitif bolgede, yukselis trendi devam ediyor'
    elif macd < 0 and signal < 0:
        description = f'MACD negatif bolgede, dusus trendi devam ediyor'
    else:
        description = f'MACD notr bolgede'
    
    return {
        'signal': signal_type,
        'strength': int(crossover_strength),
        'description': description,
        'crossover': crossover,
        'macd_value': round(macd, 4),
        'signal_value': round(signal, 4),
        'histogram_value': round(histogram, 4)
    }


# Test fonksiyonu
if __name__ == "__main__":
    print("=" * 60)
    print("MOMENTUM GOSTERGELERI - TEST")
    print("=" * 60)
    
    from src.data.fetcher import fetch_stock_data
    
    # Test verisi çek
    print("\n[TEST] THYAO verisi cekiliyor...")
    data = fetch_stock_data('THYAO', period='6mo')
    
    if data is not None:
        print(f"[OK] {len(data)} gunluk veri cekildi\n")
        
        # RSI hesapla
        print("="*60)
        print("[TEST 1] RSI Hesaplama")
        print("="*60)
        
        rsi = calculate_rsi(data)
        current_rsi = rsi.iloc[-1]
        
        print(f"\nSon 5 gun RSI degerleri:")
        for i in range(-5, 0):
            print(f"  {data.index[i].date()}: RSI = {rsi.iloc[i]:.2f}")
        
        print(f"\n[YORUM] Guncel RSI: {current_rsi:.2f}")
        rsi_interp = interpret_rsi(current_rsi)
        print(f"  Sinyal: {rsi_interp['signal']}")
        print(f"  Guc: {rsi_interp['strength']}/100")
        print(f"  Bolge: {rsi_interp['zone']}")
        print(f"  Aciklama: {rsi_interp['description']}")
        
        # MACD hesapla
        print("\n" + "="*60)
        print("[TEST 2] MACD Hesaplama")
        print("="*60)
        
        macd_line, signal_line, histogram = calculate_macd(data)
        
        print(f"\nSon 5 gun MACD degerleri:")
        for i in range(-5, 0):
            print(f"  {data.index[i].date()}: MACD={macd_line.iloc[i]:.3f}, Signal={signal_line.iloc[i]:.3f}, Hist={histogram.iloc[i]:.3f}")
        
        print(f"\n[YORUM] Guncel MACD:")
        macd_interp = interpret_macd(
            macd_line.iloc[-1],
            signal_line.iloc[-1],
            histogram.iloc[-1],
            macd_line.iloc[-2],
            signal_line.iloc[-2]
        )
        print(f"  Sinyal: {macd_interp['signal']}")
        print(f"  Guc: {macd_interp['strength']}/100")
        print(f"  Kesisim: {macd_interp['crossover']}")
        print(f"  Aciklama: {macd_interp['description']}")
        
        print("\n" + "="*60)
        print("[OK] TUM TESTLER TAMAMLANDI!")
        print("="*60)
    else:
        print("[HATA] Veri cekilemedi, test yapilamiyor")

