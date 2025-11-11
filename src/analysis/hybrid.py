"""
Hibrid analiz motoru
Teknik analiz + Makroekonomik analiz birleştirme
"""

from typing import Dict, Optional
from ..macro.analyzer import MacroAnalyzer
from ..macro.sectors import SectorAnalyzer


class HybridAnalyzer:
    """Teknik ve makro analizi birleştiren sınıf"""
    
    def __init__(self, technical_score: float, macro_data: Dict, symbol: str):
        """
        Args:
            technical_score: Teknik analiz skoru (0-100)
            macro_data: Makroekonomik veriler
            symbol: Hisse sembolü (örn: 'THYAO')
        """
        self.technical_score = technical_score
        self.macro_data = macro_data
        self.symbol = symbol
        
        # Makro analizörleri
        self.macro_analyzer = MacroAnalyzer(macro_data)
        self.sector_analyzer = SectorAnalyzer(macro_data)
    
    def calculate_hybrid_score(self, 
                               technical_weight: float = 0.70,
                               macro_weight: float = 0.30) -> Dict:
        """
        Teknik ve makro skorları birleştirip hibrid skor hesaplar
        
        Args:
            technical_weight: Teknik analizin ağırlığı (0-1 arası, default: 0.70)
            macro_weight: Makro analizin ağırlığı (0-1 arası, default: 0.30)
            
        Returns:
            Dict: Hibrid analiz sonuçları
        """
        # Ağırlıkları normalize et (toplamı 1 olsun)
        total_weight = technical_weight + macro_weight
        technical_weight = technical_weight / total_weight
        macro_weight = macro_weight / total_weight
        
        # Genel makro analiz
        macro_result = self.macro_analyzer.calculate_overall_macro_score()
        macro_score_raw = macro_result['total_score']  # -10 ile +10 arası
        macro_score_normalized = macro_result['normalized_score']  # 0-100 arası
        
        # Sektöre özel analiz
        sector_score, sector_desc = self.sector_analyzer.analyze_sector_specific(self.symbol)
        sector = self.sector_analyzer.get_sector(self.symbol)
        
        # Sektörel skoru makro skora ekle (ağırlık: 0.3)
        combined_macro_score = (macro_score_raw * 0.7) + (sector_score * 0.3)
        combined_macro_normalized = (combined_macro_score + 10) * 5  # 0-100'e normalize
        
        # Final hibrid skor
        hybrid_score = (
            self.technical_score * technical_weight +
            combined_macro_normalized * macro_weight
        )
        
        # 0-100 arasında tut
        hybrid_score = max(0, min(100, hybrid_score))
        
        # Sinyal belirleme
        if hybrid_score >= 65:
            signal = 'AL'
            signal_emoji = '[+]'
            confidence = 'YÜKSEK'
        elif hybrid_score >= 50:
            signal = 'AL'
            signal_emoji = '[+]'
            confidence = 'ORTA'
        elif hybrid_score >= 40:
            signal = 'BEK'
            signal_emoji = '[o]'
            confidence = 'DÜŞÜK'
        elif hybrid_score >= 25:
            signal = 'SAT'
            signal_emoji = '[-]'
            confidence = 'ORTA'
        else:
            signal = 'SAT'
            signal_emoji = '[-]'
            confidence = 'YÜKSEK'
        
        # Uyum analizi (teknik ve makro uyumlu mu?)
        tech_direction = 'ALIŞ' if self.technical_score >= 50 else 'SATIŞ'
        macro_direction = 'ALIŞ' if combined_macro_normalized >= 50 else 'SATIŞ'
        
        if tech_direction == macro_direction:
            alignment = 'UYUMLU'
            alignment_emoji = '[OK]'
            alignment_desc = f"Teknik ve makro analiz {tech_direction} yönünde uyumlu"
        else:
            alignment = 'ÇATIŞMA'
            alignment_emoji = '[!]'
            alignment_desc = f"Teknik {tech_direction}, makro {macro_direction} sinyali veriyor"
        
        # Risk değerlendirmesi
        if alignment == 'ÇATIŞMA':
            if signal == 'AL' and macro_direction == 'SATIŞ':
                risk_level = 'YÜKSEK'
                risk_desc = "Teknik olarak güçlü görünse de makro ortam olumsuz - dikkatli olun"
            elif signal == 'SAT' and macro_direction == 'ALIŞ':
                risk_level = 'ORTA'
                risk_desc = "Teknik zayıf ama makro destekleyici - beklemek mantıklı olabilir"
            else:
                risk_level = 'ORTA'
                risk_desc = "Karma sinyaller - dikkatli pozisyon alın"
        else:
            if hybrid_score >= 65 or hybrid_score <= 35:
                risk_level = 'DÜŞÜK'
                risk_desc = "Her iki analiz de aynı yönde - güvenilir sinyal"
            else:
                risk_level = 'ORTA'
                risk_desc = "Sinyaller uyumlu ama güven seviyesi orta"
        
        return {
            'hybrid_score': round(hybrid_score, 1),
            'signal': signal,
            'signal_emoji': signal_emoji,
            'confidence': confidence,
            'weights': {
                'technical': round(technical_weight * 100, 1),
                'macro': round(macro_weight * 100, 1)
            },
            'technical': {
                'score': round(self.technical_score, 1),
                'direction': tech_direction
            },
            'macro': {
                'score_raw': round(combined_macro_score, 2),
                'score_normalized': round(combined_macro_normalized, 1),
                'direction': macro_direction,
                'general': macro_result,
                'sector': {
                    'name': sector if sector else 'Bilinmiyor',
                    'score': round(sector_score, 1),
                    'description': sector_desc
                }
            },
            'alignment': {
                'status': alignment,
                'emoji': alignment_emoji,
                'description': alignment_desc
            },
            'risk': {
                'level': risk_level,
                'description': risk_desc
            }
        }
    
    def get_recommendation(self, hybrid_result: Dict) -> str:
        """
        Hibrid analiz sonucuna göre yatırım önerisi üretir
        
        Args:
            hybrid_result: calculate_hybrid_score() çıktısı
            
        Returns:
            str: Detaylı öneri metni
        """
        score = hybrid_result['hybrid_score']
        signal = hybrid_result['signal']
        risk = hybrid_result['risk']['level']
        alignment = hybrid_result['alignment']['status']
        
        recommendations = []
        
        # Sinyal bazlı öneriler
        if signal == 'AL':
            if risk == 'DÜŞÜK':
                recommendations.append("[+] AL pozisyonu acabilirsiniz. Hem teknik hem makro destekliyor.")
            elif risk == 'ORTA':
                recommendations.append("[!] AL pozisyonu icin uygun ama kucuk pozisyon tercih edin.")
            else:
                recommendations.append("[!] Teknik guclu ama makro riskli. Dikkatli olun veya bekleyin.")
        
        elif signal == 'SAT':
            if risk == 'DÜŞÜK':
                recommendations.append("[-] SAT sinyali guclu. Pozisyon varsa kapatmayi dusunun.")
            elif risk == 'ORTA':
                recommendations.append("[!] Zayif gorunuyor. Stop-loss koymadan pozisyon almayin.")
            else:
                recommendations.append("[!] Teknik zayif ama makro iyi. Bekleyip gozlemleyin.")
        
        else:  # BEK
            recommendations.append("[o] Net sinyal yok. Bekleyip gelismeleri takip edin.")
        
        # Uyum bazlı öneriler
        if alignment == 'ÇATIŞMA':
            recommendations.append(f"[!] {hybrid_result['alignment']['description']}")
            recommendations.append("[*] Catisan sinyaller var - daha fazla arastirma yapin.")
        
        # Sektörel öneriler
        sector_name = hybrid_result['macro']['sector']['name']
        if sector_name != 'Bilinmiyor':
            recommendations.append(f"[S] Sektor ({sector_name.upper()}): {hybrid_result['macro']['sector']['description']}")
        
        # Risk bazlı öneriler
        recommendations.append(f"[R] Risk Seviyesi: {risk} - {hybrid_result['risk']['description']}")
        
        return "\n".join(recommendations)


