import streamlit as st

st.set_page_config(
    page_title="LLM Veri Temizleme ve Ön-İşleme Aracı",
    page_icon="🧹",
    layout="wide",
)

import pandas as pd
import os
import sys
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import_errors = []

try:
    from modules.language_detector import detect_languages, separate_by_language
except ImportError as e:
    import_errors.append(f"language_detector modülü yüklenemedi: {str(e)}")

try:
    import modules.duplicate_detector as duplicate_detector
except ImportError as e:
    import_errors.append(f"duplicate_detector modülü yüklenemedi: {str(e)}")

try:
    from modules.spam_detector import detect_spam
except ImportError as e:
    import_errors.append(f"spam_detector modülü yüklenemedi: {str(e)}")

try:
    from modules.text_cleaner import clean_text
except ImportError as e:
    import_errors.append(f"text_cleaner modülü yüklenemedi: {str(e)}")

try:
    from modules.prompt_converter import convert_to_prompt_completion
except ImportError as e:
    import_errors.append(f"prompt_converter modülü yüklenemedi: {str(e)}")

try:
    from utils.file_handler import save_processed_data, load_file
except ImportError as e:
    import_errors.append(f"file_handler modülü yüklenemedi: {str(e)}")


if import_errors:
    st.error("Bazı modüller yüklenemedi. Lütfen proje yapısını kontrol edin:")
    for error in import_errors:
        st.warning(error)

st.sidebar.header("İşlem Ayarları")


uploaded_file = st.sidebar.file_uploader("Veri dosyası yükle", type=["csv", "txt", "json"])

st.sidebar.subheader("İşlem Seçenekleri")
detect_lang = st.sidebar.checkbox("Dil Tanıma & Ayırma", value=True, disabled='language_detector' in [
    e.split(':')[0].strip().replace(' modülü yüklenemedi', '') for e in import_errors])
detect_dups = st.sidebar.checkbox("Duplicate Tespiti", value=True, disabled='duplicate_detector' in [
    e.split(':')[0].strip().replace(' modülü yüklenemedi', '') for e in import_errors])
detect_spam_option = st.sidebar.checkbox("Spam & Reklam Tespiti", value=True, disabled='spam_detector' in [
    e.split(':')[0].strip().replace(' modülü yüklenemedi', '') for e in import_errors])
clean_text_option = st.sidebar.checkbox("Metin Düzeltme", value=True, disabled='text_cleaner' in [
    e.split(':')[0].strip().replace(' modülü yüklenemedi', '') for e in import_errors])
convert_prompt = st.sidebar.checkbox("Prompt-Completion Dönüştürme", value=True, disabled='prompt_converter' in [
    e.split(':')[0].strip().replace(' modülü yüklenemedi', '') for e in import_errors])

with st.sidebar.expander("İleri Düzey Ayarlar"):

    target_languages = st.multiselect(
        "Hedef Diller",
        ["Türkçe", "İngilizce", "Almanca", "Fransızca", "İspanyolca", "Diğer"],
        default=["Türkçe", "İngilizce"]
    )

    similarity_threshold = st.slider(
        "Benzerlik Eşiği",
        min_value=0.5,
        max_value=1.0,
        value=0.85,
        step=0.01
    )

    spam_threshold = st.slider(
        "Spam Eşiği",
        min_value=0.1,
        max_value=1.0,
        value=0.7,
        step=0.01
    )

    normalize_case = st.checkbox("Büyük/Küçük Harf Normalizasyonu", value=True)
    remove_extra_spaces = st.checkbox("Fazla Boşlukları Kaldır", value=True)
    fix_punctuation = st.checkbox("Noktalama İşaretlerini Düzelt", value=True)

    prompt_format = st.selectbox(
        "Prompt Formatı",
        ["Soru-Cevap", "Talimat-Yanıt", "Diyalog", "Özel"]
    )

process_button = st.sidebar.button("İşlemi Başlat")


