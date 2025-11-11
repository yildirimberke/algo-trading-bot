"""
Makroekonomik analiz ve puanlama motoru
Makro verileri analiz edip -10 ile +10 arası skor üretir
"""

from typing import Dict, Tuple, Optional


class MacroAnalyzer:
    """Makroekonomik verileri analiz eden ve puanlayan sınıf"""
    
    def __init__(self, macro_data: Dict):
        """
        Args:
            macro_data: config/macro_data.json'dan yüklenen veriler
        """
        self.data = macro_data
    
    def analyze_usd_try(self) -> Tuple[float, str]:
        """
        USD/TRY değişimini analiz eder (Hibrid: Seviye + Momentum)
        
        Returns:
            Tuple[float, str]: (skor, açıklama)
                skor: -10 ile +10 arası
        """
        try:
            change = self.data['usd_try']['change_30d']
            current = self.data['usd_try']['current']
            
            if change is None or current is None:
                return 0, "USD/TRY verisi eksik"
            
            # 1) Mutlak Seviye Değerlendirmesi (Baz Risk)
            level_score = 0
            level_desc = ""
            
            if current >= 50:
                level_score = -5
                level_desc = "Cok yuksek seviye (50+)"
            elif current >= 45:
                level_score = -4
                level_desc = "Yuksek seviye (45+)"
            elif current >= 40:
                level_score = -2
                level_desc = "Orta-yuksek seviye (40+)"
            elif current >= 35:
                level_score = -1
                level_desc = "Orta seviye (35+)"
            elif current >= 30:
                level_score = 0
                level_desc = "Normal seviye (30+)"
            else:
                level_score = +1
                level_desc = "Dusuk seviye (<30)"
            
            # 2) Momentum Değerlendirmesi (30 günlük değişim)
            momentum_score = 0
            momentum_desc = ""
            
            if change >= 5:
                momentum_score = -6
                momentum_desc = f"Cok hizli yukselis (+%{change:.1f})"
            elif change >= 3:
                momentum_score = -4
                momentum_desc = f"Hizli yukselis (+%{change:.1f})"
            elif change >= 1.5:
                momentum_score = -2
                momentum_desc = f"Yukselis (+%{change:.1f})"
            elif change >= 0.5:
                momentum_score = -1
                momentum_desc = f"Hafif yukselis (+%{change:.1f})"
            elif change >= -0.5:
                momentum_score = 0
                momentum_desc = f"Stabil (%{change:.1f})"
            elif change >= -1.5:
                momentum_score = +1
                momentum_desc = f"Hafif dusus (%{change:.1f})"
            elif change >= -3:
                momentum_score = +2
                momentum_desc = f"Dusus (%{change:.1f})"
            else:
                momentum_score = +4
                momentum_desc = f"Hizli dusus (%{change:.1f})"
            
            # 3) Seviye-Momentum İnteraksiyonu
            # Yüksek seviyelerde momentum daha kritik
            if current >= 40 and change > 0:
                momentum_score *= 1.3  # %30 daha agresif
            elif current < 35 and change < 0:
                momentum_score *= 0.7  # %30 daha yumuşak
            
            # 4) Final Skor
            total_score = level_score + momentum_score
            total_score = max(-10, min(10, total_score))  # -10/+10 arası tut
            
            # 5) Açıklama
            direction = "[-]" if total_score < -2 else "[!]" if total_score < 2 else "[+]"
            desc = f"USD/TRY {current:.1f} TL ({level_desc}, {momentum_desc}) {direction}"
            
            return round(total_score, 1), desc
            
        except Exception as e:
            return 0, f"USD/TRY analiz hatası: {e}"
    
    def analyze_tcmb_rate(self, previous_rate: Optional[float] = None) -> Tuple[float, str]:
        """
        TCMB faiz politikasını analiz eder (Hibrid: Seviye + Değişim)
        
        Args:
            previous_rate: Önceki faiz oranı (varsa)
            
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        try:
            current_rate = self.data.get('tcmb_rate')
            
            if current_rate is None:
                return 0, "TCMB faizi girilmemis (notr kabul)"
            
            # 1) Mutlak Seviye Değerlendirmesi
            # Yüksek faiz = sıkı para politikası = BIST için olumsuz (kısa vadede)
            # Ama enflasyonu kontrol ederse uzun vadede iyi
            level_score = 0
            level_desc = ""
            
            if current_rate >= 55:
                level_score = -4
                level_desc = "Cok yuksek faiz (55+)"
            elif current_rate >= 50:
                level_score = -3
                level_desc = "Yuksek faiz (50+)"
            elif current_rate >= 45:
                level_score = -2
                level_desc = "Orta-yuksek faiz (45+)"
            elif current_rate >= 40:
                level_score = -1
                level_desc = "Orta faiz (40+)"
            elif current_rate >= 30:
                level_score = 0
                level_desc = "Normal faiz (30+)"
            else:
                level_score = +1
                level_desc = "Dusuk faiz (<30)"
            
            # 2) Değişim Değerlendirmesi (eğer önceki oran biliniyorsa)
            change_score = 0
            change_desc = ""
            
            if previous_rate is not None:
                change = current_rate - previous_rate
                
                if change >= 5:
                    change_score = -5
                    change_desc = f"Cok artti (+%{change:.1f})"
                elif change >= 2:
                    change_score = -3
                    change_desc = f"Artti (+%{change:.1f})"
                elif change >= 0.5:
                    change_score = -1
                    change_desc = f"Hafif artti (+%{change:.1f})"
                elif change >= -0.5:
                    change_score = 0
                    change_desc = "Sabit"
                elif change >= -2:
                    change_score = +1
                    change_desc = f"Hafif dustu (%{change:.1f})"
                elif change >= -5:
                    change_score = +3
                    change_desc = f"Dustu (%{change:.1f})"
                else:
                    change_score = +5
                    change_desc = f"Cok dustu (%{change:.1f})"
            else:
                change_desc = "Degisim bilinmiyor"
            
            # 3) Seviye-Değişim İnteraksiyonu
            # Yüksek seviyede artış daha kötü
            if current_rate >= 50 and change_score < 0:
                change_score *= 1.2
            
            # 4) Final Skor
            total_score = level_score + change_score
            total_score = max(-10, min(10, total_score))
            
            # 5) Açıklama
            direction = "[-]" if total_score < -2 else "[!]" if total_score < 2 else "[+]"
            if previous_rate:
                desc = f"TCMB %{current_rate} ({level_desc}, {change_desc}) {direction}"
            else:
                desc = f"TCMB %{current_rate} ({level_desc}) {direction}"
            
            return round(total_score, 1), desc
            
        except Exception as e:
            return 0, f"TCMB analiz hatası: {e}"
    
    def analyze_bist100(self) -> Tuple[float, str]:
        """
        BIST100 endeks trendini analiz eder
        
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        try:
            trend = self.data['bist100']['trend']
            change = self.data['bist100']['change_30d']
            current = self.data['bist100']['current']
            
            # Trend bazlı puanlama
            if trend == 'up':
                base_score = +6
                emoji = "[+]"
                trend_desc = "yukselis trendinde"
            elif trend == 'down':
                base_score = -6
                emoji = "[-]"
                trend_desc = "dusus trendinde"
            else:
                base_score = 0
                emoji = "[o]"
                trend_desc = "yatay seyrediyor"
            
            # Değişim oranına göre ayarlama
            if change is not None:
                if abs(change) > 10:
                    # Çok keskin hareket - skoru güçlendir
                    base_score = base_score * 1.3
                    desc = f"BIST100 {trend_desc} ve son 30 gunde %{change:.1f} degisti {emoji}"
                else:
                    desc = f"BIST100 {trend_desc} (son 30g: %{change:.1f}) {emoji}"
            else:
                desc = f"BIST100 {trend_desc} {emoji}"
            
            return round(base_score, 1), desc
            
        except Exception as e:
            return 0, f"BIST100 analiz hatası: {e}"
    
    def analyze_oil(self) -> Tuple[float, str]:
        """
        Petrol fiyatlarını analiz eder (Hibrid: Seviye + Momentum)
        
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        try:
            change = self.data['oil']['change_30d']
            current = self.data['oil']['current']
            
            if change is None or current is None:
                return 0, "Petrol verisi eksik"
            
            # 1) Mutlak Seviye Değerlendirmesi
            level_score = 0
            level_desc = ""
            
            if current >= 100:
                level_score = -3
                level_desc = "Cok yuksek ($100+)"
            elif current >= 85:
                level_score = -2
                level_desc = "Yuksek ($85+)"
            elif current >= 75:
                level_score = -1
                level_desc = "Orta-yuksek ($75+)"
            elif current >= 60:
                level_score = 0
                level_desc = "Normal ($60+)"
            elif current >= 50:
                level_score = +1
                level_desc = "Dusuk ($50+)"
            else:
                level_score = +2
                level_desc = "Cok dusuk (<$50)"
            
            # 2) Momentum Değerlendirmesi
            momentum_score = 0
            momentum_desc = ""
            
            if change >= 20:
                momentum_score = -3
                momentum_desc = f"Cok hizli yukselis (+%{change:.1f})"
            elif change >= 10:
                momentum_score = -2
                momentum_desc = f"Hizli yukselis (+%{change:.1f})"
            elif change >= 5:
                momentum_score = -1
                momentum_desc = f"Yukselis (+%{change:.1f})"
            elif change >= -5:
                momentum_score = 0
                momentum_desc = f"Stabil (%{change:.1f})"
            elif change >= -10:
                momentum_score = +1
                momentum_desc = f"Dusus (%{change:.1f})"
            elif change >= -20:
                momentum_score = +2
                momentum_desc = f"Hizli dusus (%{change:.1f})"
            else:
                momentum_score = +3
                momentum_desc = f"Cok hizli dusus (%{change:.1f})"
            
            # 3) Seviye-Momentum İnteraksiyonu
            # Yüksek seviyede artış enflasyon için çok kötü
            if current >= 85 and change > 5:
                momentum_score *= 1.4
            
            # 4) Final Skor
            total_score = level_score + momentum_score
            total_score = max(-10, min(10, total_score))
            
            # 5) Açıklama
            direction = "[-]" if total_score < -1.5 else "[!]" if total_score < 1.5 else "[+]"
            desc = f"Petrol ${current:.1f} ({level_desc}, {momentum_desc}) {direction}"
            
            return round(total_score, 1), desc
            
        except Exception as e:
            return 0, f"Petrol analiz hatası: {e}"
    
    def analyze_gold(self) -> Tuple[float, str]:
        """
        Altın fiyatlarını analiz eder (Hibrid: Seviye + Momentum)
        Risk iştahı göstergesi
        
        Returns:
            Tuple[float, str]: (skor, açıklama)
        """
        try:
            change = self.data['gold']['change_30d']
            current = self.data['gold']['current']
            
            if change is None or current is None:
                return 0, "Altin verisi eksik"
            
            # 1) Mutlak Seviye Değerlendirmesi
            # Yüksek altın = güvensizlik/risk kaçışı = hisse için olumsuz
            level_score = 0
            level_desc = ""
            
            if current >= 2400:
                level_score = -2
                level_desc = "Cok yuksek ($2400+) - Risk kacisi"
            elif current >= 2200:
                level_score = -1.5
                level_desc = "Yuksek ($2200+) - Temkinli"
            elif current >= 2000:
                level_score = -0.5
                level_desc = "Orta-yuksek ($2000+)"
            elif current >= 1800:
                level_score = 0
                level_desc = "Normal ($1800+)"
            elif current >= 1600:
                level_score = +0.5
                level_desc = "Dusuk ($1600+)"
            else:
                level_score = +1
                level_desc = "Cok dusuk (<$1600)"
            
            # 2) Momentum Değerlendirmesi
            momentum_score = 0
            momentum_desc = ""
            
            if change >= 15:
                momentum_score = -2.5
                momentum_desc = f"Cok hizli yukselis (+%{change:.1f})"
            elif change >= 8:
                momentum_score = -1.5
                momentum_desc = f"Hizli yukselis (+%{change:.1f})"
            elif change >= 3:
                momentum_score = -0.5
                momentum_desc = f"Yukselis (+%{change:.1f})"
            elif change >= -3:
                momentum_score = 0
                momentum_desc = f"Stabil (%{change:.1f})"
            elif change >= -8:
                momentum_score = +0.5
                momentum_desc = f"Dusus (%{change:.1f})"
            elif change >= -15:
                momentum_score = +1.5
                momentum_desc = f"Hizli dusus (%{change:.1f})"
            else:
                momentum_score = +2.5
                momentum_desc = f"Cok hizli dusus (%{change:.1f})"
            
            # 3) Seviye-Momentum İnteraksiyonu
            # Zaten yüksek seviyede hızlı yükseliş = panik
            if current >= 2200 and change > 8:
                momentum_score *= 1.5
            
            # 4) Final Skor
            total_score = level_score + momentum_score
            total_score = max(-10, min(10, total_score))
            
            # 5) Açıklama
            direction = "[-]" if total_score < -1.5 else "[!]" if total_score < 1.5 else "[+]"
            desc = f"Altin ${current:.1f} ({level_desc}, {momentum_desc}) {direction}"
            
            return round(total_score, 1), desc
            
        except Exception as e:
            return 0, f"Altin analiz hatası: {e}"
    
    def calculate_overall_macro_score(self) -> Dict:
        """
        Tüm makro faktörleri analiz edip genel skor hesaplar
        
        Returns:
            Dict: {
                'total_score': -10 ile +10 arası,
                'components': Her faktörün detayı,
                'summary': Özet açıklama
            }
        """
        # Her faktörü analiz et
        usd_score, usd_desc = self.analyze_usd_try()
        tcmb_score, tcmb_desc = self.analyze_tcmb_rate()
        bist_score, bist_desc = self.analyze_bist100()
        oil_score, oil_desc = self.analyze_oil()
        gold_score, gold_desc = self.analyze_gold()
        
        # Ağırlıklı ortalama hesapla
        # USD/TRY ve BIST100 en önemli faktörler (Türkiye için)
        weights = {
            'usd': 0.30,   # %30
            'tcmb': 0.25,  # %25
            'bist': 0.30,  # %30
            'oil': 0.10,   # %10
            'gold': 0.05   # %5
        }
        
        total = (
            usd_score * weights['usd'] +
            tcmb_score * weights['tcmb'] +
            bist_score * weights['bist'] +
            oil_score * weights['oil'] +
            gold_score * weights['gold']
        )
        
        # -10 ile +10 arasında tut
        total = max(-10, min(10, total))
        
        # Özet oluştur
        if total >= 5:
            summary = "[+] Makroekonomik ortam OLUMLU - BIST icin destekleyici"
        elif total >= 2:
            summary = "[+] Makroekonomik ortam HAFIF OLUMLU - Dikkatli iyimserlik"
        elif total >= -2:
            summary = "[o] Makroekonomik ortam NOTR - Karma sinyaller"
        elif total >= -5:
            summary = "[!] Makroekonomik ortam HAFIF OLUMSUZ - Risk var"
        else:
            summary = "[-] Makroekonomik ortam OLUMSUZ - Yuksek risk"
        
        return {
            'total_score': round(total, 2),
            'normalized_score': round((total + 10) * 5, 1),  # 0-100 skalasına normalize
            'components': {
                'usd_try': {'score': usd_score, 'description': usd_desc, 'weight': weights['usd']},
                'tcmb_rate': {'score': tcmb_score, 'description': tcmb_desc, 'weight': weights['tcmb']},
                'bist100': {'score': bist_score, 'description': bist_desc, 'weight': weights['bist']},
                'oil': {'score': oil_score, 'description': oil_desc, 'weight': weights['oil']},
                'gold': {'score': gold_score, 'description': gold_desc, 'weight': weights['gold']}
            },
            'summary': summary,
            'last_update': self.data.get('last_update', 'Bilinmiyor')
        }


# Test fonksiyonu
if __name__ == "__main__":
    # Örnek test verisi
    test_data = {
        'last_update': '2025-11-11',
        'usd_try': {'current': 34.25, 'change_30d': 3.2},
        'eur_try': {'current': 37.80, 'change_30d': 2.8},
        'bist100': {'current': 9500, 'trend': 'down', 'change_30d': -5.5},
        'oil': {'current': 75.2, 'change_30d': 8.3},
        'gold': {'current': 2010.5, 'change_30d': 4.2},
        'tcmb_rate': 50.0
    }
    
    analyzer = MacroAnalyzer(test_data)
    result = analyzer.calculate_overall_macro_score()
    
    print("=" * 60)
    print("MAKRO ANALİZ TESTİ")
    print("=" * 60)
    print(f"\n📊 GENEL SKOR: {result['total_score']}/10")
    print(f"📊 NORMALİZE SKOR: {result['normalized_score']}/100")
    print(f"\n{result['summary']}\n")
    print("-" * 60)
    print("DETAYLAR:")
    print("-" * 60)
    
    for key, comp in result['components'].items():
        print(f"\n{key.upper()}:")
        print(f"  Skor: {comp['score']:.1f}/10 (Ağırlık: %{comp['weight']*100:.0f})")
        print(f"  {comp['description']}")

