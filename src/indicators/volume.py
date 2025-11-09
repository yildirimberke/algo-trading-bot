"""
Hacim (Volume) Analizi

Bu modül hacim bazlı analizler yapar:
- Hacim artışı/azalışı tespiti
- Kurumsal alım tespiti
- Volume-Price correlation
"""

import pandas as pd
import numpy as np
from typing import Dict


def analyze_volume(
    data: pd.DataFrame,
    avg_period: int = 20,
    threshold_multiplier: float = 1.5
) -> Dict[str, any]:
    """
    Hacim Analizi - Volume Analysis
    
    Hacim Nedir?
    -----------
    Bir günde el değiştiren hisse adedidir.
    Yüksek hacim = İlgi var, güçlü hareket
    Düşük hacim = İlgi yok, zayıf hareket
    
    Nasıl Yorumlanır?
    ----------------
    1. Hacim + Fiyat Yükselişi = GÜÇLÜ AL BASKI (Bullish)
    2. Hacim + Fiyat Düşüşü = GÜÇLÜ SAT BASKI (Bearish)
    3. Hacim Düşük + Fiyat Hareketi = ZAY if HAREKET (şüpheli)
    4. Ani Hacim Artışı = ÖNEMLI BIR ŞEY OLUYOR (dikkat!)
    
    Kurumsal Alım/Satım:
    -------------------
    - Hacim normalin 2-3 katı + Fiyat yükselişi = Kurumsal alım olabilir
    - Hacim normalin 2-3 katı + Fiyat düşüşü = Kurumsal satış olabilir
    
    Args:
        data (pd.DataFrame): Fiyat ve hacim verileri
        avg_period (int): Ortalama hacim hesaplama periyodu
        threshold_multiplier (float): Hangi katı "yüksek hacim" sayılsın
    
    Returns:
        dict: Hacim analiz sonuçları
    
    Örnek:
        >>> data = fetch_stock_data('THYAO')
        >>> vol_analysis = analyze_volume(data)
        >>> print(vol_analysis['description'])
    """
    
    if 'Volume' not in data.columns:
        return {
            'signal': 'HOLD',
            'strength': 0,
            'description': 'Hacim verisi yok',
            'status': 'N/A'
        }
    
    # Son günün hacmi
    current_volume = data['Volume'].iloc[-1]
    
    # Ortalama hacim hesapla
    avg_volume = data['Volume'].rolling(window=avg_period).mean().iloc[-1]
    
    # Hacim oranı
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
    
    # Fiyat değişimi (son gün)
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    price_change_pct = (price_change / data['Close'].iloc[-2]) * 100
    
    # Sinyal ve yorum oluştur
    if volume_ratio >= threshold_multiplier * 2:  # Çok yüksek hacim (3x+)
        volume_status = 'PATLAMA'
        
        if price_change > 0:
            signal = 'BUY'
            strength = min(100, int(volume_ratio * 20))
            description = f'HACIM PATLAMASI! ({volume_ratio:.1f}x normal) + Fiyat yukseldi ({price_change_pct:+.1f}%). GUCLU ALIM BASKI - Kurumsal alim olabilir!'
        else:
            signal = 'SELL'
            strength = min(100, int(volume_ratio * 20))
            description = f'HACIM PATLAMASI! ({volume_ratio:.1f}x normal) + Fiyat dustu ({price_change_pct:+.1f}%). GUCLU SATIM BASKI - Kurumsal satim olabilir!'
    
    elif volume_ratio >= threshold_multiplier:  # Yüksek hacim (1.5x-3x)
        volume_status = 'YUKSEK'
        
        if price_change > 0:
            signal = 'HOLD_BUY'
            strength = int(volume_ratio * 25)
            description = f'Yuksek hacim ({volume_ratio:.1f}x) + Fiyat yukseldi ({price_change_pct:+.1f}%). Alim baski devam ediyor.'
        else:
            signal = 'HOLD_SELL'
            strength = int(volume_ratio * 25)
            description = f'Yuksek hacim ({volume_ratio:.1f}x) + Fiyat dustu ({price_change_pct:+.1f}%). Satim baski devam ediyor.'
    
    elif volume_ratio < 0.5:  # Çok düşük hacim
        volume_status = 'COK DUSUK'
        signal = 'HOLD'
        strength = 10
        
        if abs(price_change_pct) > 2:
            description = f'Cok dusuk hacim ({volume_ratio:.1f}x) ama fiyat hareket etti ({price_change_pct:+.1f}%). SUPLELI hareket, dikkatli olun!'
        else:
            description = f'Cok dusuk hacim ({volume_ratio:.1f}x). Ilgi yok, beklemede kalin.'
    
    else:  # Normal hacim
        volume_status = 'NORMAL'
        
        if abs(price_change_pct) > 3:
            signal = 'HOLD_BUY' if price_change > 0 else 'HOLD_SELL'
            strength = 30
            description = f'Normal hacim ama fiyat belirgin hareket etti ({price_change_pct:+.1f}%). Orta seviye sinyal.'
        else:
            signal = 'HOLD'
            strength = 10
            description = f'Normal hacim, normal fiyat hareketi. Net sinyal yok.'
    
    return {
        'signal': signal,
        'strength': strength,
        'description': description,
        'volume_status': volume_status,
        'current_volume': int(current_volume),
        'avg_volume': int(avg_volume),
        'volume_ratio': round(volume_ratio, 2),
        'price_change_pct': round(price_change_pct, 2)
    }


