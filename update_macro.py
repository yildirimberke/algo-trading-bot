"""
Makro Ekonomik Veri Güncelleme Scripti

Makroekonomik verileri günceller ve config/macro_data.json'a kaydeder.
"""

import argparse
import sys
from src.macro.fetcher import MacroDataFetcher
from src.reporting.terminal import print_macro_data_summary


def main():
    parser = argparse.ArgumentParser(
        description='Makroekonomik verileri guncelle',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ornekler:
  python update_macro.py                    # Tum verileri guncelle
  python update_macro.py --tcmb-rate 51.5   # TCMB faizini guncelle
  python update_macro.py --show             # Mevcut verileri goster
        """
    )
    
    parser.add_argument(
        '--tcmb-rate',
        type=float,
        help='TCMB politika faizini manuel guncelle (ornek: 50.0)'
    )
    
    parser.add_argument(
        '--show',
        action='store_true',
        help='Mevcut makro verileri goster (guncelleme yapma)'
    )
    
    args = parser.parse_args()
    
    fetcher = MacroDataFetcher()
    
    # Sadece gösterme modu
    if args.show:
        print("Mevcut makro veriler yukleniyor...")
        data = fetcher.load_from_config()
        
        if data is None:
            print("[WARN] Henuz makro veri yok. Guncellemek icin: python update_macro.py")
            sys.exit(1)
        
        print_macro_data_summary(data)
        sys.exit(0)
    
    # TCMB faizi güncelleme
    if args.tcmb_rate is not None:
        print(f"TCMB faizi guncelleniyor: %{args.tcmb_rate}")
        success = fetcher.update_tcmb_rate(args.tcmb_rate)
        
        if success:
            print("[OK] TCMB faizi guncellendi!")
            data = fetcher.load_from_config()
            print_macro_data_summary(data)
        else:
            print("[ERROR] TCMB faizi guncellenemedi!")
            sys.exit(1)
        
        sys.exit(0)
    
    # Tam güncelleme
    print("=" * 70)
    print("MAKRO EKONOMİK VERİ GÜNCELLEMESİ")
    print("=" * 70)
    print("\nTum makro veriler yfinance'den cekiliyor...")
    print("(Bu birkaç saniye surebilir)\n")
    
    data = fetcher.fetch_all_macro_data()
    
    if data:
        success = fetcher.save_to_config(data)
        
        if success:
            print("\n[OK] Tum makro veriler guncellendi!\n")
            print_macro_data_summary(data)
            
            # TCMB faizi uyarısı
            if data.get('tcmb_rate') is None:
                print(f"\n[WARN] UYARI: TCMB faizi manuel girilmeli!")
                print(f"Guncellemek icin: python update_macro.py --tcmb-rate 50.0")
        else:
            print("\n[ERROR] Veriler kaydedilemedi!")
            sys.exit(1)
    else:
        print("\n[ERROR] Veriler cekilemedi!")
        sys.exit(1)


if __name__ == "__main__":
    main()

