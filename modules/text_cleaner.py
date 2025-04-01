import re
import pandas as pd
import unicodedata
def clean_text(text: str,
               normalize_case: bool = True,
               remove_extra_spaces: bool = True,
               fix_punctuation: bool = True) -> str:

    if text is None:
        return ""

    text = str(text)

    text = unicodedata.normalize('NFC', text)

    if remove_extra_spaces:
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)

    if fix_punctuation:
        text = re.sub(r'\.{2,}', '.', text)
        text = re.sub(r'\!{2,}', '!', text)
        text = re.sub(r'\?{2,}', '?', text)

        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'([.,!?;:])\s*', r'\1 ', text)

    if normalize_case:
        text = text.lower()

    return text.strip()


def clean_dataframe(df: pd.DataFrame,
                    text_column: str = "text",
                    output_column: str = "cleaned_text",
                    **kwargs) -> pd.DataFrame:

    if text_column not in df.columns:
        raise ValueError(f"'{text_column}' sütunu DataFrame'de bulunamadı.")

    result_df = df.copy()
    result_df[output_column] = result_df[text_column].apply(lambda x: clean_text(x, **kwargs))

    return result_df