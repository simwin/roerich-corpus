# Корпус теософских и рериховских текстов

Корпус в формате **JSONL** для вычислительного анализа: частотности, тематический поиск, конкордансы, сравнение исторических слоёв.

**Объём:** 61,394 записей, ≈14,044,726 слов, 313.7 MB.

## Быстрый старт

```bash
git clone --depth 1 https://github.com/simwin/roerich-corpus.git
```

```python
import json, gzip

def load(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]
```

## Состав

| файл | записей | слов | размер |
|---|---:|---:|---:|
| `corpus/agni_corpus.jsonl` | 7,585 | 776,136 | 10.8 MB |
| `corpus/de_rochas_1895.jsonl` | 10 | 79,635 | 493.8 KB |
| `corpus/ei_diaries_prolog.jsonl` | 6,352 | 1,362,106 | 35.5 MB |
| `corpus/ei_diaries_ug_kosmsotr.jsonl` | 2,197 | 704,907 | 18.6 MB |
| `corpus/ei_diaries_ug_mashinopis.jsonl` | 2,721 | 975,029 | 25.2 MB |
| `corpus/ei_diaries_ug_ognopyt_r1.jsonl` | 2,250 | 2,250 | 19.6 MB |
| `corpus/ei_diaries_ug_ognopyt_r2v1.jsonl` | 1,054 | 442,333 | 11.5 MB |
| `corpus/ei_diaries_ug_ognopyt_r2v2.jsonl` | 1,379 | 11,041 | 12.7 MB |
| `corpus/ei_diaries_ug_otdelnye.jsonl` | 2,571 | 680,384 | 18.5 MB |
| `corpus/ei_diaries_ug_pervichnaya.jsonl` | 5,281 | 5,281 | 30.6 MB |
| `corpus/ei_diaries_ug_uchenie.jsonl` | 4,133 | 1,464,626 | 39.3 MB |
| `corpus/ei_letters_corpus.jsonl` | 7,192 | 2,507,530 | 30.5 MB |
| `corpus/ei_letters_riga1940.jsonl` | 233 | 271,399 | 3.4 MB |
| `corpus/five_years_theosophy_1885.jsonl` | 41 | 147,020 | 894.0 KB |
| `corpus/glossary_corpus.jsonl` | 2,780 | 134,851 | 2.0 MB |
| `corpus/grani_corpus.jsonl` | 14,171 | 2,671,692 | 32.2 MB |
| `corpus/mahatma_corpus.jsonl` | 1,433 | 384,602 | 4.7 MB |
| `corpus/sd_corpus.jsonl` | 11 | 1,423,904 | 17.3 MB |

## Схема

