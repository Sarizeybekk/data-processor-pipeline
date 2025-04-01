import re
import pandas as pd
SPAM_KEYWORDS = [
    'bedava', 'ücretsiz', 'kazanç', 'kazandınız', 'ödül', 'fırsat', 'acil', 'tebrikler',
    'kredi', 'kumar', 'bahis', 'casino', 'şans', 'zengin', 'para', 'kazan', 'tıkla',
    'hemen', 'sınırlı', 'stok', 'kampanya', 'indirim', 'avantaj', 'özel teklif',
    'free', 'win', 'winner', 'prize', 'offer', 'urgent', 'congratulations', 'credit',
    'gambling', 'bet', 'casino', 'lucky', 'rich', 'money', 'cash', 'click', 'now',
    'limited', 'stock', 'deal', 'discount', 'special offer', 'act now', 'guarantee',
    'www', 'http', '.com', '.net', '.org', '.info'
]

SPAM_PATTERNS = [
    r'(\d{1,3}[,.]\d{1,2}%\s*(off|discount))',
    r'(\$\d+[,.]\d{2}|\d+[,.]\d{2}\$)',
    r'(https?://\S+)',
    r'(\b\S+@\S+\.\S+)',
    r'(\b\d{3}[-.]?\d{3}[-.]?\d{4}\b)',
    r'(\b[A-Z]{2,}\b)',
    r'([!?]{2,})',
]


def detect_spam(text: str) -> float:

    if not text or len(str(text).strip()) < 5:
        return 0.0

    text = str(text).lower().strip()
    text_length = len(text)

    keyword_score = 0
    pattern_score = 0
    format_score = 0

    words = text.split()
    spam_word_count = sum(1 for word in words if word in SPAM_KEYWORDS)

    if words:
        keyword_score = min(1.0, spam_word_count / len(words) * 2.5)

    pattern_matches = 0
    for pattern in SPAM_PATTERNS:
        matches = re.findall(pattern, text)
        pattern_matches += len(matches)

    pattern_score = min(1.0, pattern_matches / 5)

    uppercase_ratio = sum(1 for c in text if c.isupper()) / max(1, text_length)

    punctuation_ratio = sum(1 for c in text if c in '!?*.,:;') / max(1, text_length)

    contains_url = 1 if re.search(r'https?://\S+', text) else 0
    contains_email = 1 if re.search(r'\b\S+@\S+\.\S+', text) else 0

    format_score = min(1.0, uppercase_ratio * 2 + punctuation_ratio * 3 + contains_url * 0.3 + contains_email * 0.3)

    total_score = (keyword_score * 0.5) + (pattern_score * 0.3) + (format_score * 0.2)

    return round(total_score, 2)


def filter_spam(df: pd.DataFrame,
                text_column: str = "text",
                threshold: float = 0.7,
                add_score_column: bool = True) -> pd.DataFrame:
    if text_column not in df.columns:
        raise ValueError(f"'{text_column}' sütunu DataFrame'de bulunamadı.")

    result_df = df.copy()

    result_df["spam_score"] = result_df[text_column].apply(detect_spam)

    filtered_df = result_df[result_df["spam_score"] < threshold]
    if not add_score_column and "spam_score" in filtered_df.columns:
        filtered_df = filtered_df.drop(columns=["spam_score"])

    return filtered_df