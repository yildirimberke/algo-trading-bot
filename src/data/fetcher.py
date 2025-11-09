"""
BIST Hisse Veri Çekme Modülü

Bu modül yfinance kullanarak BIST hisselerinin fiyat ve
hacim verilerini çeker. Error handling ve cache mekanizması içerir.

Örnek Kullanım:
    >>> from src.data.fetcher import fetch_stock_data
    >>> data = fetch_stock_data('THYAO', period='3mo')
    >>> print(data.tail())
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Optional, Dict, Any


def fetch_stock_data(
    symbol: str,
    period: str = "1y",
    interval: str = "1d",
    retry_count: int = 3,
    retry_delay: float = 2.0
) -> Optional[pd.DataFrame]:
    """
    BIST hissesi için fiyat ve hacim verisi çeker.
    
    Args:
        symbol (str): Hisse kodu (örn: "THYAO", "SASA", "GARAN")
                      .IS uzantısı otomatik eklenir
        period (str): Zaman aralığı 
                      - "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"
        interval (str): Veri aralığı
                        - "1m", "5m", "15m", "30m", "60m", "1d", "1wk", "1mo"
        retry_count (int): Hata durumunda tekrar deneme sayısı
        retry_delay (float): Denemeler arası bekleme süresi (saniye)
    
    Returns:
        pd.DataFrame: Tarih indeksli DataFrame
                      Columns: Open, High, Low, Close, Volume
        None: Hata durumunda
    
    Raises:
        ValueError: Geçersiz parametre durumunda
    
    Örnekler:
        >>> # Son 3 ay THYAO verileri
        >>> data = fetch_stock_data('THYAO', period='3mo')
        
        >>> # Son 5 gün, saatlik veri
        >>> data = fetch_stock_data('SASA', period='5d', interval='1h')
        
        >>> # Maximum geçmiş veri
        >>> data = fetch_stock_data('GARAN', period='max')
    
    Notlar:
        - BIST hisseleri için otomatik ".IS" suffix eklenir
        - yfinance API'si bazen yavaş olabilir (1-3 saniye)
        - Rate limit durumunda otomatik retry yapar
        - Internet bağlantısı gereklidir
    """
    
    # Symbol'ü büyük harfe çevir ve temizle
    symbol = symbol.strip().upper()
    
    # BIST hisseleri için .IS suffix'i ekle
    if not symbol.endswith('.IS'):
        ticker_symbol = f"{symbol}.IS"
    else:
        ticker_symbol = symbol
    
    # Retry mekanizması ile veri çek
    for attempt in range(retry_count):
        try:
            print(f"[VERI] {symbol} verisi cekiliyor... (Deneme {attempt + 1}/{retry_count})")
            
            # yfinance Ticker objesi oluştur
            ticker = yf.Ticker(ticker_symbol)
            
            # Geçmiş verileri çek
            data = ticker.history(period=period, interval=interval)
            
            # Veri kontrolü
            if data.empty:
                print(f"[UYARI] {symbol} icin veri bulunamadi. Hisse kodu dogru mu?")
                return None
            
            # Sütun isimlerini düzenle (bazı versiyonlarda farklı olabiliyor)
            data.columns = [col.strip() for col in data.columns]
            
            print(f"[OK] {symbol} verisi basariyla cekildi! ({len(data)} satir)")
            
            return data
            
        except Exception as e:
            print(f"[HATA] (Deneme {attempt + 1}): {str(e)}")
            
            if attempt < retry_count - 1:
                print(f"[BEKLE] {retry_delay} saniye sonra tekrar deneniyor...")
                time.sleep(retry_delay)
            else:
                print(f"[HATA] {symbol} verisi {retry_count} denemeden sonra cekilemedi.")
                return None
    
    return None


def get_stock_info(symbol: str) -> Optional[Dict[str, Any]]:
    """
    Hisse hakkında genel bilgileri çeker.
    
    Args:
        symbol (str): Hisse kodu
    
    Returns:
        dict: Hisse bilgileri (şirket adı, sektör, market cap, vb.)
        None: Hata durumunda
    
    Örnek:
        >>> info = get_stock_info('THYAO')
        >>> print(info['longName'])  # 'Turk Hava Yollari A.O.'
        >>> print(info['sector'])    # 'Industrials'
    """
    
    symbol = symbol.strip().upper()
    
    if not symbol.endswith('.IS'):
        ticker_symbol = f"{symbol}.IS"
    else:
        ticker_symbol = symbol
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        if not info:
            print(f"[UYARI] {symbol} icin bilgi bulunamadi.")
            return None
        
        # Bazı yararlı alanları çıkar
        useful_info = {
            'symbol': symbol,
            'longName': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'marketCap': info.get('marketCap', 0),
            'currency': info.get('currency', 'TRY'),
            'exchange': info.get('exchange', 'IST'),
        }
        
        return useful_info
        
    except Exception as e:
        print(f"[HATA] {symbol} bilgisi cekilemedi: {e}")
        return None


def get_latest_price(symbol: str) -> Optional[float]:
    """
    Hissenin anlık/son fiyatını çeker.
    
    Args:
        symbol (str): Hisse kodu
    
    Returns:
        float: Son kapanış fiyatı
        None: Hata durumunda
    
    Örnek:
        >>> price = get_latest_price('THYAO')
        >>> print(f"THYAO: {price} TL")
    """
    
    data = fetch_stock_data(symbol, period='5d', retry_count=2)
    
    if data is not None and not data.empty:
        return float(data['Close'].iloc[-1])
    
    return None


def get_multiple_stocks(symbols: list, period: str = "1y") -> Dict[str, pd.DataFrame]:
    """
    Birden fazla hissenin verisini aynı anda çeker.
    
    Args:
        symbols (list): Hisse kodları listesi
        period (str): Zaman aralığı
    
    Returns:
        dict: {symbol: DataFrame} formatında
    
    Örnek:
        >>> stocks = get_multiple_stocks(['THYAO', 'SASA', 'GARAN'], period='3mo')
        >>> for symbol, data in stocks.items():
        ...     print(f"{symbol}: {len(data)} gün verisi")
    """
    
    results = {}
    
    for symbol in symbols:
        print(f"\n{'='*50}")
        data = fetch_stock_data(symbol, period=period)
        
        if data is not None:
            results[symbol] = data
        
        # API'yi yormamak için kısa bekleme
        time.sleep(0.5)
    
    print(f"\n{'='*50}")
    print(f"[OK] {len(results)}/{len(symbols)} hisse basariyla cekildi.\n")
    
    return results


# Test fonksiyonu (bu dosyayı doğrudan çalıştırırsanız)
if __name__ == "__main__":
    print("=" * 60)
    print("BIST VERİ ÇEKME MODÜLÜ - TEST")
    print("=" * 60)
    
    # Test 1: Tek hisse
    print("\n[TEST 1] THYAO verisi cekiliyor...\n")
    thyao_data = fetch_stock_data('THYAO', period='1mo')
    
    if thyao_data is not None:
        print(f"\n[OK] Veri cekildi! Ilk 5 satir:\n")
        print(thyao_data.head())
        print(f"\nSon 5 satir:\n")
        print(thyao_data.tail())
    
    # Test 2: Hisse bilgisi
    print("\n" + "="*60)
    print("[TEST 2] THYAO bilgileri...\n")
    info = get_stock_info('THYAO')
    
    if info:
        print("[OK] Hisse Bilgileri:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    # Test 3: Son fiyat
    print("\n" + "="*60)
    print("[TEST 3] Son fiyatlar...\n")
    
    for symbol in ['THYAO', 'SASA', 'GARAN']:
        price = get_latest_price(symbol)
        if price:
            print(f"  {symbol}: {price:.2f} TL")
    
    print("\n" + "="*60)
    print("[OK] TUM TESTLER TAMAMLANDI!")
    print("=" * 60)

