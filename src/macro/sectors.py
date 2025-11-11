"""
Sektörel faktör analizi
Farklı sektörlerdeki hisseler için özel makro değerlendirmesi
"""

from typing import Dict, Tuple, Optional


class SectorAnalyzer:
    """Sektöre özel makro analiz yapan sınıf"""
    
    # Sektör tanımları (BIST hisseleri için)
    SECTORS = {
        # Havayolu şirketleri
        'airline': ['THYAO', 'PGSUS'],
        
        # Bankalar
        'bank': ['GARAN', 'AKBNK', 'ISCTR', 'YKBNK', 'HALKB', 'VAKBN'],
        
        # Holding'ler
        'holding': ['SAHOL', 'KCHOL', 'DOHOL', 'TAVHL'],
        
        # Enerji
        'energy': ['TUPRS', 'PETKM', 'PENTA', 'AKENR'],
        
        # Teknoloji
        'tech': ['ASELS', 'LOGO', 'NETAS', 'KAREL'],
        
        # İhracatçı sanayi
        'export': ['EREGL', 'ARCLK', 'VESTEL', 'FROTO', 'TOASO', 'SISE'],
        
        # İthalatçı perakende
        'retail': ['BIMAS', 'MGROS', 'SOKM', 'MAVI'],
        
        # Turizm
        'tourism': ['MAALT', 'AYCES', 'KSTUR'],
        
        # Telekom
        'telecom': ['TTKOM', 'TCELL', 'TURKCELL']
    }
    
    def __init__(self, macro_data: Dict):
        """
        Args:
            macro_data: Makroekonomik veriler (config/macro_data.json)
        """
        self.data = macro_data
    
    def get_sector(self, symbol: str) -> Optional[str]:
        """
        Bir hisse sembolünün sektörünü bulur
        
        Args:
            symbol: Hisse sembolü (örn: 'THYAO')
            
        Returns:
            str: Sektör adı veya None
        """
        # .IS suffix'ini temizle
        clean_symbol = symbol.replace('.IS', '').upper()
        
        for sector, stocks in self.SECTORS.items():
            if clean_symbol in stocks:
                return sector
        
        return None
    
    def analyze_airline_sector(self) -> Tuple[float, str]:
        """
        Havayolu sektörü için özel analiz
        
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        try:
            usd_change = self.data['usd_try']['change_30d']
            oil_change = self.data['oil']['change_30d']
            
            score = 0
            factors = []
            
            # USD/TRY yükselmesi havayolu için çok kötü (yakıt maliyeti)
            if usd_change is not None:
                if usd_change >= 5:
                    score -= 10
                    factors.append(f"Doviz cok yuksek (%{usd_change:.1f}) [-]")
                elif usd_change >= 2:
                    score -= 6
                    factors.append(f"Doviz yuksek (%{usd_change:.1f}) [!]")
                elif usd_change <= -2:
                    score += 6
                    factors.append(f"Doviz dusuyor (%{usd_change:.1f}) [+]")
            
            # Petrol yükselmesi de kötü
            if oil_change is not None:
                if oil_change >= 10:
                    score -= 6
                    factors.append(f"Petrol cok yuksek (%{oil_change:.1f}) [-]")
                elif oil_change >= 5:
                    score -= 3
                    factors.append(f"Petrol yuksek (%{oil_change:.1f}) [!]")
                elif oil_change <= -5:
                    score += 3
                    factors.append(f"Petrol dusuyor (%{oil_change:.1f}) [+]")
            
            # -10 ile +10 arasında tut
            score = max(-10, min(10, score))
            
            desc = "HAVACILIK: " + ", ".join(factors) if factors else "HAVACILIK: Veri yetersiz"
            return score, desc
            
        except Exception as e:
            return 0, f"Havacılık analiz hatası: {e}"
    
    def analyze_bank_sector(self) -> Tuple[float, str]:
        """
        Bankacılık sektörü için özel analiz
        
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        try:
            tcmb_rate = self.data.get('tcmb_rate')
            bist_change = self.data['bist100']['change_30d']
            
            score = 0
            factors = []
            
            # Yüksek faiz bankalar için iyi (marj)
            if tcmb_rate is not None:
                if tcmb_rate >= 50:
                    score += 4
                    factors.append(f"Yuksek faiz (%{tcmb_rate}) [+]")
                elif tcmb_rate >= 40:
                    score += 2
                    factors.append(f"Orta faiz (%{tcmb_rate}) [o]")
                else:
                    score -= 2
                    factors.append(f"Dusuk faiz (%{tcmb_rate}) [!]")
            
            # Ama ekonomi kötüyse kredi geri ödemeleri risk
            if bist_change is not None:
                if bist_change <= -10:
                    score -= 5
                    factors.append(f"Piyasa cok kotu (%{bist_change:.1f}) [-]")
                elif bist_change <= -5:
                    score -= 2
                    factors.append(f"Piyasa kotu (%{bist_change:.1f}) [!]")
            
            score = max(-10, min(10, score))
            
            desc = "BANKACILIK: " + ", ".join(factors) if factors else "BANKACILIK: Veri yetersiz"
            return score, desc
            
        except Exception as e:
            return 0, f"Bankacılık analiz hatası: {e}"
    
    def analyze_export_sector(self) -> Tuple[float, str]:
        """
        İhracatçı sanayi sektörü için özel analiz
        
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        try:
            usd_change = self.data['usd_try']['change_30d']
            eur_change = self.data['eur_try']['change_30d']
            
            score = 0
            factors = []
            
            # İhracatçılar için döviz yükselmesi OLUMLU
            if usd_change is not None:
                if usd_change >= 5:
                    score += 8
                    factors.append(f"Doviz cok yuksek (%{usd_change:.1f}) [+]")
                elif usd_change >= 2:
                    score += 5
                    factors.append(f"Doviz yuksek (%{usd_change:.1f}) [+]")
                elif usd_change <= -3:
                    score -= 5
                    factors.append(f"Doviz dusuyor (%{usd_change:.1f}) [!]")
            
            # EUR/TRY da önemli (Avrupa'ya ihracat)
            if eur_change is not None:
                if eur_change >= 3:
                    score += 4
                    factors.append(f"Euro yuksek (%{eur_change:.1f}) [+]")
                elif eur_change <= -3:
                    score -= 3
                    factors.append(f"Euro dusuyor (%{eur_change:.1f}) [!]")
            
            score = max(-10, min(10, score))
            
            desc = "İHRACATÇI SANAYİ: " + ", ".join(factors) if factors else "İHRACATÇI: Veri yetersiz"
            return score, desc
            
        except Exception as e:
            return 0, f"İhracatçı analiz hatası: {e}"
    
    def analyze_retail_sector(self) -> Tuple[float, str]:
        """
        Perakende sektörü için özel analiz
        
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        try:
            usd_change = self.data['usd_try']['change_30d']
            bist_change = self.data['bist100']['change_30d']
            
            score = 0
            factors = []
            
            # Perakende için döviz yükselmesi kötü (ithalat maliyeti)
            if usd_change is not None:
                if usd_change >= 5:
                    score -= 7
                    factors.append(f"Doviz cok yuksek (%{usd_change:.1f}) [-]")
                elif usd_change >= 2:
                    score -= 4
                    factors.append(f"Doviz yuksek (%{usd_change:.1f}) [!]")
                elif usd_change <= -2:
                    score += 4
                    factors.append(f"Doviz dusuyor (%{usd_change:.1f}) [+]")
            
            # Genel ekonomik durum da önemli (tüketici harcamaları)
            if bist_change is not None:
                if bist_change >= 5:
                    score += 3
                    factors.append(f"Piyasa iyi (%{bist_change:.1f}) [+]")
                elif bist_change <= -5:
                    score -= 3
                    factors.append(f"Piyasa kotu (%{bist_change:.1f}) [!]")
            
            score = max(-10, min(10, score))
            
            desc = "PERAKENDE: " + ", ".join(factors) if factors else "PERAKENDE: Veri yetersiz"
            return score, desc
            
        except Exception as e:
            return 0, f"Perakende analiz hatası: {e}"
    
    def analyze_sector_specific(self, symbol: str) -> Tuple[float, str]:
        """
        Bir hisse için sektöre özel analiz yapar
        
        Args:
            symbol: Hisse sembolü (örn: 'THYAO')
            
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        sector = self.get_sector(symbol)
        
        if sector is None:
            return 0, "Sektör bilgisi yok (genel makro analiz kullanılıyor)"
        
        # Sektöre göre özel analiz
        if sector == 'airline':
            return self.analyze_airline_sector()
        elif sector == 'bank':
            return self.analyze_bank_sector()
        elif sector == 'export':
            return self.analyze_export_sector()
        elif sector == 'retail':
            return self.analyze_retail_sector()
        else:
            # Diğer sektörler için henüz özel analiz yok
            return 0, f"Sektör: {sector.upper()} (genel makro analiz kullanılıyor)"


# Test fonksiyonu
if __name__ == "__main__":
    test_data = {
        'usd_try': {'current': 34.25, 'change_30d': 3.2},
        'eur_try': {'current': 37.80, 'change_30d': 2.8},
        'bist100': {'current': 9500, 'trend': 'down', 'change_30d': -5.5},
        'oil': {'current': 75.2, 'change_30d': 8.3},
        'gold': {'current': 2010.5, 'change_30d': 4.2},
        'tcmb_rate': 50.0
    }
    
    analyzer = SectorAnalyzer(test_data)
    
    print("=" * 60)
    print("SEKTÖREL ANALİZ TESTİ")
    print("=" * 60)
    
    test_stocks = ['THYAO', 'GARAN', 'EREGL', 'BIMAS', 'ASELS']
    
    for stock in test_stocks:
        sector = analyzer.get_sector(stock)
        score, desc = analyzer.analyze_sector_specific(stock)
        
        print(f"\n{stock}:")
        print(f"  Sektör: {sector if sector else 'Bilinmiyor'}")
        print(f"  Skor: {score:.1f}/10")
        print(f"  {desc}")

