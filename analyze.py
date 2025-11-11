#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Algo Trading Bot - Ana Analiz Scripti

Kullanim:
    python analyze.py THYAO
    python analyze.py SASA --period 6mo
    python analyze.py GARAN --detailed
    python analyze.py THYAO --macro

Yazar: Berke Yildirim
Tarih: 2025-11-09
Guncelleme: 2025-11-11 (Faz 2: Makro entegrasyonu)
"""

import sys
import argparse
import os
from src.data.fetcher import fetch_stock_data
from src.data.bist_stocks import is_valid_bist_stock, suggest_similar_stocks
from src.analysis.technical import analyze_stock, generate_signals
from src.reporting.terminal import print_analysis_report, print_hybrid_report
from src.macro.fetcher import MacroDataFetcher
from src.analysis.hybrid import HybridAnalyzer


def main():
    """Ana fonksiyon"""
    
    # Argument parser
    parser = argparse.ArgumentParser(
        description='BIST hisse senedi analiz araci (Teknik + Makro)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ornekler:
  python analyze.py THYAO                # Sadece teknik analiz
  python analyze.py SASA --period 6mo    # 6 aylik veri
  python analyze.py THYAO --macro        # Hibrid analiz (Teknik + Makro)
  python analyze.py GARAN --detailed     # Detayli rapor

Desteklenen periyotlar:
  1d, 5d, 1mo, 3mo, 6mo, 1y (varsayilan), 2y, 5y, max

Not: --macro kullanmadan once: python update_macro.py
        """
    )
    
    parser.add_argument(
        'symbol',
        type=str,
        help='Hisse kodu (ornek: THYAO, SASA, GARAN)'
    )
    
    parser.add_argument(
        '--period',
        type=str,
        default='1y',
        help='Veri periyodu (varsayilan: 1y)'
    )
    
    parser.add_argument(
        '--macro',
        action='store_true',
        help='Makroekonomik analiz ekle (Hibrid mod)'
    )
    
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Detayli rapor (gelecekte eklenecek)'
    )
    
    args = parser.parse_args()
    
    # Hisse kodunu büyük harfe çevir
    symbol = args.symbol.upper().strip()
    
    # Banner
    print("\n" + "="*70)
    if args.macro:
        print("    ALGO TRADING BOT - Hibrid Analiz Sistemi v0.2")
        print("         (Teknik Analiz + Makroekonomik Faktörler)")
    else:
        print("       ALGO TRADING BOT - Teknik Analiz Sistemi v0.1")
    print("="*70)
    
    # BIST hissesi kontrolü
    if not is_valid_bist_stock(symbol):
        print(f"\n[UYARI] '{symbol}' BIST100 listesinde bulunamadi.")
        
        # Benzer hisse öner
        similar = suggest_similar_stocks(symbol)
        if similar:
            print(f"[ONERI] Belki bunlardan birini mi demek istediniz?")
            for s in similar[:5]:
                print(f"  - {s}")
        
        response = input(f"\nYine de devam etmek istiyor musunuz? (e/h): ")
        if response.lower() != 'e':
            print("[IPTAL] Analiz iptal edildi.")
            sys.exit(0)
    
    # Veri çek
    print(f"\n[ADIM 1] {symbol} verisi cekiliyor ({args.period})...")
    data = fetch_stock_data(symbol, period=args.period)
    
    if data is None or data.empty:
        print(f"[HATA] {symbol} verisi cekilemedi. Hisse kodu dogru mu?")
        sys.exit(1)
    
    print(f"[OK] {len(data)} gunluk veri cekildi.")
    
    # Analiz yap
    print(f"\n[ADIM 2] Teknik gostergeler hesaplaniyor...")
    analysis = analyze_stock(data, symbol=symbol)
    
    print(f"[OK] {len(analysis.get('signals', []))} gosterge hesaplandi.")
    
    # Sinyal üret
    print(f"\n[ADIM 3] Genel sinyal uretiliyor...")
    signals = generate_signals(analysis)
    
    print(f"[OK] Analiz tamamlandi!")
    
    # Makro analiz istendi mi?
    if args.macro:
        print(f"\n[ADIM 4] Makroekonomik veriler yukleniyor...")
        
        # Makro veri yükle
        fetcher = MacroDataFetcher()
        macro_data = fetcher.load_from_config()
        
        if macro_data is None:
            print(f"[HATA] Makro veriler bulunamadi!")
            print(f"[COZUM] Once makro verileri guncelleyin: python update_macro.py")
            sys.exit(1)
        
        print(f"[OK] Makro veriler yuklendi (Son guncelleme: {macro_data.get('last_update', 'Bilinmiyor')})")
        
        # Hibrid analiz
        print(f"\n[ADIM 5] Hibrid analiz yapiliyor (Teknik + Makro)...")
        
        technical_score = signals.get('score', 50)  # Teknik skor (0-100)
        
        hybrid_analyzer = HybridAnalyzer(
            technical_score=technical_score,
            macro_data=macro_data,
            symbol=symbol
        )
        
        hybrid_result = hybrid_analyzer.calculate_hybrid_score()
        recommendation = hybrid_analyzer.get_recommendation(hybrid_result)
        
        print(f"[OK] Hibrid analiz tamamlandi!")
        
        # Hibrid rapor yazdır
        print_hybrid_report(analysis, signals, hybrid_result, recommendation)
    else:
        # Normal teknik rapor
        print_analysis_report(analysis, signals)
        
        # Makro öneri
        print(f"\n[IPUCU] Makroekonomik faktörleri de analiz etmek icin:")
        print(f"         python analyze.py {symbol} --macro")
    
    # Ek bilgi
    if args.detailed:
        print("[BILGI] Detayli rapor ozelligi yakinda eklenecek...")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[IPTAL] Kullanici tarafindan iptal edildi.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[HATA] Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

