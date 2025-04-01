import pandas as pd
import numpy as np
from typing import List, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib


def compute_text_hash(text: str) -> str:

    return hashlib.md5(str(text).strip().lower().encode()).hexdigest()


def detect_duplicates(texts: Union[pd.Series, List[str]], threshold: float = 0.85) -> List[bool]:

    if isinstance(texts, pd.Series):
        texts = texts.tolist()

    if not texts:
        return []

    texts = [str(t) if t is not None else "" for t in texts]

    text_hashes = [compute_text_hash(text) for text in texts]
    seen_hashes = set()
    is_duplicate = []

    for h in text_hashes:
        if h in seen_hashes:
            is_duplicate.append(True)
        else:
            seen_hashes.add(h)
            is_duplicate.append(False)

    if threshold < 1.0:

        non_dup_indices = [i for i, is_dup in enumerate(is_duplicate) if not is_dup]
        non_dup_texts = [texts[i] for i in non_dup_indices]

        if len(non_dup_texts) > 1:

            vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
            try:
                tfidf_matrix = vectorizer.fit_transform(non_dup_texts)

                similarity_matrix = cosine_similarity(tfidf_matrix)

                near_dup_indices = set()
                for i in range(len(similarity_matrix)):
                    for j in range(i + 1, len(similarity_matrix)):
                        if similarity_matrix[i, j] >= threshold:
                            near_dup_indices.add(j)

                for idx in near_dup_indices:
                    is_duplicate[non_dup_indices[idx]] = True
            except Exception as e:
                print(f"TF-IDF hesaplaması sırasında hata: {e}")

    return is_duplicate


def detect_duplicates_in_df(df: pd.DataFrame, text_column: str = "text", threshold: float = 0.85) -> pd.DataFrame:

    if text_column not in df.columns:
        raise ValueError(f"'{text_column}' sütunu DataFrame'de bulunamadı.")

    result_df = df.copy()
    result_df["is_duplicate"] = detect_duplicates(df[text_column], threshold)

    return result_df