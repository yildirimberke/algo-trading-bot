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


def print_hybrid_report(analysis: Dict, signals: Dict, hybrid_result: Dict, recommendation: str):
    """
    Hibrid analiz (Teknik + Makro) sonuçlarını yazdırır.
    
    Args:
        analysis: Teknik analiz sonuçları
        signals: Teknik sinyal sonuçları
        hybrid_result: Hibrid analiz sonuçları
        recommendation: Yatırım önerisi
    """
    
    if 'error' in analysis:
        print(f"{Fore.RED}[HATA] {analysis['error']}{Style.RESET_ALL}")
        return
    
    symbol = analysis.get('symbol', 'N/A')
    price = analysis.get('current_price', 0)
    date = analysis.get('date', 'N/A')
    
    # Başlık
    print("\n" + "=" * 80)
    print(f"{Fore.CYAN}     HİBRİD ANALİZ RAPORU - {symbol} (Teknik + Makro){Style.RESET_ALL}")
    print("=" * 80)
    
    print(f"\nTarih: {date}")
    print(f"Guncel Fiyat: {Fore.YELLOW}{price:.2f} TL{Style.RESET_ALL}")
    
    # Hibrid Genel Değerlendirme
    print("\n" + "-" * 80)
    print(f"{Fore.MAGENTA}HIBRİD GENEL DEGERLENDİRME{Style.RESET_ALL}")
    print("-" * 80)
    
    signal = hybrid_result['signal']
    emoji = hybrid_result['signal_emoji']
    score = hybrid_result['hybrid_score']
    confidence = hybrid_result['confidence']
    
    print(f"\nHibrid Skor: {Fore.CYAN}{score}/100{Style.RESET_ALL}")
    print(f"Sinyal: {emoji} {Fore.GREEN if signal == 'AL' else Fore.RED if signal == 'SAT' else Fore.YELLOW}{signal}{Style.RESET_ALL}")
    print(f"Guven Seviyesi: {confidence}")
    print(f"Agirliklar: Teknik %{hybrid_result['weights']['technical']} | Makro %{hybrid_result['weights']['macro']}")
    
    # Uyum Durumu
    alignment = hybrid_result['alignment']
    print(f"\n{alignment['emoji']} Uyum Durumu: {alignment['status']}")
    print(f"   {alignment['description']}")
    
    # Teknik Özet
    print("\n" + "-" * 80)
    print(f"{Fore.GREEN}1) TEKNİK ANALİZ ÖZET{Style.RESET_ALL}")
    print("-" * 80)
    
    tech = hybrid_result['technical']
    tech_signal = signals.get('overall_signal', 'HOLD')
    
    print(f"Teknik Skor: {tech['score']}/100")
    print(f"Yon: {tech['direction']}")
    print(f"Teknik Sinyal: {get_signal_text(tech_signal)}")
    print(f"Guven: {signals.get('confidence', 0)}%")
    
    # Makro Analiz
    print("\n" + "-" * 80)
    print(f"{Fore.GREEN}2) MAKRO EKONOMİK ANALİZ{Style.RESET_ALL}")
    print("-" * 80)
    
    macro = hybrid_result['macro']
    general = macro['general']
    
    print(f"\nMakro Skor: {macro['score_raw']}/10 (Normalize: {macro['score_normalized']}/100)")
    print(f"Yon: {macro['direction']}")
    print(f"\n{general['summary']}")
    
    # Makro Detaylar
    print(f"\n{Fore.CYAN}Makro Faktörler:{Style.RESET_ALL}")
    
    for key, comp in general['components'].items():
        score_color = Fore.GREEN if comp['score'] > 2 else Fore.RED if comp['score'] < -2 else Fore.YELLOW
        print(f"\n  {key.upper().replace('_', '/')}:")
        print(f"    Skor: {score_color}{comp['score']:.1f}/10{Style.RESET_ALL} (Agirlik: %{comp['weight']*100:.0f})")
        print(f"    {comp['description']}")
    
    # Sektörel Analiz
    print(f"\n{Fore.CYAN}Sektörel Faktör:{Style.RESET_ALL}")
    sector = macro['sector']
    sector_color = Fore.GREEN if sector['score'] > 2 else Fore.RED if sector['score'] < -2 else Fore.YELLOW
    print(f"  Sektor: {sector['name']}")
    print(f"  Skor: {sector_color}{sector['score']:.1f}/10{Style.RESET_ALL}")
    print(f"  {sector['description']}")
    
    # Risk Analizi
    print("\n" + "-" * 80)
    print(f"{Fore.GREEN}3) RİSK DEGERLENDİRMESİ{Style.RESET_ALL}")
    print("-" * 80)
    
    risk = hybrid_result['risk']
    risk_color = Fore.GREEN if risk['level'] == 'DÜŞÜK' else Fore.RED if risk['level'] == 'YÜKSEK' else Fore.YELLOW
    
    print(f"\nRisk Seviyesi: {risk_color}{risk['level']}{Style.RESET_ALL}")
    print(f"{risk['description']}")
    
    # Yatırım Önerisi
    print("\n" + "-" * 80)
    print(f"{Fore.GREEN}4) YATIRIM ÖNERİSİ{Style.RESET_ALL}")
    print("-" * 80)
    print()
    print(recommendation)
    
    # Alt bilgi
    print("\n" + "=" * 80)
    print(f"{Fore.MAGENTA}NOT:{Style.RESET_ALL} Bu hibrid analiz egitim amacidir, yatirim tavsiyesi degildir!")
    print(f"{Fore.MAGENTA}UYARI:{Style.RESET_ALL} Makro veriler periyodik guncellenmeli (update_macro.py kullanarak)")
    print("=" * 80 + "\n")


