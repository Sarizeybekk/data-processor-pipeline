"""
LLM Veri Temizleme ve Ön-İşleme Aracı modülleri.
"""

# Modülleri güvenli bir şekilde import et
try:
    from modules.language_detector import detect_languages, separate_by_language, filter_by_languages
except ImportError:
    print("Uyarı: language_detector modülü yüklenemedi")

try:
    from modules.duplicate_detector import detect_duplicates, detect_duplicates_in_df
except ImportError:
    print("Uyarı: duplicate_detector modülü yüklenemedi")

try:
    from modules.spam_detector import detect_spam, filter_spam
except ImportError:
    print("Uyarı: spam_detector modülü yüklenemedi")

try:
    from modules.text_cleaner import clean_text, clean_dataframe
except ImportError:
    print("Uyarı: text_cleaner modülü yüklenemedi")

try:
    from modules.prompt_converter import convert_to_prompt_completion
except ImportError:
    print("Uyarı: prompt_converter modülü yüklenemedi")

# Tüm fonksiyonların listesi - modül bazında import için
__all__ = [
    'detect_languages',
    'separate_by_language',
    'filter_by_languages',
    'detect_duplicates',
    'detect_duplicates_in_df',
    'detect_spam',
    'filter_spam',
    'clean_text',
    'clean_dataframe',
    'convert_to_prompt_completion'
]