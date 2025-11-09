# 📊 Algo Trading Bot

> **Kişisel Algoritmik Trading Öğrenme ve Analiz Platformu**

BIST hisseleri için teknik analiz + makro ekonomi entegrasyonlu, tamamen ücretsiz, Python tabanlı bir trading analiz sistemi. TradingView Pro'ya alternatif olarak geliştirilmektedir.

---

## 🎯 Proje Vizyonu

Bu proje, hem **trading öğretme** hem de **gerçek analiz** yapma amacıyla geliştirilmektedir. Ekonomi öğrencileri ve yeni başlayanlar için:

- ✅ Her satır açıklamalı, öğretici kod
- ✅ Teknik + Makro ekonomi hibrid analizi
- ✅ Paper trading ile risk almadan test
- ✅ %100 ücretsiz (sıfır maliyet)
- ✅ İleride otomatik trading'e genişletilebilir mimari

---

## 🚀 Özellikler

### Mevcut Özellikler (v0.1)
- 🔄 **Veri Çekme**: yfinance ile BIST hisseleri
- 📈 **5 Temel Gösterge**: RSI, MACD, Bollinger Bands, MA, Volume
- 💡 **Basit Analiz**: AL/SAT/BEK sinyalleri
- 📟 **Terminal Çıktısı**: Anlaşılır raporlar

### Planlanmış Özellikler
- 📊 **20+ Gösterge**: Stochastic, ADX, ATR, Fibonacci...
- 🕯️ **Mum Formasyonları**: Doji, Engulfing, Hammer...
- 🌍 **Makro Analiz**: Faiz, dolar, BIST100 trendi
- 🎯 **Hibrid Skor**: Teknik + Makro birleşimi
- 💼 **Paper Trading**: Sanal portföy yönetimi
- 🔔 **Alarmlar**: Windows bildirimleri
- 📉 **Backtesting**: Geçmiş performans testleri
- 🤖 **Gelecek**: Broker API entegrasyonu

---

## 🛠️ Kurulum

### Gereksinimler
- Python 3.10 veya üzeri
- Git

### Adımlar

```bash
# 1. Repo'yu klonlayın
git clone https://github.com/yildirimberke/algo-trading-bot.git
cd algo-trading-bot

# 2. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# 3. İlk analizi çalıştırın
python analyze.py THYAO
```

---

## 📖 Kullanım

### Basit Analiz
```bash
python analyze.py THYAO
```

### Detaylı Analiz (gelecekte)
```bash
python analyze.py THYAO --detailed --macro
```

### Paper Trading (gelecekte)
```bash
python paper_trade.py --buy THYAO --price 320 --target 350
```

---

## 📚 Dökümantasyon

- **[PROGRESS.md](PROGRESS.md)** - Geliştirme ilerlemesi
- **[ROADMAP.md](ROADMAP.md)** - Gelecek planları
- **[docs/SETUP.md](docs/SETUP.md)** - Detaylı kurulum (yakında)
- **[docs/INDICATORS.md](docs/INDICATORS.md)** - Gösterge açıklamaları (yakında)

---

## 🎓 Öğrenme Kaynakları

Bu proje, Python ve trading öğrenme aracı olarak tasarlanmıştır. Her kod dosyası:

- ✅ Bol açıklama (docstring + comment)
- ✅ Göstergelerin matematiksel açıklamaları
- ✅ Gerçek veri ile örnekler
- ✅ Test kodları

`docs/learning/` klasöründe trading kavramları açıklanmaktadır.

---

## 🤝 Katkıda Bulunma

Bu kişisel bir öğrenme projesidir, ancak öneriler ve geri bildirimler her zaman değerlidir!

---

## 📜 Lisans

MIT License - Açık kaynak, özgürce kullanın!

---

## ⚠️ Uyarı

**Bu bir eğitim projesidir!** 

- Finansal tavsiye değildir
- Gerçek para yatırımı yapmadan önce profesyonel danışman ile konuşun
- Trading risklidir, sermaye kaybedebilirsiniz

---

## 📞 İletişim

- GitHub: [@yildirimberke](https://github.com/yildirimberke)
- Proje: [algo-trading-bot](https://github.com/yildirimberke/algo-trading-bot)

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**