# Test fonksiyonu
if __name__ == "__main__":
    # Test verileri
    test_macro_data = {
        'last_update': '2025-11-11',
        'usd_try': {'current': 34.25, 'change_30d': 3.2},
        'eur_try': {'current': 37.80, 'change_30d': 2.8},
        'bist100': {'current': 9500, 'trend': 'down', 'change_30d': -5.5},
        'oil': {'current': 75.2, 'change_30d': 8.3},
        'gold': {'current': 2010.5, 'change_30d': 4.2},
        'tcmb_rate': 50.0
    }
    
    # Test 1: Teknik güçlü, Makro zayıf (ÇATIŞMA)
    print("=" * 60)
    print("TEST 1: Teknik Güçlü (75), Makro Zayıf - THYAO")
    print("=" * 60)
    
    analyzer1 = HybridAnalyzer(
        technical_score=75,
        macro_data=test_macro_data,
        symbol='THYAO'
    )
    result1 = analyzer1.calculate_hybrid_score()
    
    print(f"\nTeknik Skor: {result1['technical']['score']}/100")
    print(f"Makro Skor: {result1['macro']['score_normalized']}/100")
    print(f"Hibrid Skor: {result1['hybrid_score']}/100")
    print(f"Sinyal: {result1['signal_emoji']} {result1['signal']} (Güven: {result1['confidence']})")
    print(f"Uyum: {result1['alignment']['emoji']} {result1['alignment']['status']}")
    print(f"\n{result1['alignment']['description']}")
    print(f"\nÖNERİ:\n{analyzer1.get_recommendation(result1)}")
    
    # Test 2: Teknik zayıf, Makro zayıf (UYUMLU)
    print("\n" + "=" * 60)
    print("TEST 2: Teknik Zayıf (30), Makro Zayıf - THYAO")
    print("=" * 60)
    
    analyzer2 = HybridAnalyzer(
        technical_score=30,
        macro_data=test_macro_data,
        symbol='THYAO'
    )
    result2 = analyzer2.calculate_hybrid_score()
    
    print(f"\nTeknik Skor: {result2['technical']['score']}/100")
    print(f"Makro Skor: {result2['macro']['score_normalized']}/100")
    print(f"Hibrid Skor: {result2['hybrid_score']}/100")
    print(f"Sinyal: {result2['signal_emoji']} {result2['signal']} (Güven: {result2['confidence']})")
    print(f"Uyum: {result2['alignment']['emoji']} {result2['alignment']['status']}")

