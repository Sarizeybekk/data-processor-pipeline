"""
LLM Veri Temizleme ve Ön-İşleme Aracı konfigürasyon dosyası
"""

# Desteklenen diller ve kodları
SUPPORTED_LANGUAGES = {
    'Türkçe': 'tr',
    'İngilizce': 'en',
    'Almanca': 'de',
    'Fransızca': 'fr',
    'İspanyolca': 'es',
    'İtalyanca': 'it',
    'Portekizce': 'pt',
    'Rusça': 'ru',
    'Çince': 'zh',
    'Japonca': 'ja',
    'Korece': 'ko',
    'Arapça': 'ar',
    'Hintçe': 'hi',
    'Diğer': 'other'
}

# Prompts-completion formatları
PROMPT_FORMATS = {
    'Soru-Cevap': {
        'description': 'Metin, soru ve cevap şeklinde ayrılır.',
        'example': 'Türkiye\'nin başkenti neresidir? - Türkiye\'nin başkenti Ankara\'dır.'
    },
    'Talimat-Yanıt': {
        'description': 'Metin, bir talimat ve ona verilen yanıt şeklinde ayrılır.',
        'example': 'Bir kek tarifi yazın. - Malzemeler: 3 yumurta, 1 su bardağı şeker...'
    },
    'Diyalog': {
        'description': 'Metin, iki kişi arasında geçen konuşma şeklinde ayrılır.',
        'example': 'İnsan: Merhaba, nasılsın?\nAI: Merhaba! Ben bir yapay zekayım...'
    },
    'Özel': {
        'description': 'Özel bir formatta prompt-completion çiftleri oluşturulur.',
        'example': 'Özelleştirilmiş prefix\'ler ile formatlama yapılır.'
    }
}

# Dosya tipleri
SUPPORTED_FILE_TYPES = {
    'csv': 'Comma-Separated Values',
    'txt': 'Text File',
    'json': 'JSON File',
    'jsonl': 'JSON Lines'
}

# Metin temizleme ayarları
DEFAULT_CLEANER_CONFIG = {
    'normalize_case': True,
    'remove_extra_spaces': True,
    'fix_punctuation': True,
    'fix_quotes': True,
    'remove_accents': False,
    'remove_html': True,
    'remove_url': True
}


DEFAULT_SPAM_CONFIG = {
    'threshold': 0.7
}

DEFAULT_DUPLICATE_CONFIG = {
    'threshold': 0.85,
    'use_hash': True
}

APP_CONFIG = {
    'max_file_size_mb': 100,
    'sample_preview_rows': 5,
    'debug_mode': False,
    'default_output_format': 'csv'
}