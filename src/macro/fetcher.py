"""
Makroekonomik veri çekme modülü
USD/TRY, EUR/TRY, BIST100, Petrol, Altın verilerini yfinance'den çeker
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional
import json
import os


class MacroDataFetcher:
    """Makroekonomik verileri çeken ve yöneten sınıf"""
    
    def __init__(self, config_path: str = "config/macro_data.json"):
        self.config_path = config_path
        
        # Veri sembolleri
        self.symbols = {
            'usd_try': 'TRY=X',      # USD/TRY
            'eur_try': 'EURTRY=X',   # EUR/TRY
            'bist100': 'XU100.IS',   # BIST100 Endeksi
            'oil': 'CL=F',           # WTI Crude Oil
            'gold': 'GC=F'           # Gold Futures
        }
    
    def fetch_current_price(self, symbol: str) -> Optional[float]:
        """
        Bir sembol için güncel fiyat çeker
        
        Args:
            symbol: yfinance sembolü (örn: 'TRY=X')
            
        Returns:
            float: Güncel fiyat veya None
        """
        try:
            ticker = yf.Ticker(symbol)
            # Son 5 günlük veriyi çek (güncel fiyat için)
            hist = ticker.history(period='5d')
            
            if hist.empty:
                print(f"[WARN] {symbol} icin veri cekilemedi")
                return None
            
            # En son kapanış fiyatı
            current_price = hist['Close'].iloc[-1]
            return round(float(current_price), 2)
            
        except Exception as e:
            print(f"[ERROR] {symbol} verisi cekilirken hata: {e}")
            return None
    
    def fetch_price_change(self, symbol: str, days: int = 30) -> Optional[float]:
        """
        Belirli bir periyottaki fiyat değişimini hesaplar
        
        Args:
            symbol: yfinance sembolü
            days: Kaç gün öncesiyle karşılaştırılacak
            
        Returns:
            float: Yüzdesel değişim (örn: 3.5 = %3.5 artış)
        """
        try:
            ticker = yf.Ticker(symbol)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+5)  # Biraz buffer
            
            hist = ticker.history(start=start_date, end=end_date)
            
            if len(hist) < 2:
                return None
            
            old_price = hist['Close'].iloc[0]
            new_price = hist['Close'].iloc[-1]
            
            change_pct = ((new_price - old_price) / old_price) * 100
            return round(float(change_pct), 2)
            
        except Exception as e:
            print(f"[ERROR] {symbol} degisim hesaplanirken hata: {e}")
            return None
    
    def fetch_bist100_trend(self) -> str:
        """
        BIST100'ün trend durumunu belirler (up/down/flat)
        Son 20 günlük MA ile son 50 günlük MA karşılaştırması
        
        Returns:
            str: 'up', 'down', veya 'flat'
        """
        try:
            ticker = yf.Ticker(self.symbols['bist100'])
            hist = ticker.history(period='3mo')
            
            if len(hist) < 50:
                return 'flat'
            
            # 20 ve 50 günlük hareketli ortalamalar
            ma20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            ma50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            
            # Trend belirleme
            if ma20 > ma50 * 1.02:  # %2+ üstünde
                return 'up'
            elif ma20 < ma50 * 0.98:  # %2+ altında
                return 'down'
            else:
                return 'flat'
                
        except Exception as e:
            print(f"[ERROR] BIST100 trend hesaplanirken hata: {e}")
            return 'flat'
    
    def fetch_all_macro_data(self) -> Dict:
        """
        Tüm makroekonomik verileri çeker ve dict olarak döner
        
        Returns:
            Dict: Tüm makro veriler
        """
        print("[*] Makro veriler cekiliyor...")
        
        data = {
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'usd_try': {
                'current': self.fetch_current_price(self.symbols['usd_try']),
                'change_30d': self.fetch_price_change(self.symbols['usd_try'], 30)
            },
            'eur_try': {
                'current': self.fetch_current_price(self.symbols['eur_try']),
                'change_30d': self.fetch_price_change(self.symbols['eur_try'], 30)
            },
            'bist100': {
                'current': self.fetch_current_price(self.symbols['bist100']),
                'trend': self.fetch_bist100_trend(),
                'change_30d': self.fetch_price_change(self.symbols['bist100'], 30)
            },
            'oil': {
                'current': self.fetch_current_price(self.symbols['oil']),
                'change_30d': self.fetch_price_change(self.symbols['oil'], 30)
            },
            'gold': {
                'current': self.fetch_current_price(self.symbols['gold']),
                'change_30d': self.fetch_price_change(self.symbols['gold'], 30)
            },
            'tcmb_rate': None  # Manuel input gerekecek
        }
        
        print("[OK] Makro veriler cekildi!")
        return data
    
    def save_to_config(self, data: Dict) -> bool:
        """
        Makro verileri config/macro_data.json'a kaydeder
        
        Args:
            data: Kaydedilecek makro veriler
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            # Config klasörünü oluştur (yoksa)
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Veriler kaydedildi: {self.config_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Veriler kaydedilirken hata: {e}")
            return False
    
    def load_from_config(self) -> Optional[Dict]:
        """
        Config dosyasından makro verileri yükler
        
        Returns:
            Dict: Makro veriler veya None
        """
        try:
            if not os.path.exists(self.config_path):
                print(f"[WARN] Config dosyasi bulunamadi: {self.config_path}")
                return None
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"[OK] Veriler yuklendi: {self.config_path}")
            return data
            
        except Exception as e:
            print(f"[ERROR] Veriler yuklenirken hata: {e}")
            return None
    
    def update_tcmb_rate(self, rate: float) -> bool:
        """
        TCMB politika faizini manuel günceller
        
        Args:
            rate: Yeni faiz oranı (örn: 50.0)
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            # Mevcut veriyi yükle
            data = self.load_from_config()
            
            if data is None:
                # İlk kez oluşturuyoruz
                data = self.fetch_all_macro_data()
            
            # Faizi güncelle
            data['tcmb_rate'] = rate
            data['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Kaydet
            return self.save_to_config(data)
            
        except Exception as e:
            print(f"[ERROR] TCMB faizi guncellenirken hata: {e}")
            return False


# Test fonksiyonu
if __name__ == "__main__":
    fetcher = MacroDataFetcher()
    
    print("=" * 60)
    print("MAKRO VERİ ÇEKME TESTİ")
    print("=" * 60)
    
    # Tüm verileri çek
    data = fetcher.fetch_all_macro_data()
    
    print("\n📊 Çekilen Veriler:")
    print(f"USD/TRY: {data['usd_try']['current']} (Değişim 30g: %{data['usd_try']['change_30d']})")
    print(f"EUR/TRY: {data['eur_try']['current']} (Değişim 30g: %{data['eur_try']['change_30d']})")
    print(f"BIST100: {data['bist100']['current']} (Trend: {data['bist100']['trend']})")
    print(f"Petrol: ${data['oil']['current']} (Değişim 30g: %{data['oil']['change_30d']})")
    print(f"Altın: ${data['gold']['current']} (Değişim 30g: %{data['gold']['change_30d']})")
    
    # Kaydet
    fetcher.save_to_config(data)
    
    # Tekrar yükle (test)
    loaded_data = fetcher.load_from_config()
    print("\n✅ Veriler kaydedildi ve tekrar yüklendi!")

