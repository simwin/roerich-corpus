# Корпус теософских и рериховских текстов

Корпус в формате **JSONL** для вычислительного анализа: частотности, тематический поиск, конкордансы, сравнение исторических слоёв.

**Объём:** 33,182 записей, ≈7,978,350 слов, 98.0 MB.

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
| `corpus/ei_letters_corpus.jsonl` | 7,192 | 2,507,530 | 30.5 MB |
| `corpus/glossary_corpus.jsonl` | 2,780 | 134,851 | 2.0 MB |
| `corpus/grani_corpus.jsonl` | 14,171 | 2,671,692 | 32.2 MB |
| `corpus/mahatma_corpus.jsonl` | 1,433 | 384,602 | 4.7 MB |
| `corpus/sd_corpus.jsonl` | 11 | 1,423,904 | 17.3 MB |

## Схема

- `corpus/agni_corpus.jsonl` — поля: `source`, `book`, `ref`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/de_rochas_1895.jsonl` — поля: `source`, `author`, `year`, `edition`, `lang`, `chapter_id`, `chapter_num`, `chapter_title`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/ei_letters_corpus.jsonl` — поля: `source`, `edition`, `ref`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/glossary_corpus.jsonl` — поля: `source`, `headword`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/grani_corpus.jsonl` — поля: `file`, `year`, `date`, `text`, `words`, `chars`; текст в `text`
- `corpus/mahatma_corpus.jsonl` — поля: `source`, `ref`, `file`, `text`, `words`, `chars`; текст в `text`
- `corpus/sd_corpus.jsonl` — поля: `source`, `volume`, `part`, `file`, `text`, `words`, `chars`; текст в `text`

## Оговорки

- Конвертация из CHM/DOC: изредка теряется первая буква абзаца-буквицы. На поиск и частоты не влияет.
- Права на тексты принадлежат правообладателям изданий; репозиторий собран для личного исследовательского использования.
