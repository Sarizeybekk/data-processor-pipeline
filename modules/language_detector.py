import pandas as pd
from langdetect import detect, LangDetectException
from typing import List, Dict, Optional


def detect_languages(text: str) -> str:

    if not text or len(str(text).strip()) < 10:
        return "unknown"

    try:
        return detect(str(text))
    except LangDetectException:
        return "unknown"
    except Exception:
        return "unknown"

def separate_by_language(df: pd.DataFrame,
                         text_column: str = "text",
                         target_languages: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:

    if text_column not in df.columns:
        raise ValueError(f"'{text_column}' sütunu DataFrame'de bulunamadı.")

    df_copy = df.copy()
    df_copy["detected_language"] = df_copy[text_column].apply(detect_languages)

    grouped = {lang: group for lang, group in df_copy.groupby("detected_language")}

    if target_languages:
        return {lang: group for lang, group in grouped.items() if lang in target_languages}

    return grouped


def filter_by_languages(df: pd.DataFrame,
                        target_languages: List[str],
                        text_column: str = "text") -> pd.DataFrame:

    df_copy = df.copy()

    df_copy["detected_language"] = df_copy[text_column].apply(detect_languages)

    return df_copy[df_copy["detected_language"].isin(target_languages)]