"""
Teknik Analiz Motoru

Tüm teknik göstergeleri birleştirerek
kapsamlı analiz yapar ve sinyaller üretir.
"""

import pandas as pd
from typing import Dict, List
from ..indicators.momentum import calculate_rsi, calculate_macd, interpret_rsi, interpret_macd
from ..indicators.volatility import calculate_bollinger_bands, interpret_bollinger_bands
from ..indicators.trend import calculate_moving_averages, interpret_moving_averages, detect_ma_cross
from ..indicators.volume import analyze_volume


def analyze_stock(data: pd.DataFrame, symbol: str = "") -> Dict:
    """
    Hisse için kapsamlı teknik analiz yapar.
    
    Args:
        data: Fiyat verileri
        symbol: Hisse kodu
    
    Returns:
        dict: Tüm analiz sonuçları
    """
    
    if data is None or data.empty:
        return {'error': 'Veri yok'}
    
    results = {
        'symbol': symbol,
        'current_price': float(data['Close'].iloc[-1]),
        'date': str(data.index[-1].date()),
        'indicators': {},
        'signals': []
    }
    
    # 1. RSI
    try:
        rsi = calculate_rsi(data)
        rsi_val = rsi.iloc[-1]
        rsi_interp = interpret_rsi(rsi_val)
        results['indicators']['RSI'] = rsi_interp
        results['signals'].append({
            'indicator': 'RSI',
            'signal': rsi_interp['signal'],
            'strength': rsi_interp['strength']
        })
    except Exception as e:
        results['indicators']['RSI'] = {'error': str(e)}
    
    # 2. MACD
    try:
        macd_line, signal_line, histogram = calculate_macd(data)
        macd_interp = interpret_macd(
            macd_line.iloc[-1],
            signal_line.iloc[-1],
            histogram.iloc[-1],
            macd_line.iloc[-2] if len(macd_line) > 1 else None,
            signal_line.iloc[-2] if len(signal_line) > 1 else None
        )
        results['indicators']['MACD'] = macd_interp
        results['signals'].append({
            'indicator': 'MACD',
            'signal': macd_interp['signal'],
            'strength': macd_interp['strength']
        })
    except Exception as e:
        results['indicators']['MACD'] = {'error': str(e)}
    
    # 3. Bollinger Bands
    try:
        upper, middle, lower = calculate_bollinger_bands(data)
        bb_interp = interpret_bollinger_bands(
            data['Close'].iloc[-1],
            upper.iloc[-1],
            middle.iloc[-1],
            lower.iloc[-1]
        )
        results['indicators']['Bollinger_Bands'] = bb_interp
        results['signals'].append({
            'indicator': 'Bollinger Bands',
            'signal': bb_interp['signal'],
            'strength': bb_interp['strength']
        })
    except Exception as e:
        results['indicators']['Bollinger_Bands'] = {'error': str(e)}
    
    # 4. Moving Averages
    try:
        mas = calculate_moving_averages(data, periods=[20, 50, 200])
        ma_values = {p: ma.iloc[-1] for p, ma in mas.items() if not pd.isna(ma.iloc[-1])}
        ma_interp = interpret_moving_averages(data['Close'].iloc[-1], ma_values)
        
        # Golden/Death Cross
        if 50 in mas and 200 in mas:
            cross_info = detect_ma_cross(mas[50], mas[200], lookback=10)
            ma_interp['cross_info'] = cross_info
        
        results['indicators']['Moving_Averages'] = ma_interp
        results['signals'].append({
            'indicator': 'Moving Averages',
            'signal': ma_interp['signal'],
            'strength': ma_interp['strength']
        })
    except Exception as e:
        results['indicators']['Moving_Averages'] = {'error': str(e)}
    
    # 5. Volume
    try:
        vol_result = analyze_volume(data)
        results['indicators']['Volume'] = vol_result
        results['signals'].append({
            'indicator': 'Volume',
            'signal': vol_result['signal'],
            'strength': vol_result['strength']
        })
    except Exception as e:
        results['indicators']['Volume'] = {'error': str(e)}
    
    return results


def generate_signals(analysis: Dict) -> Dict:
    """
    Tüm göstergelerin sinyallerini birleştirerek
    genel karar üretir.
    
    Args:
        analysis: analyze_stock() çıktısı
    
    Returns:
        dict: Genel sinyal ve öneriler
    """
    
    if 'error' in analysis:
        return {'error': analysis['error']}
    
    signals = analysis.get('signals', [])
    
    if not signals:
        return {
            'overall_signal': 'HOLD',
            'confidence': 0,
            'description': 'Yeterli sinyal yok'
        }
    
    # Sinyal skorlama sistemi
    score = 0
    total_strength = 0
    buy_count = 0
    sell_count = 0
    hold_count = 0
    
    for sig in signals:
        signal_type = sig['signal']
        strength = sig['strength']
        
        if 'BUY' in signal_type:
            score += strength
            buy_count += 1
        elif 'SELL' in signal_type:
            score -= strength
            sell_count += 1
        else:
            hold_count += 1
        
        total_strength += strength
    
    # Ortalama güven seviyesi
    avg_strength = total_strength / len(signals) if signals else 0
    
    # Genel sinyal belirle
    if score > 100:
        overall_signal = 'STRONG_BUY'
        confidence = min(95, 60 + (score / 10))
    elif score > 50:
        overall_signal = 'BUY'
        confidence = min(85, 50 + (score / 10))
    elif score > 0:
        overall_signal = 'HOLD_BUY'
        confidence = 40 + (score / 5)
    elif score < -100:
        overall_signal = 'STRONG_SELL'
        confidence = min(95, 60 + (-score / 10))
    elif score < -50:
        overall_signal = 'SELL'
        confidence = min(85, 50 + (-score / 10))
    elif score < 0:
        overall_signal = 'HOLD_SELL'
        confidence = 40 + (-score / 5)
    else:
        overall_signal = 'HOLD'
        confidence = 30
    
    # Açıklama oluştur
    total_indicators = len(signals)
    description = f"{buy_count}/{total_indicators} gosterge ALIM, {sell_count}/{total_indicators} gosterge SATIM sinyali veriyor."
    
    return {
        'overall_signal': overall_signal,
        'confidence': int(confidence),
        'score': int(score),
        'description': description,
        'buy_count': buy_count,
        'sell_count': sell_count,
        'hold_count': hold_count,
        'avg_strength': int(avg_strength)
    }

