import pandas as pd
import re
from typing import List, Tuple, Dict


def is_question(text: str) -> bool:
    if '?' in text:
        return True

    question_words = ['ne', 'neden', 'niçin', 'niye', 'nasıl', 'hangi', 'kim', 'kime',
                      'nerede', 'nereden', 'nereye', 'ne zaman', 'kaç', 'mı', 'mi', 'mu', 'mü',
                      'what', 'why', 'how', 'which', 'who', 'whom', 'whose', 'where',
                      'when', 'how many', 'how much', 'do', 'does', 'did', 'is', 'are']

    text_lower = text.lower()
    for word in question_words:
        if text_lower.startswith(word + ' '):
            return True

    return False


def extract_qa_pair(text: str) -> Tuple[str, str]:
    for sep in ['?: ', '? ', '\n']:
        if sep in text:
            parts = text.split(sep, 1)
            if len(parts) == 2:
                question = parts[0] + ('?' if sep.startswith('?') else '')
                answer = parts[1].strip()

                if is_question(question):
                    return question, answer

    if is_question(text):
        return text, ""
    else:
        return "", text


def create_prompt_completion_pairs(df: pd.DataFrame,
                                   text_column: str = "text",
                                   format_type: str = "Soru-Cevap") -> pd.DataFrame:

    if text_column not in df.columns:
        raise ValueError(f"'{text_column}' sütunu DataFrame'de bulunamadı.")

    result_rows = []

    for _, row in df.iterrows():
        text = row[text_column]
        row_data = {col: row[col] for col in df.columns}  # Orijinal sütunları kopyala

        if isinstance(text, str) and text.strip():  # Metin kontrolü
            if format_type == "Soru-Cevap":
                prompt, completion = extract_qa_pair(text)

            elif format_type == "Talimat-Yanıt":
                parts = text.split("\n", 1)
                if len(parts) == 2:
                    prompt, completion = parts[0], parts[1]
                else:
                    sentences = re.split(r'(?<=[.!?]) +', text)
                    if len(sentences) > 1:
                        prompt = sentences[0]
                        completion = " ".join(sentences[1:])
                    else:
                        prompt, completion = text, ""

            elif format_type == "Diyalog":
                lines = text.split("\n")
                if len(lines) >= 2:
                    prompt = lines[0]
                    completion = "\n".join(lines[1:])
                else:
                    prompt, completion = text, ""

            else:
                mid_point = len(text) // 2
                prompt = text[:mid_point].strip()
                completion = text[mid_point:].strip()

            row_data["prompt"] = prompt
            row_data["completion"] = completion
            result_rows.append(row_data)

    if result_rows:
        return pd.DataFrame(result_rows)
    else:

        return pd.DataFrame(columns=list(df.columns) + ["prompt", "completion"])

def convert_to_prompt_completion(df: pd.DataFrame,
                                 text_column: str = "text",
                                 format_type: str = "Soru-Cevap") -> pd.DataFrame:

    return create_prompt_completion_pairs(df, text_column, format_type)