if uploaded_file is not None:

    file_details = {"Dosya Adı": uploaded_file.name, "Dosya Tipi": uploaded_file.type,
                    "Dosya Boyutu": f"{uploaded_file.size / 1024:.2f} KB"}
    st.write("### Yüklenen Dosya Bilgileri")
    st.json(file_details)

    df = load_file(uploaded_file)

    if df is not None:
        st.write("### Veri Ön İzleme (İlk 5 Satır)")
        st.dataframe(df.head())

        if process_button:
            progress_bar = st.progress(0)
            status_text = st.empty()

            results_container = st.container()

            with results_container:
                st.write("## İşlem Sonuçları")

                processed_df = df.copy()
                steps_completed = 0
                total_steps = sum([detect_lang, detect_dups, detect_spam_option, clean_text_option, convert_prompt])

                if detect_lang:
                    status_text.text("Dil tanıma ve ayırma işlemi yapılıyor...")

                    if "text" in processed_df.columns:
                        processed_df["detected_language"] = processed_df["text"].apply(detect_languages)

                        language_map = {
                            "Türkçe": "tr",
                            "İngilizce": "en",
                            "Almanca": "de",
                            "Fransızca": "fr",
                            "İspanyolca": "es"
                        }
                        target_lang_codes = [language_map.get(lang, lang) for lang in target_languages]

                        processed_df = processed_df[processed_df["detected_language"].isin(target_lang_codes)]

                        lang_stats = processed_df["detected_language"].value_counts()
                        st.write("### Dil Dağılımı")
                        st.bar_chart(lang_stats)

                    steps_completed += 1
                    progress_bar.progress(steps_completed / total_steps)


                if detect_dups:
                    status_text.text("Duplicate tespiti yapılıyor...")

                    if "text" in processed_df.columns:

                        processed_df["is_duplicate"] = duplicate_detector.detect_duplicates(processed_df["text"],
                                                                                            similarity_threshold)

                        unique_count_before = len(processed_df)
                        processed_df = processed_df[~processed_df["is_duplicate"]]
                        unique_count_after = len(processed_df)

                        st.write(f"### Duplicate Tespiti Sonuçları")
                        st.write(f"Kaldırılan duplicate sayısı: {unique_count_before - unique_count_after}")

                    steps_completed += 1
                    progress_bar.progress(steps_completed / total_steps)

                if detect_spam_option:
                    status_text.text("Spam ve reklam içeriği tespiti yapılıyor...")

                    if "text" in processed_df.columns:
                        processed_df["spam_score"] = processed_df["text"].apply(lambda x: detect_spam(x))

                        non_spam_count_before = len(processed_df)
                        processed_df = processed_df[processed_df["spam_score"] < spam_threshold]
                        non_spam_count_after = len(processed_df)

                        st.write(f"### Spam Tespiti Sonuçları")
                        st.write(
                            f"Filtrelenen spam/reklam içeriği sayısı: {non_spam_count_before - non_spam_count_after}")

                    steps_completed += 1
                    progress_bar.progress(steps_completed / total_steps)

                if clean_text_option:
                    status_text.text("Metin temizleme ve düzeltme işlemi yapılıyor...")

                    if "text" in processed_df.columns:

                        clean_params = {
                            "normalize_case": normalize_case,
                            "remove_extra_spaces": remove_extra_spaces,
                            "fix_punctuation": fix_punctuation
                        }

                        processed_df["cleaned_text"] = processed_df["text"].apply(
                            lambda x: clean_text(x, **clean_params)
                        )


                        st.write("### Metin Temizleme Örnekleri")
                        sample_df = processed_df[["text", "cleaned_text"]].head(3)
                        st.dataframe(sample_df)

                    steps_completed += 1
                    progress_bar.progress(steps_completed / total_steps)

                if convert_prompt:
                    status_text.text("Prompt-completion dönüştürme işlemi yapılıyor...")

                    text_column = "cleaned_text" if "cleaned_text" in processed_df.columns else "text"

                    if text_column in processed_df.columns:
                        prompt_completion_df = convert_to_prompt_completion(
                            processed_df,
                            text_column=text_column,
                            format_type=prompt_format
                        )

                        st.write("### Prompt-Completion Dönüşüm Örnekleri")
                        if not prompt_completion_df.empty:
                            st.dataframe(prompt_completion_df[["prompt", "completion"]].head(3))

                            processed_df = prompt_completion_df
                        else:
                            st.warning("Prompt-completion dönüşümü için uygun veri bulunamadı.")

                    steps_completed += 1
                    progress_bar.progress(steps_completed / total_steps)

                status_text.text("İşlem tamamlandı!")


                if not processed_df.empty:

                    output_filename = f"processed_{uploaded_file.name.split('.')[0]}.csv"
                    csv = processed_df.to_csv(index=False)

                    st.write("### İşlenmiş Veri")
                    st.dataframe(processed_df.head(10))


                    st.write("### İşlem İstatistikleri")
                    st.write(f"Başlangıç satır sayısı: {len(df)}")
                    st.write(f"İşlem sonrası satır sayısı: {len(processed_df)}")
                    st.write(f"Temizlenen veri oranı: {(1 - len(processed_df) / len(df)) * 100:.2f}%")


                    st.download_button(
                        label="İşlenmiş Veriyi İndir",
                        data=csv,
                        file_name=output_filename,
                        mime="text/csv"
                    )
                else:
                    st.error("İşlem sonrası veri boş. Filtreleme parametrelerini kontrol ediniz.")
    else:
        st.error("Dosya okunamadı. Lütfen dosya formatını kontrol ediniz.")
else:
    st.info(" Başlamak için sol menüden bir dosya yükleyin ve işlem seçeneklerini ayarlayın.")


    st.write("##  İş Akışı")
    st.write("""
    1. **Dil Tanıma & Ayırma**: Verilerin dilini otomatik olarak tespit eder ve istediğiniz dilleri filtrelemenize olanak tanır.
    2. **Duplicate Tespiti**: Aynı veya çok benzer içerikleri tespit ederek veri setinden çıkarır.
    3. **Spam & Reklam Tespiti**: Spam veya reklam içeriği olabilecek metinleri tespit eder.
    4. **Metin Düzeltme**: Metinlerdeki biçimsel sorunları giderir, fazla boşlukları kaldırır, noktalama işaretlerini düzeltir.
    5. **Prompt-Completion Dönüştürme**: Metinleri, LLM eğitimi için prompt-completion çiftlerine dönüştürür.
    """)

    st.write("##  Desteklenen Veri Formatları")
    st.code("""
    # CSV Örneği:
    id,text,metadata
    1,"Bu bir örnek metindir.","{'source': 'web'}"
    2,"This is a sample text.","{'source': 'book'}"

    # JSON Örneği:
    [
        {"id": 1, "text": "Bu bir örnek metindir.", "metadata": {"source": "web"}},
        {"id": 2, "text": "This is a sample text.", "metadata": {"source": "book"}}
    ]
    """)

st.markdown("---")
st.markdown(" LLM Veri Temizleme ve Ön-İşleme Aracı ")