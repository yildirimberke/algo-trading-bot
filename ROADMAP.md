# 🗺️ ROADMAP - Algo Trading Bot

> **Gelecek Planları ve Özellik Haritası**

---

## 🎯 Genel Vizyon

6 fazlı bir geliştirme planı ile başlangıçtan tam özellikli trading platformuna doğru ilerleyeceğiz.

**Zaman Çizelgesi:** 3-6 ay (düzensiz çalışma temposu ile)  
**İlke:** Her faz kendi başına kullanılabilir olmalı

---

## ✅ FAZ 1: Temel Altyapı (1-2 hafta)

**Durum:** 🔄 Devam ediyor (Başlangıç: 2025-11-09)

### Hedef
Çalışan bir basit analiz sistemi, gerçek verilerle test

### Özellikler
- [x] Proje yapısı
- [x] Dökümantasyon (README, PROGRESS, ROADMAP)
- [ ] requirements.txt
- [ ] .gitignore
- [ ] Git repo başlatma
- [ ] **Veri Çekme Modülü**
  - yfinance entegrasyonu
  - BIST hisse desteği (.IS suffix)
  - Error handling & retry
  - Cache mekanizması
- [ ] **5 Temel Gösterge**
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Simple Moving Average (50, 200)
  - Volume analizi
- [ ] **Basit Analiz Motoru**
  - Multi-indicator skorlama
  - AL/SAT/BEK sinyali
  - Terminal çıktısı
- [ ] **İlk Testler**
  - THYAO, SASA, GARAN testleri
  - İlk git commit

### Başarı Kriteri
✅ `python analyze.py THYAO` komutu çalışır ve anlamlı sonuç verir

---

## 📊 FAZ 2: Makro Ekonomi Entegrasyonu (2-3 hafta)

**Durum:** ⏳ Bekliyor

### Hedef
Teknik + Makro ekonomi hibrid analiz sistemi

### Özellikler
- [ ] **Makro Veri Yönetimi**
  - config/macro_data.json yapısı
  - USD/TRY otomatik çekme
  - TCMB politika faizi (manuel input)
  - BIST100 trend analizi
  - Petrol/Altın fiyatları
- [ ] **Makro Analiz Motoru**
  - Faiz değişimi puanlama (-10/+10)
  - Döviz değişimi puanlama
  - Sektörel faktör analizi
  - Makro risk skoru
- [ ] **Hibrid Skorlama Sistemi**
  - Teknik skor + Makro skor birleştirme
  - Ağırlıklı hesaplama
  - Güven seviyesi (confidence score)
  - İyimser/Kötümser senaryo analizi
- [ ] **Gelişmiş Raporlama**
  - Makro faktörlerin açıklanması
  - "Neden bu karar?" mantık ağacı

### Başarı Kriteri
✅ Teknik olarak güçlü ama makro olumsuz olan durumları yakalayabilme

---

## 🔥 FAZ 3: Gelişmiş Göstergeler (3-4 hafta)

**Durum:** ⏳ Bekliyor

### Hedef
20+ gösterge, mum formasyonları, chart patterns

### Özellikler
- [ ] **Momentum Göstergeleri (5+)**
  - Stochastic Oscillator
  - Williams %R
  - ROC (Rate of Change)
  - CCI (Commodity Channel Index)
  - Money Flow Index
- [ ] **Trend Göstergeleri (5+)**
  - EMA (Exponential Moving Average)
  - ADX (Average Directional Index)
  - Parabolic SAR
  - Ichimoku Cloud
  - VWAP
- [ ] **Volatilite Göstergeleri (3+)**
  - ATR (Average True Range)
  - Standard Deviation
  - Keltner Channels
- [ ] **Mum Formasyonları (10+)**
  - Doji (4 çeşit)
  - Hammer, Hanging Man
  - Engulfing (Bullish/Bearish)
  - Morning/Evening Star
  - Shooting Star, Inverted Hammer
  - Harami, Piercing Line
- [ ] **Chart Patterns (Temel)**
  - Destek-direnç otomatik tespit
  - Trend çizgileri
  - Baş-omuz formasyonu (temel)
  - Fibonacci retracement
- [ ] **Hacim Profil Analizi**
  - Kurumsal alım tespiti
  - Hacim artış alarmı
  - Volume-price correlation

### Başarı Kriteri
✅ En az 20 farklı göstergeden sinyal üretimi

---

## 💼 FAZ 4: Paper Trading Sistemi (3-4 hafta)

**Durum:** ⏳ Bekliyor

### Hedef
Risk almadan sanal portföy ile gerçek test

### Özellikler
- [ ] **Emir Yönetimi**
  - Manuel AL emri (`--buy THYAO 320`)
  - Hedef fiyat belirleme
  - Stop-loss ayarlama
  - JSON kayıt sistemi
- [ ] **Model Tahminleri**
  - Matematiksel hedef fiyat hesaplama
  - Zaman tahmini (5-10 gün)
  - Risk/Reward oranı
  - Başarı olasılığı
- [ ] **Pozisyon Takibi**
  - Açık pozisyonları görüntüleme
  - Günlük fiyat kontrolü
  - Hedef tutup tutmadığını otomatik kontrol
  - Win/Loss kaydı
- [ ] **Performans Metrikleri**
  - Win rate (kazanma oranı)
  - Ortalama kazanç/kayıp
  - Model doğruluk oranı
  - Maximum drawdown
  - Sharpe ratio (basit)
- [ ] **Portföy Yönetimi**
  - Sanal sermaye takibi
  - Pozisyon büyüklüğü önerisi
  - Risk yönetimi kuralları