def detect_volume_trend(data: pd.DataFrame, period: int = 10) -> str:
    """
    Son N günün hacim trendini tespit eder.
    
    Args:
        data: Fiyat verileri
        period: Kaç gün geriye bakılsın
    
    Returns:
        str: 'ARTIS', 'AZALIS', 'SABIT'
    """
    
    if 'Volume' not in data.columns or len(data) < period:
        return 'BILINMIYOR'
    
    recent_volumes = data['Volume'].iloc[-period:]
    first_half_avg = recent_volumes.iloc[:period//2].mean()
    second_half_avg = recent_volumes.iloc[period//2:].mean()
    
    change_ratio = second_half_avg / first_half_avg if first_half_avg > 0 else 1
    
    if change_ratio > 1.2:
        return 'ARTIS'
    elif change_ratio < 0.8:
        return 'AZALIS'
    else:
        return 'SABIT'


# Test fonksiyonu
if __name__ == "__main__":
    print("=" * 60)
    print("HACIM ANALIZI - TEST")
    print("=" * 60)
    
    from src.data.fetcher import fetch_stock_data
    
    print("\n[TEST] THYAO verisi cekiliyor...")
    data = fetch_stock_data('THYAO', period='3mo')
    
    if data is not None:
        print(f"[OK] {len(data)} gunluk veri cekildi\n")
        
        print("="*60)
        print("[TEST] Hacim Analizi")
        print("="*60)
        
        print(f"\nSon 5 gun hacim ve fiyat:")
        for i in range(-5, 0):
            vol = data['Volume'].iloc[i]
            price = data['Close'].iloc[i]
            print(f"  {data.index[i].date()}: Hacim={vol:,}, Fiyat={price:.2f} TL")
        
        print("\n" + "="*60)
        print("[YORUM] Guncel Hacim Analizi")
        print("="*60)
        
        vol_result = analyze_volume(data)
        
        print(f"\n  Sinyal: {vol_result['signal']}")
        print(f"  Guc: {vol_result['strength']}/100")
        print(f"  Durum: {vol_result['volume_status']}")
        print(f"  Guncel Hacim: {vol_result['current_volume']:,}")
        print(f"  Ortalama Hacim: {vol_result['avg_volume']:,}")
        print(f"  Hacim Orani: {vol_result['volume_ratio']}x")
        print(f"  Fiyat Degisimi: {vol_result['price_change_pct']:+.2f}%")
        print(f"\n  Aciklama: {vol_result['description']}")
        
        # Hacim trendi
        vol_trend = detect_volume_trend(data, period=10)
        print(f"\n  Son 10 gun hacim trendi: {vol_trend}")
        
        print("\n" + "="*60)
        print("[OK] TEST TAMAMLANDI!")
        print("="*60)
    else:
        print("[HATA] Veri cekilemedi")

