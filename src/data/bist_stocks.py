"""
BIST Hisse Listesi

Bu modül BIST30 ve BIST100 endekslerindeki hisse kodlarını içerir.
Hisse geçerliliği kontrolü ve liste yönetimi sağlar.

Not: Liste değişebilir, periyodik olarak güncellenmeli.
"""

from typing import List, Optional

# BIST 30 Endeksi (En likit 30 hisse)
# Güncelleme tarihi: 2025-11 (örnektir, güncel liste için KAP'a bakın)
BIST30 = [
    'ASELS',  # ASELSAN
    'BIMAS',  # BİM
    'EREGL',  # EREĞLİ
    'GARAN',  # GARANTİ BANKASI
    'HEKTS',  # HEKTAŞ
    'ISCTR',  # İŞ BANKASI (C)
    'KCHOL',  # KOÇ HOLDING
    'KOZAA',  # KOZA ANADOLU METAL
    'KOZAL',  # KOZA ALTIN
    'PETKM',  # PETKIM
    'PGSUS',  # PEGASUS
    'SAHOL',  # SABANCI HOLDING
    'SASA',   # SASA
    'SISE',   # ŞİŞE CAM
    'TAVHL',  # TAV HAVALİMANLARI
    'TCELL',  # TURKCELL
    'THYAO',  # TÜRK HAVA YOLLARI
    'TKFEN',  # TEKFEN
    'TOASO',  # TOFAŞ OTO. FAB.
    'TUPRS',  # TÜPRAŞ
    'VAKBN',  # VAKIFBANK
    'YKBNK',  # YAPI KREDİ
]

# BIST 100 Endeksi (100 hisse - tam liste çok uzun, örnekler)
# Not: BIST30 hepsi BIST100'de de vardır
BIST100 = BIST30 + [
    'ADEL',   # ADEL
    'ADESE',  # ADESE
    'AEFES',  # ANADOLU EFES
    'AFYON',  # AFYON ÇİMENTO
    'AGHOL',  # AG ANADOLU GRUBU
    'AKBNK',  # AKBANK
    'AKCNS',  # AKÇANSA
    'AKENR',  # AK ENERJİ
    'AKSA',   # AKSA
    'AKSEN',  # AKSA ENERJİ
    'ALARK',  # ALARKO
    'ALBRK',  # AL BARAKA TÜRK
    'ALGYO',  # ALARKO GYO
    'ALKIM',  # ALKİM
    'ANSGR',  # ANSGr
    'ARCLK',  # ARÇELİK
    'ARDYZ',  # ARDEMİR
    'ASTOR',  # ASTOR
    'BAGFS',  # BAGFAŞ
    'BANVT',  # BANVİT
    'BRSAN',  # BORUSAN
    'BFREN',  # BOSCH FREN
    'BRYAT',  # BORUSAN YATIRIM
    'BTCIM',  # BATIÇİM
    'BUCIM',  # BURÇELİK
    'CCOLA',  # COCA COLA
    'CEMTS',  # ÇEMTAŞ
    'CIMSA',  # ÇİMSA
    'DOAS',   # DOĞAN
    'DOHOL',  # DOĞAN HOLDING
    'ECILC',  # EIS ECZA
    'EGEEN',  # EGE ENDÜSTRİ
    'EKGYO',  # EMLAK KONUT GYO
    'ENKAI',  # ENKA
    'ENJSA',  # ENERJISA
    'EUPWR',  # EUROPOWER
    'FROTO',  # FORD OTOSAN
    'GESAN',  # GESAN
    'GLYHO',  # GLOBAL YATIRIM
    'GOLTS',  # GÖLTAŞ
    'GOODY',  # GOODYEAR
    'GOZDE',  # GÖZDE
    'GUBRF',  # GÜBRE FABRİKALARI
    'HALKB',  # HALK BANKASI
    'IPEKE',  # İPEK DOĞAL
    'JANTS',  # JANTSA
    'KARSN',  # KARSAN
    'KARTN',  # KARTONSAN
    'KORDS',  # KORDSA
    'KONYA',  # KONYA ÇİMENTO
    'KRDMD',  # KARDEMIR (D)
    'KTLEV',  # KITLE
    'LOGO',   # LOGO YAZILIM
    'MAVI',   # MAVİ GİYİM
    'MGROS',  # MİGROS
    'ODAS',   # ODAŞ
    'OTKAR',  # OTOKAR
    'OYAKC',  # OYAK ÇİMENTO
    'PENTA',  # PENTA
    'PRKME',  # PARK ELEKT.
    'QUAGR',  # QUA GRANITE
    'SELEC',  # SELÇUK ECZA
    'SKBNK',  # ŞEKERBANK
    'SOKM',   # ŞOK MARKETLER
    'TATGD',  # TAT GIDA
    'TBORG',  # T.TUBORG
    'TKNSA',  # TEKNOSA
    'TMSN',   # TÜMOSAN
    'TRGYO',  # TORUNLAR GYO
    'TSKB',   # TSKB
    'TTKOM',  # TÜRK TELEKOM
    'TTRAK',  # TÜRK TRAKTÖR
    'ULKER',  # ÜLKER
    'VESTL',  # VESTEL
    'VESBE',  # VESTEL BEYAZ
    'YATAS',  # YATAŞ
]