- `corpus/agni_corpus.jsonl` — поля: `source`, `book`, `ref`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/de_rochas_1895.jsonl` — поля: `source`, `author`, `year`, `edition`, `lang`, `chapter_id`, `chapter_num`, `chapter_title`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/ei_diaries_prolog.jsonl` — поля: `source`, `edition`, `line`, `volume`, `date`, `place`, `tetrad_candidates`, `parallel_candidates`, `tetrad_ambiguous`, `text`, `words`, `chars`, `ref`, `seq`, `id`, `text_search`, `parallel_match`, `tetrad`, `tetrad_basis`; текст в `text`
- `corpus/ei_diaries_ug_kosmsotr.jsonl` — поля: `id`, `topic_id`, `series`, `topic_title`, `tetrad_no`, `gmr_no`, `author_no`, `gmr_series`, `pdf_url`, `form`, `lang`, `unit`, `n`, `n2`, `verso`, `text`, `text_search`, `date`, `date_basis`, `date_marks`, `date_scope`, `out_of_span`, `source_note`, `prod`, `words`, `chars`; текст в `text`
- `corpus/ei_diaries_ug_mashinopis.jsonl` — поля: `id`, `topic_id`, `series`, `topic_title`, `tetrad_no`, `gmr_no`, `author_no`, `gmr_series`, `pdf_url`, `form`, `lang`, `unit`, `n`, `n2`, `verso`, `text`, `text_search`, `date`, `date_basis`, `date_marks`, `date_scope`, `out_of_span`, `source_note`, `prod`, `words`, `chars`; текст в `text`
- `corpus/ei_diaries_ug_ognopyt_r1.jsonl` — поля: `id`, `topic_id`, `series`, `topic_title`, `tetrad_no`, `gmr_no`, `author_no`, `gmr_series`, `pdf_url`, `form`, `lang`, `unit`, `n`, `n2`, `verso`, `text`, `text_search`, `date`, `date_basis`, `date_marks`, `date_scope`, `out_of_span`, `source_note`, `prod`, `words`, `chars`; текст в `pdf_url`
- `corpus/ei_diaries_ug_ognopyt_r2v1.jsonl` — поля: `id`, `topic_id`, `series`, `topic_title`, `tetrad_no`, `gmr_no`, `author_no`, `gmr_series`, `pdf_url`, `form`, `lang`, `unit`, `n`, `n2`, `verso`, `text`, `text_search`, `date`, `date_basis`, `date_marks`, `date_scope`, `out_of_span`, `source_note`, `prod`, `words`, `chars`; текст в `text`
- `corpus/ei_diaries_ug_ognopyt_r2v2.jsonl` — поля: `id`, `topic_id`, `series`, `topic_title`, `tetrad_no`, `gmr_no`, `author_no`, `gmr_series`, `pdf_url`, `form`, `lang`, `unit`, `n`, `n2`, `verso`, `text`, `text_search`, `date`, `date_basis`, `date_marks`, `date_scope`, `out_of_span`, `source_note`, `prod`, `words`, `chars`; текст в `topic_title`
- `corpus/ei_diaries_ug_otdelnye.jsonl` — поля: `id`, `topic_id`, `series`, `topic_title`, `tetrad_no`, `gmr_no`, `author_no`, `gmr_series`, `pdf_url`, `form`, `lang`, `unit`, `n`, `n2`, `verso`, `text`, `text_search`, `date`, `date_basis`, `date_marks`, `date_scope`, `out_of_span`, `source_note`, `prod`, `words`, `chars`; текст в `text`
- `corpus/ei_diaries_ug_pervichnaya.jsonl` — поля: `id`, `topic_id`, `series`, `topic_title`, `tetrad_no`, `gmr_no`, `author_no`, `gmr_series`, `pdf_url`, `form`, `lang`, `unit`, `n`, `n2`, `verso`, `text`, `text_search`, `date`, `date_basis`, `date_marks`, `date_scope`, `out_of_span`, `source_note`, `prod`, `words`, `chars`; текст в `pdf_url`
- `corpus/ei_diaries_ug_uchenie.jsonl` — поля: `id`, `topic_id`, `series`, `topic_title`, `tetrad_no`, `gmr_no`, `author_no`, `gmr_series`, `pdf_url`, `form`, `lang`, `unit`, `n`, `n2`, `verso`, `text`, `text_search`, `date`, `date_basis`, `date_marks`, `date_scope`, `out_of_span`, `source_note`, `prod`, `words`, `chars`; текст в `text`
- `corpus/ei_letters_corpus.jsonl` — поля: `source`, `edition`, `ref`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/ei_letters_riga1940.jsonl` — поля: `source`, `edition`, `vol`, `n`, `kind`, `section`, `date_raw`, `date`, `date_prec`, `ref`, `text`, `words`, `chars`; текст в `text`
- `corpus/five_years_theosophy_1885.jsonl` — поля: `source`, `editor`, `year`, `orig_publication`, `edition`, `lang`, `section`, `article_num`, `article_title`, `author`, `author_basis`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/glossary_corpus.jsonl` — поля: `source`, `headword`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/grani_corpus.jsonl` — поля: `file`, `year`, `date`, `text`, `words`, `chars`; текст в `text`
- `corpus/mahatma_corpus.jsonl` — поля: `source`, `ref`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/sd_corpus.jsonl` — поля: `source`, `volume`, `part`, `file`, `text`, `words`, `chars`; текст в `text`

## Оговорки

- Конвертация из CHM/DOC: изредка теряется первая буква абзаца-буквицы. На поиск и частоты не влияет.
- Права на тексты принадлежат правообладателям изданий; репозиторий собран для личного исследовательского использования.