def print_macro_data_summary(macro_data: Dict):
    """
    Makro verilerin özetini yazdırır
    
    Args:
        macro_data: Makroekonomik veriler
    """
    print("\n" + "=" * 70)
    print(f"{Fore.CYAN}       MAKRO EKONOMİK VERİLER{Style.RESET_ALL}")
    print("=" * 70)
    
    print(f"\nSon Guncelleme: {macro_data.get('last_update', 'Bilinmiyor')}")
    
    print(f"\n{Fore.GREEN}Doviz Kurlari:{Style.RESET_ALL}")
    usd = macro_data.get('usd_try', {})
    eur = macro_data.get('eur_try', {})
    print(f"  USD/TRY: {usd.get('current', 'N/A')} (30g: %{usd.get('change_30d', 'N/A')})")
    print(f"  EUR/TRY: {eur.get('current', 'N/A')} (30g: %{eur.get('change_30d', 'N/A')})")
    
    print(f"\n{Fore.GREEN}Piyasa Göstergeleri:{Style.RESET_ALL}")
    bist = macro_data.get('bist100', {})
    print(f"  BIST100: {bist.get('current', 'N/A')} (Trend: {bist.get('trend', 'N/A')})")
    
    print(f"\n{Fore.GREEN}Emtialar:{Style.RESET_ALL}")
    oil = macro_data.get('oil', {})
    gold = macro_data.get('gold', {})
    print(f"  Petrol (WTI): ${oil.get('current', 'N/A')} (30g: %{oil.get('change_30d', 'N/A')})")
    print(f"  Altin: ${gold.get('current', 'N/A')} (30g: %{gold.get('change_30d', 'N/A')})")
    
    print(f"\n{Fore.GREEN}Faiz:{Style.RESET_ALL}")
    tcmb = macro_data.get('tcmb_rate')
    if tcmb:
        print(f"  TCMB Politika Faizi: %{tcmb}")
    else:
        print(f"  {Fore.YELLOW}TCMB Politika Faizi: Girilmemis (update_macro.py --tcmb-rate X){Style.RESET_ALL}")
    
    print("\n" + "=" * 70 + "\n")
