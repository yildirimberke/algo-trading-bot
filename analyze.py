#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Algo Trading Bot - Ana Analiz Scripti

Kullanim:
    python analyze.py THYAO
    python analyze.py SASA --period 6mo
    python analyze.py GARAN --detailed

Yazar: Berke Yildirim
Tarih: 2025-11-09
"""

import sys
import argparse
from src.data.fetcher import fetch_stock_data
from src.data.bist_stocks import is_valid_bist_stock, suggest_similar_stocks
from src.analysis.technical import analyze_stock, generate_signals
from src.reporting.terminal import print_analysis_report


def main():
    """Ana fonksiyon"""
    
    # Argument parser
    parser = argparse.ArgumentParser(
        description='BIST hisse senedi teknik analiz araci',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ornekler:
  python analyze.py THYAO
  python analyze.py SASA --period 6mo
  python analyze.py GARAN --detailed

Desteklenen periyotlar:
  1d, 5d, 1mo, 3mo, 6mo, 1y (varsayilan), 2y, 5y, max
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
        '--detailed',
        action='store_true',
        help='Detayli rapor (gelecekte eklenecek)'
    )
    
    args = parser.parse_args()
    
    # Hisse kodunu büyük harfe çevir
    symbol = args.symbol.upper().strip()
    
    # Banner
    print("\n" + "="*70)
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
    print(f"\n[ADIM 3] Genel sinyal ureti liyor...")
    signals = generate_signals(analysis)
    
    print(f"[OK] Analiz tamamlandi!")
    
    # Rapor yazdır
    print_analysis_report(analysis, signals)
    
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

