# LLM Veri Temizleme ve Ön-İşleme Aracı

Bu araç, Büyük Dil Modeli (LLM) eğitimi için ham verileri temizleyen, normalize eden ve etiketleyen kapsamlı bir işlem hattı sunar. Karmaşık verileri yüksek kaliteli eğitim çiftlerine dönüştürmek için çeşitli işleme aşamaları içerir.

## Özellikler

- **Dil Tanıma ve Filtreleme**: Metin dilini otomatik olarak tespit eder ve tercih ettiğiniz dillere göre filtreler.
- **Duplicate Tespiti**: Eğitim verilerindeki tekrarları önlemek için tam ve yakın duplicate içerikleri tespit eder ve kaldırır.
- **Spam ve Reklam Tespiti**: Eğitim setinizi kirletebilecek spam içeriklerini ve reklamları tespit ederek filtreler.
- **Metin Temizleme**: Noktalama işaretlerini düzelterek, fazla boşlukları kaldırarak ve formatı standartlaştırarak metni normalize eder.
- **Prompt-Completion Dönüşümü**: Metinleri LLM eğitimine hazır prompt-completion çiftlerine dönüştürür.

### Adımlar

```bash
# Repository'yi klonlayın
git clone https://github.com/sarizeybekk/data-processor-pipeline.git
cd data-processor-pipeline

# Bağımlılıkları yükleyin
pip install -r requirements.txt