### Başarı Kriteri
✅ 20+ işlem sonrası modelin gerçek doğruluk oranını ölçebilme

---

## 🔔 FAZ 5: Alarm ve Raporlama (2 hafta)

**Durum:** ⏳ Bekliyor

### Hedef
Otomatik bildirimler ve profesyonel raporlar

### Özellikler
- [ ] **Alarm Sistemi**
  - Windows toast bildirimi
  - Terminal ses uyarısı (beep)
  - Kritik sinyal algılama
  - Özelleştirilebilir alarm kuralları
- [ ] **Raporlama Seviyeleri**
  - Basit mod (3-4 satır özet)
  - Orta mod (10-15 satır, ana göstergeler)
  - Detaylı mod (tüm göstergeler, açıklamalar)
- [ ] **Görsel İyileştirmeler**
  - Renkli terminal çıktısı (colorama)
  - ASCII art grafikler
  - Emoji kullanımı
  - Tablo formatları
- [ ] **Export Özellikleri**
  - İşlem geçmişi → CSV
  - Analiz raporu → TXT
  - Günlük özet raporu
  - (Opsiyonel) HTML rapor

### Başarı Kriteri
✅ Güçlü sinyal geldiğinde otomatik bildirim alabilme

---

## 📉 FAZ 6: Backtesting Motoru (3-4 hafta)

**Durum:** ⏳ Bekliyor

### Hedef
Geçmiş verilerle strateji testi ve optimizasyon

### Özellikler
- [ ] **Backtest Altyapısı**
  - Tarih aralığı seçimi (1 ay - 5 yıl)
  - Geçmiş veri çekme & cache
  - Simulasyon motoru
  - Slippage & commission hesabı
- [ ] **Strateji Testleri**
  - Mevcut stratejinin geçmiş performansı
  - "What-if" analizi
  - Parametre optimizasyonu (RSI 30 mu 25 mi?)
  - Monte Carlo simülasyonu
- [ ] **Performans Analizi**
  - Win rate evolution (zamana göre)
  - Maximum drawdown
  - Sharpe ratio
  - Sortino ratio
  - Calmar ratio
- [ ] **Grafiksel Çıktılar**
  - Equity curve (matplotlib)
  - Drawdown grafiği
  - Win/Loss dağılımı
  - Aylık performance

### Başarı Kriteri
✅ "Son 2 yılda bu strateji %X kazandırırdı" bilgisini görebilme

---

## 🚀 FAZ 7: İleri Özellikler (İsteğe Bağlı)

**Durum:** 💭 Fikir aşaması

### Potansiyel Özellikler

#### A. Gelişmiş Pattern Recognition
- Otomatik üçgen, bayrak, kama tespiti
- Fibonacci extension
- Elliott Wave analizi (temel)
- Harmonic patterns

#### B. Korelasyon ve Sentiment
- Hisseler arası korelasyon matrisi
- Sektör performans karşılaştırması
- BIST100 ile korelasyon
- Market sentiment göstergesi

#### C. Strateji Oluşturucu
- Kendi kurallarını tanımlama:
  ```
  IF RSI < 30 AND MACD > 0 AND Volume > 1.5x AVG
  THEN BUY
  ```
- Strateji kaydetme/yükleme
- Strateji karşılaştırması

#### D. Web Arayüzü
- Flask/Streamlit ile web UI
- Gerçek zamanlı dashboard
- Grafik gösterimi
- Uzaktan erişim

#### E. Broker API Entegrasyonu
- İş Yatırım API
- Ata Yatırım API
- Semi-otomatik emir gönderme
- Gerçek portföy senkronizasyonu

#### F. Makine Öğrenmesi
- XGBoost ile fiyat tahmini
- LSTM (deep learning) denemeleri
- Ensemble modeller
- Auto-ML pipeline

---

## 📅 Zaman Tahmini

| Faz | Tahmini Süre | Kümülatif |
|-----|-------------|-----------|
| Faz 1 | 1-2 hafta | 2 hafta |
| Faz 2 | 2-3 hafta | 5 hafta |
| Faz 3 | 3-4 hafta | 9 hafta |
| Faz 4 | 3-4 hafta | 13 hafta (~3 ay) |
| Faz 5 | 2 hafta | 15 hafta |
| Faz 6 | 3-4 hafta | 19 hafta (~4.5 ay) |

**Not:** Düzensiz çalışma temposu nedeniyle gerçek süre 2-3x olabilir (6-12 ay)

---

## 🎖️ Milestone'lar

- [ ] **v0.1** - İlk çalışan sistem (Faz 1 sonu)
- [ ] **v0.2** - Makro entegrasyonu (Faz 2 sonu)
- [ ] **v0.3** - Tam gösterge seti (Faz 3 sonu)
- [ ] **v0.5** - Paper trading (Faz 4 sonu)
- [ ] **v0.7** - Alarm sistemi (Faz 5 sonu)
- [ ] **v1.0** - Backtesting (Faz 6 sonu) - **TAM PLATFORM**
- [ ] **v2.0** - Broker API (Faz 7) - **OTO TRADING**

---

## 🔄 Değişiklik Süreci

Bu roadmap esnek bir dokümandır:

- ✅ Özellikler eklenebilir/çıkarılabilir
- ✅ Öncelikler değişebilir
- ✅ Faz süreleri ayarlanabilir
- ✅ Kullanıcı geri bildirimine göre güncellenecek

**Son Güncelleme:** 2025-11-09  
**Durum:** Aktif geliştirme (Faz 1)

---

**💡 Not:** Her faz tamamlandığında PROGRESS.md güncellenir ve bu roadmap gözden geçirilir.


