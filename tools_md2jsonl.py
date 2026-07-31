#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md -> jsonl для приватного репозитория puchko-sources.
Режет по заголовкам, хранит путь в иерархии, имена файлов ASCII.
Запускать в папке, где лежат три .md."""
import re, json, io, os

META = {
 'Пучко_Радиэстезическое_познание_человека.md': dict(
    out='puchko_rpch.jsonl',
    source='Радиэстезическое познание человека',
    subtitle='Система самодиагностики, самоисцеления и самопознания человека',
    author='Пучко Л. Г.', year=None,
    year_note='издание в файле не датировано; по библиографии >=1997; в проекте датируется «до 2006»',
    edition='fb2 royallib.com, cp1251->UTF-8, 29 иллюстраций заменены пометками [рисунок: N]'),
 'Пучко_Новые_вопросы_и_новые_ответы_2009.md': dict(
    out='puchko_new_questions_2009.jsonl',
    source='Многомерная медицина. Новые вопросы и новые ответы',
    subtitle='', author='Пучко Л. Г.', year=2009, year_note='',
    edition='АНС/АСТ/Астрель, Москва, 2009, ISBN 978-5-17-064156-7; из fb2, картинки удалены'),
 'Сборник_Новые_алгоритмы_Многомерной_медицины_2012.md': dict(
    out='sbornik_new_algorithms_2012.jsonl',
    source='Новые алгоритмы Многомерной медицины',
    subtitle='Сборник, серия «Международный Клуб Многомерной медицины имени Л. Г. Пучко»',
    author='Сборник, под ред. Непокойчицкого Г. А.', year=2012, year_note='',
    edition='АНС/АСТ/Астрель, 2012, ISBN 978-5-271-41429-9; из fb2, картинки удалены'),
}

HEAD = re.compile(r'^(#{2,6})\s+(.*\S)\s*$')

def slug(s, n):
    """ASCII-идентификатор секции: sec0001 + порядковый номер"""
    return 'sec%04d' % n

for src, m in META.items():
    if not os.path.exists(src):
        print('НЕТ ФАЙЛА:', src)
        continue
    lines = io.open(src, encoding='utf-8', errors='replace').read().split('\n')

    stack, cur, recs = [], None, []
    def flush():
        if cur and cur['buf']:
            txt = '\n'.join(cur['buf']).strip()
            if txt:
                w = len(re.findall(r'\S+', txt))
                recs.append(dict(
                    source=m['source'], subtitle=m['subtitle'], author=m['author'],
                    year=m['year'], year_note=m['year_note'], edition=m['edition'],
                    lang='ru', file=src,
                    section_id=slug(cur['title'], len(recs) + 1),
                    section_level=cur['level'],
                    section_title=cur['title'],
                    path=' / '.join(cur['path']),
                    text=txt, words=w, chars=len(txt)))
        if cur:
            cur['buf'] = []

    for ln in lines:
        h = HEAD.match(ln)
        if h:
            flush()
            lvl, title = len(h.group(1)), h.group(2)
            while stack and stack[-1][0] >= lvl:
                stack.pop()
            stack.append((lvl, title))
            cur = dict(level=lvl, title=title, path=[t for _, t in stack], buf=[])
        else:
            if cur is None:
                cur = dict(level=1, title='(преамбула)', path=['(преамбула)'], buf=[])
            cur['buf'].append(ln)
    flush()

    with io.open(m['out'], 'w', encoding='utf-8') as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    tot_src = len(re.findall(r'\S+', '\n'.join(lines)))
    tot_out = sum(r['words'] for r in recs)
    print('%-38s -> %-34s %4d записей | слов: %6d из %6d (%.1f%% сохранено)' %
          (src[:38], m['out'], len(recs), tot_out, tot_src, 100.0 * tot_out / tot_src))
