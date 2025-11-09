"""
Terminal Raporlama

Analiz sonuçlarını terminal'de
renkli ve düzenli gösterir.
"""

from colorama import Fore, Style, init
from typing import Dict

# Colorama başlat (Windows için)
init(autoreset=True)


def print_analysis_report(analysis: Dict, signals: Dict):
    """
    Analiz sonuçlarını terminal'de yazdırır.
    
    Args:
        analysis: analyze_stock() çıktısı
        signals: generate_signals() çıktısı
    """
    
    if 'error' in analysis:
        print(f"{Fore.RED}[HATA] {analysis['error']}{Style.RESET_ALL}")
        return
    
    symbol = analysis.get('symbol', 'N/A')
    price = analysis.get('current_price', 0)
    date = analysis.get('date', 'N/A')
    
    # Başlık
    print("\n" + "=" * 70)
    print(f"{Fore.CYAN}       HISSE ANALIZ RAPORU - {symbol}{Style.RESET_ALL}")
    print("=" * 70)
    
    print(f"\nTarih: {date}")
    print(f"Guncel Fiyat: {Fore.YELLOW}{price:.2f} TL{Style.RESET_ALL}")
    
    # Genel Sinyal
    print("\n" + "-" * 70)
    print(f"{Fore.GREEN}GENEL DEGERLENDIRME{Style.RESET_ALL}")
    print("-" * 70)
    
    overall_signal = signals.get('overall_signal', 'HOLD')
    confidence = signals.get('confidence', 0)
    
    # Sinyal rengi
    if 'BUY' in overall_signal:
        signal_color = Fore.GREEN
        emoji = "[AL]"
    elif 'SELL' in overall_signal:
        signal_color = Fore.RED
        emoji = "[SAT]"
    else:
        signal_color = Fore.YELLOW
        emoji = "[BEK]"
    
    print(f"\nSinyal: {signal_color}{emoji} {overall_signal}{Style.RESET_ALL}")
    print(f"Guven: {confidence}% {'='*int(confidence/2)}")
    print(f"Skor: {signals.get('score', 0)}")
    print(f"\n{signals.get('description', '')}")
    
    # Göstergeler
    print("\n" + "-" * 70)
    print(f"{Fore.GREEN}GOSTERGE DETAYLARI{Style.RESET_ALL}")
    print("-" * 70)
    
    indicators = analysis.get('indicators', {})
    
    # RSI
    if 'RSI' in indicators and 'error' not in indicators['RSI']:
        rsi = indicators['RSI']
        print(f"\n{Fore.CYAN}[1] RSI (Relative Strength Index){Style.RESET_ALL}")
        print(f"    Deger: {rsi.get('value', 'N/A')}")
        print(f"    Bolge: {rsi.get('zone', 'N/A')}")
        print(f"    Sinyal: {get_signal_text(rsi.get('signal', 'HOLD'))}")
        print(f"    Guc: {rsi.get('strength', 0)}/100")
        print(f"    >> {rsi.get('description', '')}")
    
    # MACD
    if 'MACD' in indicators and 'error' not in indicators['MACD']:
        macd = indicators['MACD']
        print(f"\n{Fore.CYAN}[2] MACD (Moving Average Convergence Divergence){Style.RESET_ALL}")
        print(f"    MACD Line: {macd.get('macd_value', 'N/A')}")
        print(f"    Signal Line: {macd.get('signal_value', 'N/A')}")
        print(f"    Histogram: {macd.get('histogram_value', 'N/A')}")
        print(f"    Sinyal: {get_signal_text(macd.get('signal', 'HOLD'))}")
        print(f"    Guc: {macd.get('strength', 0)}/100")
        if macd.get('crossover'):
            print(f"    {Fore.YELLOW}>>> KESISIM: {macd.get('crossover')}{Style.RESET_ALL}")
        print(f"    >> {macd.get('description', '')}")
    
    # Bollinger Bands
    if 'Bollinger_Bands' in indicators and 'error' not in indicators['Bollinger_Bands']:
        bb = indicators['Bollinger_Bands']
        print(f"\n{Fore.CYAN}[3] Bollinger Bands{Style.RESET_ALL}")
        print(f"    Ust Band: {bb.get('upper_band', 'N/A')} TL")
        print(f"    Orta Band: {bb.get('middle_band', 'N/A')} TL")
        print(f"    Alt Band: {bb.get('lower_band', 'N/A')} TL")
        print(f"    Pozisyon: {bb.get('position', 'N/A')}")
        print(f"    Sinyal: {get_signal_text(bb.get('signal', 'HOLD'))}")
        print(f"    Guc: {bb.get('strength', 0)}/100")
        print(f"    >> {bb.get('description', '')}")
    
    # Moving Averages
    if 'Moving_Averages' in indicators and 'error' not in indicators['Moving_Averages']:
        ma = indicators['Moving_Averages']
        print(f"\n{Fore.CYAN}[4] Moving Averages (Hareketli Ortalamalar){Style.RESET_ALL}")
        print(f"    Genel Trend: {ma.get('overall_trend', 'N/A')}")
        print(f"    Sinyal: {get_signal_text(ma.get('signal', 'HOLD'))}")
        print(f"    Guc: {ma.get('strength', 0)}/100")
        
        if 'cross_info' in ma and ma['cross_info'].get('cross'):
            cross = ma['cross_info']
            print(f"    {Fore.YELLOW}>>> {cross.get('description', '')}{Style.RESET_ALL}")
        
        print(f"    >> {ma.get('description', '')}")
    
    # Volume
    if 'Volume' in indicators and 'error' not in indicators['Volume']:
        vol = indicators['Volume']
        print(f"\n{Fore.CYAN}[5] Hacim Analizi (Volume){Style.RESET_ALL}")
        print(f"    Durum: {vol.get('volume_status', 'N/A')}")
        print(f"    Guncel: {vol.get('current_volume', 0):,}")
        print(f"    Ortalama: {vol.get('avg_volume', 0):,}")
        print(f"    Oran: {vol.get('volume_ratio', 'N/A')}x normal")
        print(f"    Sinyal: {get_signal_text(vol.get('signal', 'HOLD'))}")
        print(f"    Guc: {vol.get('strength', 0)}/100")
        print(f"    >> {vol.get('description', '')}")
    
    # Alt bilgi
    print("\n" + "=" * 70)
    print(f"{Fore.MAGENTA}NOT:{Style.RESET_ALL} Bu analiz egitim amacidir, yatirim tavsiyesi degildir!")
    print("=" * 70 + "\n")


def get_signal_text(signal: str) -> str:
    """Sinyal için renkli metin döndürür."""
    if 'BUY' in signal:
        return f"{Fore.GREEN}{signal}{Style.RESET_ALL}"
    elif 'SELL' in signal:
        return f"{Fore.RED}{signal}{Style.RESET_ALL}"
    else:
        return f"{Fore.YELLOW}{signal}{Style.RESET_ALL}"