# Alternatif: Popüler hisseler (trading için sıkça kullanılanlar)
POPULAR_STOCKS = [
    'THYAO',  # Havacılık
    'PGSUS',  # Havacılık
    'TUPRS',  # Petrokimya
    'AKBNK',  # Bankacılık
    'GARAN',  # Bankacılık
    'ISCTR',  # Bankacılık
    'YKBNK',  # Bankacılık
    'VAKBN',  # Bankacılık
    'SASA',   # Kimya
    'ASELS',  # Savunma
    'KCHOL',  # Holding
    'SAHOL',  # Holding
    'TCELL',  # Telekom
    'BIMAS',  # Perakende
    'SOKM',   # Perakende
    'EREGL',  # Çelik
    'ARCLK',  # Beyaz Eşya
    'TOASO',  # Otomotiv
    'FROTO',  # Otomotiv
    'SISE',   # Cam
]


def is_valid_bist_stock(symbol: str, check_list: str = 'BIST100') -> bool:
    """
    Hisse kodunun BIST endeksinde olup olmadığını kontrol eder.
    
    Args:
        symbol (str): Hisse kodu
        check_list (str): Hangi liste kontrol edilsin
                          - 'BIST30', 'BIST100', 'POPULAR'
    
    Returns:
        bool: Hisse geçerli ise True
    
    Örnek:
        >>> is_valid_bist_stock('THYAO')
        True
        >>> is_valid_bist_stock('FAKE123')
        False
    """
    
    symbol = symbol.strip().upper()
    
    # .IS suffix'ini çıkar
    if symbol.endswith('.IS'):
        symbol = symbol[:-3]
    
    if check_list.upper() == 'BIST30':
        return symbol in BIST30
    elif check_list.upper() == 'POPULAR':
        return symbol in POPULAR_STOCKS
    else:  # Default: BIST100
        return symbol in BIST100


def get_stock_list(list_name: str = 'BIST100') -> List[str]:
    """
    Belirtilen hisse listesini döndürür.
    
    Args:
        list_name (str): 'BIST30', 'BIST100', 'POPULAR'
    
    Returns:
        list: Hisse kodları listesi
    
    Örnek:
        >>> stocks = get_stock_list('BIST30')
        >>> print(f"{len(stocks)} hisse var")
    """
    
    list_name = list_name.upper()
    
    if list_name == 'BIST30':
        return BIST30.copy()
    elif list_name == 'POPULAR':
        return POPULAR_STOCKS.copy()
    else:
        return BIST100.copy()


