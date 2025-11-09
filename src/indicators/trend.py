"""
Trend Göstergeleri

Bu modül trend takip göstergelerini hesaplar:
- Moving Averages (SMA, EMA)
- Golden Cross / Death Cross tespiti
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def calculate_moving_averages(
    data: pd.DataFrame,
    periods: List[int] = [20, 50, 200],
    ma_type: str = 'SMA',
    column: str = 'Close'
) -> Dict[str, pd.Series]:
    """
    Hareketli Ortalamalar - Moving Averages
    
    MA Nedir?
    --------
    Belirlediğin bir dönemin (örn. 50 gün) ortalama fiyatını gösterir.
    Fiyat gürültüsünü azaltır, trend yönünü netleştirir.
    
    SMA vs EMA:
    ----------
    - SMA (Simple): Tüm günlere eşit ağırlık
    - EMA (Exponential): Son günlere daha fazla ağırlık
    
    Nasıl Yorumlanır?
    ----------------
    1. Trend Yönü:
       - Fiyat MA'nın üstünde: Yükseliş trendi
       - Fiyat MA'nın altında: Düşüş trendi
    
    2. MA Eğimi:
       - MA yükseliyor: Güçlü trend
       - MA yatay: Yön belirsiz (konsolidasyon)
       - MA düşüyor: Zayıf trend
    
    3. Golden Cross (Altın Kesişim):
       - MA(50) yukarı keser MA(200): GÜÇLÜ AL sinyali
    
    4. Death Cross (Ölüm Kesişimi):
       - MA(50) aşağı keser MA(200): GÜÇLÜ SAT sinyali
    
    5. Destek-Direnç:
       - MA çizgisi genellikle destek/direnç görevi görür
    
    Args:
        data (pd.DataFrame): Fiyat verileri
        periods (list): Periyotlar listesi
        ma_type (str): 'SMA' veya 'EMA'
        column (str): Hangi sütun
    
    Returns:
        dict: {period: MA Series} formatında
    
    Örnek:
        >>> mas = calculate_moving_averages(data, periods=[20, 50, 200])
        >>> ma_50 = mas[50]
        >>> current_price = data['Close'].iloc[-1]
        >>> if current_price > ma_50.iloc[-1]:
        ...     print("Fiyat 50 gunluk MA'nin ustunde - Yukselis trendi")
    """
    
    results = {}
    
    for period in periods:
        if ma_type.upper() == 'SMA':
            # Simple Moving Average
            results[period] = data[column].rolling(window=period).mean()
        elif ma_type.upper() == 'EMA':
            # Exponential Moving Average
            results[period] = data[column].ewm(span=period, adjust=False).mean()
        else:
            raise ValueError(f"MA type '{ma_type}' gecersiz. 'SMA' veya 'EMA' kullanin.")
    
    return results


def detect_ma_cross(
    fast_ma: pd.Series,
    slow_ma: pd.Series,
    lookback: int = 5
) -> Dict[str, any]:
    """
    İki MA arasındaki kesişimi tespit eder (Golden/Death Cross).
    
    Args:
        fast_ma: Hızlı MA (örn. 50 günlük)
        slow_ma: Yavaş MA (örn. 200 günlük)
        lookback: Kaç gün geriye bakılsın
    
    Returns:
        dict: Kesişim bilgisi
    """
    
    if len(fast_ma) < 2 or len(slow_ma) < 2:
        return {'cross': None, 'days_ago': None, 'type': None}
    
    # Son N günü kontrol et
    for i in range(1, min(lookback + 1, len(fast_ma))):
        idx_curr = -i
        idx_prev = -i - 1
        
        # Golden Cross: Hızlı yukarı keser Yavaş'ı
        if (fast_ma.iloc[idx_curr] > slow_ma.iloc[idx_curr] and
            fast_ma.iloc[idx_prev] <= slow_ma.iloc[idx_prev]):
            return {
                'cross': 'GOLDEN',
                'days_ago': i - 1,
                'type': 'BULLISH',
                'description': f'GOLDEN CROSS! MA kesisimi {i-1} gun once gerceklesti - GUCLU AL sinyali'
            }
        
        # Death Cross: Hızlı aşağı keser Yavaş'ı
        elif (fast_ma.iloc[idx_curr] < slow_ma.iloc[idx_curr] and
              fast_ma.iloc[idx_prev] >= slow_ma.iloc[idx_prev]):
            return {
                'cross': 'DEATH',
                'days_ago': i - 1,
                'type': 'BEARISH',
                'description': f'DEATH CROSS! MA kesisimi {i-1} gun once gerceklesti - GUCLU SAT sinyali'
            }
    
    # Kesişim yok
    if fast_ma.iloc[-1] > slow_ma.iloc[-1]:
        return {
            'cross': None,
            'current_position': 'ABOVE',
            'type': 'BULLISH',
            'description': 'Hizli MA yavas MA\'nin ustunde - Yukselis trendi devam ediyor'
        }
    else:
        return {
            'cross': None,
            'current_position': 'BELOW',
            'type': 'BEARISH',
            'description': 'Hizli MA yavas MA\'nin altinda - Dusus trendi devam ediyor'
        }


def interpret_moving_averages(
    price: float,
    ma_values: Dict[int, float]
) -> Dict[str, any]:
    """
    Fiyatın MA'lere göre pozisyonunu yorumlar.
    
    Args:
        price: Mevcut fiyat
        ma_values: {period: ma_value} dict'i
    
    Returns:
        dict: Yorum ve sinyal
    """
    
    signals = []
    strength = 0
    
    for period, ma_val in sorted(ma_values.items()):
        if pd.isna(ma_val):
            continue
        
        if price > ma_val:
            signals.append(f"MA({period}) USTUNDE")
            strength += 15
        else:
            signals.append(f"MA({period}) ALTINDA")
            strength -= 15
    
    # Sinyal belirle
    if strength > 25:
        signal = 'BUY'
        overall = 'GUCLU YUKSELIS TRENDI'
    elif strength > 0:
        signal = 'HOLD_BUY'
        overall = 'YUKSELIS EGILIMI'
    elif strength < -25:
        signal = 'SELL'
        overall = 'GUCLU DUSUS TRENDI'
    elif strength < 0:
        signal = 'HOLD_SELL'
        overall = 'DUSUS EGILIMI'
    else:
        signal = 'HOLD'
        overall = 'NOTR / KARASIZ'
    
    description = f"{overall}. Fiyat {len([s for s in signals if 'USTUNDE' in s])}/{len(signals)} MA\'nin ustunde."
    
    return {
        'signal': signal,
        'strength': abs(strength),
        'description': description,
        'overall_trend': overall,
        'ma_positions': signals
    }


# Test fonksiyonu
if __name__ == "__main__":
    print("=" * 60)
    print("TREND GOSTERGELERI - TEST")
    print("=" * 60)
    
    from src.data.fetcher import fetch_stock_data
    
    print("\n[TEST] THYAO verisi cekiliyor...")
    data = fetch_stock_data('THYAO', period='1y')
    
    if data is not None:
        print(f"[OK] {len(data)} gunluk veri cekildi\n")
        
        print("="*60)
        print("[TEST] Moving Averages Hesaplama")
        print("="*60)
        
        mas = calculate_moving_averages(data, periods=[20, 50, 200])
        current_price = data['Close'].iloc[-1]
        
        print(f"\nGuncel Fiyat: {current_price:.2f} TL\n")
        print("MA Degerleri:")
        for period, ma_series in sorted(mas.items()):
            ma_val = ma_series.iloc[-1]
            diff = current_price - ma_val
            pct = (diff / ma_val) * 100
            status = "USTUNDE" if diff > 0 else "ALTINDA"
            print(f"  MA({period:3}): {ma_val:6.2f} TL | Fark: {diff:+6.2f} ({pct:+5.1f}%) | {status}")
        
        # Golden/Death Cross kontrolü
        if 50 in mas and 200 in mas:
            print("\n" + "="*60)
            print("[TEST] Golden/Death Cross Kontrolu")
            print("="*60)
            
            cross_info = detect_ma_cross(mas[50], mas[200], lookback=30)
            print(f"\nKesisim Durumu:")
            print(f"  Tip: {cross_info.get('cross', 'YOK')}")
            print(f"  Aciklama: {cross_info['description']}")
        
        # Genel yorum
        print("\n" + "="*60)
        print("[YORUM] Genel Trend Analizi")
        print("="*60)
        
        ma_current = {p: ma.iloc[-1] for p, ma in mas.items()}
        interp = interpret_moving_averages(current_price, ma_current)
        
        print(f"\n  Sinyal: {interp['signal']}")
        print(f"  Guc: {interp['strength']}/100")
        print(f"  Genel Trend: {interp['overall_trend']}")
        print(f"  Aciklama: {interp['description']}")
        
        print("\n" + "="*60)
        print("[OK] TEST TAMAMLANDI!")
        print("="*60)
    else:
        print("[HATA] Veri cekilemedi")

