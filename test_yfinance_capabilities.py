"""
yfinance Yetenekleri Test Scripti

Yahoo Finance web sitesi ile yfinance kütüphanesinin
çekebildiği verileri karşılaştırır.
"""

import yfinance as yf
import json

def test_yfinance_data(symbol="THYAO.IS"):
    """yfinance'in çekebildiği tüm verileri test et"""
    
    print("=" * 70)
    print(f"yfinance YETENEK TESTI: {symbol}")
    print("=" * 70)
    
    ticker = yf.Ticker(symbol)
    
    # 1. Geçmiş Fiyat Verileri
    print("\n[TEST 1] Gecmis Fiyat Verileri")
    print("-" * 70)
    try:
        hist = ticker.history(period="5d")
        if not hist.empty:
            print(f"BASARILI: {len(hist)} gun verisi cekildi")
            print(f"Kolonlar: {list(hist.columns)}")
            print(f"Son fiyat: {hist['Close'].iloc[-1]:.2f} TL")
            print(f"Son tarih: {hist.index[-1].date()}")
        else:
            print("BASARISIZ: Veri gelmedi")
    except Exception as e:
        print(f"HATA: {e}")
    
    # 2. Hisse Bilgileri (Info)
    print("\n[TEST 2] Hisse Bilgileri (info)")
    print("-" * 70)
    try:
        info = ticker.info
        if info:
            print("BASARILI: Bilgiler cekildi")
            
            # Önemli alanlar
            key_fields = [
                'longName', 'sector', 'industry', 'marketCap', 
                'currency', 'exchange', 'website', 'employees',
                'previousClose', 'open', 'dayHigh', 'dayLow',
                'volume', 'averageVolume', 'fiftyTwoWeekHigh', 
                'fiftyTwoWeekLow', 'trailingPE', 'forwardPE'
            ]
            
            available = 0
            missing = 0
            
            for field in key_fields:
                if field in info and info[field] is not None:
                    print(f"  OK: {field} = {info[field]}")
                    available += 1
                else:
                    print(f"  YOK: {field}")
                    missing += 1
            
            print(f"\nToplam: {available} mevcut, {missing} eksik")
        else:
            print("BASARISIZ: Bilgi gelmedi")
    except Exception as e:
        print(f"HATA: {e}")
    
    # 3. Finansal Tablolar
    print("\n[TEST 3] Finansal Tablolar")
    print("-" * 70)
    
    # Balance Sheet
    try:
        bs = ticker.balance_sheet
        if bs is not None and not bs.empty:
            print(f"  OK: Balance Sheet (Bilanco) - {bs.shape[0]} satir, {bs.shape[1]} sutun")
        else:
            print("  YOK: Balance Sheet")
    except Exception as e:
        print(f"  HATA: Balance Sheet - {e}")
    
    # Income Statement
    try:
        inc = ticker.financials
        if inc is not None and not inc.empty:
            print(f"  OK: Income Statement (Gelir Tablosu) - {inc.shape[0]} satir, {inc.shape[1]} sutun")
        else:
            print("  YOK: Income Statement")
    except Exception as e:
        print(f"  HATA: Income Statement - {e}")
    
    # Cash Flow
    try:
        cf = ticker.cashflow
        if cf is not None and not cf.empty:
            print(f"  OK: Cash Flow - {cf.shape[0]} satir, {cf.shape[1]} sutun")
        else:
            print("  YOK: Cash Flow")
    except Exception as e:
        print(f"  HATA: Cash Flow - {e}")
    
    # 4. Temettü
    print("\n[TEST 4] Temettü (Dividends)")
    print("-" * 70)
    try:
        divs = ticker.dividends
        if divs is not None and len(divs) > 0:
            print(f"BASARILI: {len(divs)} temettü kaydi")
            print(f"Son temettü: {divs.iloc[-1]} ({divs.index[-1].date()})")
        else:
            print("YOK: Temettü verisi yok (veya hisse temettü vermiyor)")
    except Exception as e:
        print(f"HATA: {e}")
    
    # 5. Analist Tavsiyeleri
    print("\n[TEST 5] Analist Tavsiyeleri")
    print("-" * 70)
    try:
        rec = ticker.recommendations
        if rec is not None and not rec.empty:
            print(f"BASARILI: {len(rec)} tavsiye kaydi")
            print(rec.tail())
        else:
            print("YOK: Tavsiye verisi yok")
    except Exception as e:
        print(f"HATA: {e}")
    
    # 6. Haberler
    print("\n[TEST 6] Haberler")
    print("-" * 70)
    try:
        news = ticker.news
        if news and len(news) > 0:
            print(f"BASARILI: {len(news)} haber")
            for i, n in enumerate(news[:3], 1):
                print(f"  {i}. {n.get('title', 'Baslik yok')}")
        else:
            print("YOK: Haber verisi yok")
    except Exception as e:
        print(f"HATA: {e}")
    
    # Özet
    print("\n" + "=" * 70)
    print("SONUC OZETI")
    print("=" * 70)
    print("""
yfinance YAPABILIR:
  OK - Gecmis fiyat verileri (OHLCV)
  OK - Temel hisse bilgileri (isim, sektor, vs.)
  KISITLI - Finansal tablolar (olmayabilir)
  KISITLI - Temettü (varsa)
  
yfinance YAPAMAZ/SINIRLI:
  X - Gercek zamanli veriler (15-20 dk gecikme)
  X - Detayli haberler
  X - Teknik gostergeler (kendimiz hesapliyoruz)
  X - Analist tavsiyeleri (cok sinirli)
    """)
    print("=" * 70)


if __name__ == "__main__":
    test_yfinance_data("THYAO.IS")
    
    print("\n\n[BILGI] Baska hisseler icin:")
    print("  python test_yfinance_capabilities.py")
    print("  Sonra kodu duzenlleyip baska sembol deneyin")

