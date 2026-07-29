#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corpus.py — загрузчик корпуса, применяющий правила из corpus_rules.json.

Смысл: правила дедупликации и исключений записаны в README прозой. Проза
забывается. Здесь они выполняются автоматически, поэтому ошибиться нельзя.

Быстрый старт:
    import corpus
    c = corpus.Corpus()                 # из текущей папки
    c.summary()                         # что загрузилось
    c.kwic('терафим')                   # поиск с контекстом
    c.freq(['терафим', 'наслое'])       # частоты на 10 000 слов по произведениям
"""

import gzip
import json
import os
import re
import unicodedata

DEFAULT_RULES = 'corpus_rules.json'


def _open(path):
    if path.endswith('.gz'):
        return gzip.open(path, 'rt', encoding='utf-8')
    return open(path, encoding='utf-8')


def _find(root, name):
    for cand in (name, name + '.gz'):
        p = os.path.join(root, cand)
        if os.path.exists(p):
            return p
        p = os.path.join(root, 'corpus', cand)
        if os.path.exists(p):
            return p
    return None


class Corpus:
    def __init__(self, root='.', rules=DEFAULT_RULES, strict=True, verbose=True):
        """strict=True — применять правила README (дедуп, исключения)."""
        self.root = root
        self.strict = strict
        rules_path = _find(root, rules) or os.path.join(root, rules)
        with open(rules_path, encoding='utf-8') as fh:
            self.rules = json.load(fh)
        self.text_field = self.rules.get('text_field', 'text')
        self.data = {}
        self.dropped = {}
        for fname, meta in self.rules['files'].items():
            path = _find(root, fname)
            if not path:
                if verbose:
                    print(f'  пропущен (не найден): {fname}')
                continue
            recs = []
            with _open(path) as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        recs.append(json.loads(line))
            before = len(recs)
            dd = meta.get('dedup')
            if strict and dd:
                recs = [r for r in recs
                        if dd['keep_contains'] in str(r.get(dd['field'], ''))]
            self.dropped[fname] = before - len(recs)
            self.data[fname] = recs
            if verbose:
                extra = f'  (отброшено дублей: {before - len(recs)})' if before != len(recs) else ''
                print(f'  {fname}: {len(recs):,} записей{extra}')

    # ---------- выборки ----------

    def files(self, for_frequency=False, include_secondary=True):
        out = []
        for fname, meta in self.rules['files'].items():
            if fname not in self.data:
                continue
            if for_frequency and meta.get('exclude_from_frequency'):
                continue
            out.append(fname)
        return out

    def records(self, files=None, layer=None, for_frequency=False):
        files = files or self.files(for_frequency=for_frequency)
        if isinstance(files, str):
            files = [files]
        for fname in files:
            meta = self.rules['files'][fname]
            if layer and meta.get('layer') != layer:
                continue
            for r in self.data.get(fname, []):
                yield fname, r

    def words(self, files=None, for_frequency=False):
        total = 0
        for fname, r in self.records(files, for_frequency=for_frequency):
            w = r.get(self.rules.get('words_field', 'words'))
            total += w if isinstance(w, int) else len(str(r.get(self.text_field, '')).split())
        return total

    # ---------- поиск ----------

    @staticmethod
    def _pat(stem, whole_stem=True):
        """Русская морфология: ищем по корню. 'терафим' → терафим/терафима/…"""
        s = re.escape(stem)
        return re.compile((r'\b' + s) if whole_stem else s, re.IGNORECASE)

    def kwic(self, stem, files=None, layer=None, window=220, limit=None,
             show=True):
        """Поиск по корню с контекстом. Большие записи (sd_corpus) режутся окном."""
        pat = self._pat(stem)
        hits = []
        for fname, r in self.records(files, layer=layer):
            text = str(r.get(self.text_field, ''))
            for m in pat.finditer(text):
                a = max(0, m.start() - window)
                b = min(len(text), m.end() + window)
                ctx = re.sub(r'\s+', ' ', text[a:b]).strip()
                hits.append({
                    'file': fname,
                    'ref': self._ref(fname, r),
                    'context': ('…' if a > 0 else '') + ctx + ('…' if b < len(text) else ''),
                    'match': m.group(0),
                })
                if limit and len(hits) >= limit:
                    break
            if limit and len(hits) >= limit:
                break
        if show:
            print(f'«{stem}» — найдено вхождений: {len(hits)}\n')
            for h in hits[:limit or 40]:
                print(f'[{h["ref"]}]')
                print(f'  {h["context"]}\n')
        return hits

    def _ref(self, fname, rec):
        meta = self.rules['files'][fname]
        parts = []
        for key in ('source', 'book', 'volume', 'part', 'edition',
                    'ref', 'headword', 'date', 'year'):
            v = rec.get(key)
            if v not in (None, ''):
                parts.append(str(v))
        return ' · '.join(parts) if parts else meta['work']

    # ---------- частоты ----------

    def freq(self, stems, per=10000, group='file', show=True):
        """Частоты на N слов. group='file' | 'layer'."""
        if isinstance(stems, str):
            stems = [stems]
        pats = {s: self._pat(s) for s in stems}
        buckets = {}
        for fname in self.files(for_frequency=True):
            meta = self.rules['files'][fname]
            key = meta['work'] if group == 'file' else \
                self.rules['layers'][meta['layer']]['label']
            b = buckets.setdefault(key, {'words': 0, **{s: 0 for s in stems}})
            for _, r in self.records([fname]):
                text = str(r.get(self.text_field, ''))
                w = r.get('words')
                b['words'] += w if isinstance(w, int) else len(text.split())
                for s, p in pats.items():
                    b[s] += len(p.findall(text))
        rows = []
        for key, b in buckets.items():
            row = {'группа': key, 'слов': b['words']}
            for s in stems:
                row[s] = b[s]
                row[f'{s}/{per//1000}k'] = round(b[s] * per / b['words'], 3) if b['words'] else 0.0
            rows.append(row)
        if show:
            self._table(rows)
        return rows

    @staticmethod
    def _table(rows):
        if not rows:
            return
        cols = list(rows[0].keys())
        w = {c: max(len(str(c)), *(len(f'{r[c]:,}' if isinstance(r[c], int) else str(r[c]))
                                   for r in rows)) for c in cols}
        print(' '.join(str(c).ljust(w[c]) for c in cols))
        print(' '.join('-' * w[c] for c in cols))
        for r in rows:
            print(' '.join((f'{r[c]:,}' if isinstance(r[c], int) else str(r[c])).ljust(w[c])
                           for c in cols))

    # ---------- сводка ----------

    def summary(self):
        rows = []
        for fname in self.files():
            meta = self.rules['files'][fname]
            rows.append({
                'файл': fname,
                'слой': self.rules['layers'][meta['layer']]['label'],
                'записей': len(self.data[fname]),
                'слов': self.words([fname]),
                'в частоты': 'нет' if meta.get('exclude_from_frequency') else 'да',
            })
        self._table(rows)
        print(f'\nВсего слов (для частотного анализа): {self.words(for_frequency=True):,}')
        drops = {k: v for k, v in self.dropped.items() if v}
        if drops:
            print('Отброшено дублей по правилам README:',
                  ', '.join(f'{k}: {v:,}' for k, v in drops.items()))


if __name__ == '__main__':
    c = Corpus()
    print()
    c.summary()