def suggest_similar_stocks(symbol: str, max_results: int = 5) -> List[str]:
    """
    Girilen hisse koduna benzer hisse kodları önerir.
    (Basit string similarity, kullanıcı yazım hatası yaptıysa yardımcı olur)
    
    Args:
        symbol (str): Aranacak hisse kodu
        max_results (int): Maksimum öneri sayısı
    
    Returns:
        list: Benzer hisse kodları
    
    Örnek:
        >>> suggest_similar_stocks('THYA')  # THYAO yazım hatası
        ['THYAO']
    """
    
    symbol = symbol.strip().upper()
    
    if symbol.endswith('.IS'):
        symbol = symbol[:-3]
    
    # Basit benzerlik: içinde geçen harfler
    similar = []
    
    for stock in BIST100:
        # Tam eşleşme
        if stock == symbol:
            return [stock]
        
        # Başlangıç eşleşmesi
        if stock.startswith(symbol[:2]):
            similar.append(stock)
        
        # İçinde geçiyor mu
        elif symbol[:3] in stock:
            similar.append(stock)
    
    return similar[:max_results]


def get_sector_stocks(sector: str) -> List[str]:
    """
    Belirtilen sektördeki hisseleri döndürür (basit versiyon).
    
    Args:
        sector (str): Sektör adı
                      - 'BANKA', 'HAVAYOLU', 'ENERJİ', 'TEKNOLOJİ', vb.
    
    Returns:
        list: O sektördeki bilinen hisseler
    
    Not: Bu basit bir implement, geliştirilmeli
    """
    
    sector = sector.upper()
    
    sectors = {
        'BANKA': ['AKBNK', 'GARAN', 'ISCTR', 'YKBNK', 'VAKBN', 'HALKB', 'SKBNK', 'ALBRK'],
        'HAVAYOLU': ['THYAO', 'PGSUS'],
        'ENERJI': ['AKSEN', 'AKENR', 'EUPWR', 'ENJSA'],
        'TEKNOLOJİ': ['ASELS', 'LOGO', 'TCELL', 'TTKOM'],
        'PERAKENDE': ['BIMAS', 'SOKM', 'MGROS', 'MAVI'],
        'OTOMOTİV': ['TOASO', 'FROTO', 'OTKAR', 'TTRAK', 'KARSN'],
        'HOLDİNG': ['KCHOL', 'SAHOL', 'DOHOL', 'AGHOL'],
        'GIDA': ['ULKER', 'CCOLA', 'TATGD', 'AEFES', 'TBORG'],
    }
    
    return sectors.get(sector, [])


# Test fonksiyonu
if __name__ == "__main__":
    print("=" * 60)
    print("BIST HİSSE LİSTESİ - TEST")
    print("=" * 60)
    
    print(f"\n✅ BIST30: {len(BIST30)} hisse")
    print(f"✅ BIST100: {len(BIST100)} hisse")
    print(f"✅ Popüler: {len(POPULAR_STOCKS)} hisse")
    
    print("\n📋 BIST30 Listesi:")
    for i, stock in enumerate(BIST30, 1):
        print(f"  {i:2}. {stock}", end="  ")
        if i % 5 == 0:
            print()
    
    print("\n\n🔍 Geçerlilik Testleri:")
    test_stocks = ['THYAO', 'SASA', 'FAKE123', 'GARAN']
    
    for stock in test_stocks:
        valid = is_valid_bist_stock(stock)
        emoji = "✅" if valid else "❌"
        print(f"  {emoji} {stock}: {'Geçerli' if valid else 'Geçersiz'}")
    
    print("\n🔍 Benzerlik Testi (Yazım Hatası):")
    print(f"  'THYA' için öneriler: {suggest_similar_stocks('THYA')}")
    print(f"  'GARA' için öneriler: {suggest_similar_stocks('GARA')}")
    
    print("\n🏦 Sektör Testi:")
    for sector in ['BANKA', 'HAVAYOLU', 'TEKNOLOJİ']:
        stocks = get_sector_stocks(sector)
        print(f"  {sector}: {', '.join(stocks[:5])}")
    
    print("\n" + "=" * 60)
    print("✅ TÜM TESTLER TAMAMLANDI!")
    print("=" * 60)

