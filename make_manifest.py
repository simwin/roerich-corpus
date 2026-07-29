#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор MANIFEST.txt и README.md для корпусного репозитория.
Запускать из корня репозитория:

    python3 make_manifest.py --owner ТВОЙ_ЛОГИН --repo roerich-corpus

Скрипт сам обходит подпапки, читает .jsonl / .jsonl.gz, определяет схему
полей, считает записи и слова, и собирает файлы с прямыми raw-ссылками.
"""

import argparse, gzip, io, json, os, sys

SKIP_DIRS = {'.git', '.github', '__pycache__'}


def open_any(path):
    if path.endswith('.gz'):
        return io.TextIOWrapper(gzip.open(path, 'rb'), encoding='utf-8')
    return open(path, encoding='utf-8')


def pick_text_field(rec):
    """Текстовое поле = самая длинная строка в записи."""
    best, best_len = None, -1
    for k, v in rec.items():
        if isinstance(v, str) and len(v) > best_len:
            best, best_len = k, len(v)
    return best


def scan(path):
    n_rec = n_words = 0
    keys, text_field, sample = [], None, None
    with open_any(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if n_rec == 0:
                keys = list(rec.keys())
                text_field = pick_text_field(rec)
                sample = {k: (v[:60] + '…' if isinstance(v, str) and len(v) > 60 else v)
                          for k, v in rec.items()}
            n_rec += 1
            if text_field and isinstance(rec.get(text_field), str):
                n_words += len(rec[text_field].split())
    return dict(records=n_rec, words=n_words, keys=keys,
                text_field=text_field, sample=sample)


def human(nbytes):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if nbytes < 1024 or unit == 'GB':
            return f'{nbytes:.1f} {unit}'
        nbytes /= 1024


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--owner', required=True)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--branch', default='main')
    ap.add_argument('--title', default='Корпус теософских и рериховских текстов')
    args = ap.parse_args()

    base = f'https://raw.githubusercontent.com/{args.owner}/{args.repo}/{args.branch}'
    root = os.getcwd()

    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if not (fn.endswith('.jsonl') or fn.endswith('.jsonl.gz')):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, '/')
            sys.stderr.write(f'  сканирую {rel} …\n')
            info = scan(full)
            info.update(rel=rel, size=os.path.getsize(full), url=f'{base}/{rel}')
            files.append(info)

    if not files:
        sys.exit('Не найдено ни одного .jsonl — запусти из корня репозитория.')

    files.sort(key=lambda f: f['rel'])
    tot_rec = sum(f['records'] for f in files)
    tot_wrd = sum(f['words'] for f in files)
    tot_sz = sum(f['size'] for f in files)

    # ---------- MANIFEST.txt ----------
    L = []
    L.append('MANIFEST — КОРПУС ДЛЯ АНАЛИЗА')
    L.append('=' * 80)
    L.append('Назначение: этот файл лежит И в репозитории, И в базе знаний проекта.')
    L.append('Он говорит ассистенту, ЧТО и ГДЕ лежит, чтобы корпус подтягивался')
    L.append('одной командой в любом новом чате, не занимая базу знаний.')
    L.append('')
    L.append(f'Репозиторий: https://github.com/{args.owner}/{args.repo}')
    L.append(f'Ветка: {args.branch}')
    L.append(f'Формат: JSONL — одна запись на строку, UTF-8.')
    L.append('')
    L.append('КАК ПОДТЯНУТЬ ВЕСЬ КОРПУС (в чате с исполнением кода):')
    L.append(f'  git clone --depth 1 https://github.com/{args.owner}/{args.repo}.git')
    L.append('КАК ПОДТЯНУТЬ ОДИН ФАЙЛ:')
    L.append(f'  curl -sL -O {files[0]["url"]}')
    L.append('Файлы .jsonl.gz читаются напрямую: gzip.open(path, "rt", encoding="utf-8")')
    L.append('')
    L.append('-' * 80)
    L.append('СОСТАВ')
    L.append('-' * 80)
    L.append(f'{"файл":<46}{"записей":>9}{"слов":>12}{"размер":>11}')
    for f in files:
        L.append(f'{f["rel"]:<46}{f["records"]:>9,}{f["words"]:>12,}{human(f["size"]):>11}')
    L.append(f'{"ИТОГО":<46}{tot_rec:>9,}{tot_wrd:>12,}{human(tot_sz):>11}')
    L.append('')
    L.append('-' * 80)
    L.append('СХЕМА ПОЛЕЙ (по первой записи каждого файла)')
    L.append('-' * 80)
    for f in files:
        L.append(f'• {f["rel"]}')
        L.append(f'    поля: {", ".join(f["keys"])}')
        L.append(f'    текст в поле: "{f["text_field"]}"')
        L.append(f'    ссылка: {f["url"]}')
        L.append(f'    пример: {json.dumps(f["sample"], ensure_ascii=False)[:300]}')
        L.append('')
    L.append('-' * 80)
    L.append('ОГОВОРКИ')
    L.append('-' * 80)
    L.append('• Тексты конвертированы из CHM/DOC; изредка теряется первая буква')
    L.append('  абзаца-буквицы (артефакт конвертации). На поиск и частоты не влияет.')
    L.append('• Права на тексты принадлежат правообладателям изданий; репозиторий')
    L.append('  собран для личного исследовательского использования.')

    open('MANIFEST.txt', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    # ---------- README.md ----------
    R = []
    R.append(f'# {args.title}')
    R.append('')
    R.append('Корпус в формате **JSONL** для вычислительного анализа: частотности, '
             'тематический поиск, конкордансы, сравнение исторических слоёв.')
    R.append('')
    R.append(f'**Объём:** {tot_rec:,} записей, ≈{tot_wrd:,} слов, {human(tot_sz)}.')
    R.append('')
    R.append('## Быстрый старт')
    R.append('')
    R.append('```bash')
    R.append(f'git clone --depth 1 https://github.com/{args.owner}/{args.repo}.git')
    R.append('```')
    R.append('')
    R.append('```python')
    R.append('import json, gzip')
    R.append('')
    R.append('def load(path):')
    R.append('    op = gzip.open if path.endswith(".gz") else open')
    R.append('    with op(path, "rt", encoding="utf-8") as fh:')
    R.append('        return [json.loads(l) for l in fh if l.strip()]')
    R.append('```')
    R.append('')
    R.append('## Состав')
    R.append('')
    R.append('| файл | записей | слов | размер |')
    R.append('|---|---:|---:|---:|')
    for f in files:
        R.append(f'| `{f["rel"]}` | {f["records"]:,} | {f["words"]:,} | {human(f["size"])} |')
    R.append('')
    R.append('## Схема')
    R.append('')
    for f in files:
        R.append(f'- `{f["rel"]}` — поля: `{"`, `".join(f["keys"])}`; '
                 f'текст в `{f["text_field"]}`')
    R.append('')
    R.append('## Оговорки')
    R.append('')
    R.append('- Конвертация из CHM/DOC: изредка теряется первая буква абзаца-буквицы. '
             'На поиск и частоты не влияет.')
    R.append('- Права на тексты принадлежат правообладателям изданий; '
             'репозиторий собран для личного исследовательского использования.')

    open('README.md', 'w', encoding='utf-8').write('\n'.join(R) + '\n')

    print(f'\nГотово: MANIFEST.txt и README.md')
    print(f'Файлов: {len(files)} · записей: {tot_rec:,} · слов: {tot_wrd:,} · {human(tot_sz)}')


if __name__ == '__main__':
    main()
