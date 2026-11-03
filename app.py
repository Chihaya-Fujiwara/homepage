from datetime import date
import re

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup, escape
import pandas as pd

app = Flask(__name__)


# ------------------------------------------------------------
# 共通ヘルパー
# ------------------------------------------------------------
def get_lang():
    """?lang=ja / ?lang=en を取得（それ以外は ja）。"""
    lang = request.args.get('lang', 'ja')
    return lang if lang in ('ja', 'en') else 'ja'


def read_csv(path):
    """UTF-8 (BOM付き含む) → Shift-JIS の順で読み込みを試す。"""
    for enc in ('utf-8-sig', 'cp932'):
        try:
            df = pd.read_csv(path, encoding=enc, keep_default_na=False, dtype=str)
            return df.to_dict(orient='records')
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f'Cannot decode {path}')


@app.context_processor
def inject_globals():
    lang = get_lang()

    def lang_url(target):
        """現在のページを別言語で開く URL。"""
        if request.endpoint is None:
            return '?lang=' + target
        args = dict(request.view_args or {})
        args['lang'] = target
        return url_for(request.endpoint, **args)

    return dict(lang=lang, ja=(lang == 'ja'), lang_url=lang_url,
                current_year=date.today().year)


# ------------------------------------------------------------
# Jinja フィルタ
# ------------------------------------------------------------
URL_RE = re.compile(r'(https?://[^\s<>"\'()（）、。]+)')

# 化学式の数字を下付きにする（Li2HfBr6 → Li<sub>2</sub>HfBr<sub>6</sub>）
ELEMENTS = set("""H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn
Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm
Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U X""".split())
FORMULA_RE = re.compile(
    r'(?<![A-Za-z0-9])'
    r'(?:(?:[A-Z][a-z]?|\((?:[A-Z][a-z]?[,\s]*)+\))\d{0,2}){2,}'
    r'(?![A-Za-z0-9])')
SYMBOL_RE = re.compile(r'[A-Z][a-z]?')


def _chem(text):
    """エスケープ済みテキスト中の化学式に <sub> を付ける。"""
    def repl(m):
        s = m.group(0)
        if not re.search(r'\d', s):
            return s
        if not all(sym in ELEMENTS for sym in SYMBOL_RE.findall(s)):
            return s
        return re.sub(r'(?<=[A-Za-z)])(\d{1,2})', r'<sub>\1</sub>', s)
    return FORMULA_RE.sub(repl, text)


def _short_url(url):
    """表示用に URL を短くする（doi.org は doi:xxx、それ以外はドメイン名 ↗）。"""
    m = re.match(r'https?://(?:dx\.)?doi\.org/(.+)', url)
    if m:
        return 'doi:' + m.group(1)
    host = re.sub(r'^www\.', '', url.split('/')[2])
    return host + ' ↗'


@app.template_filter('rich')
def rich_filter(text):
    """URL をリンク化し、化学式を下付き表示にする。"""
    if not text:
        return ''
    parts = URL_RE.split(str(text))
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            url, trailing = part, ''
            while url and url[-1] in '.,;:!?)':
                trailing = url[-1] + trailing
                url = url[:-1]
            out.append(f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer">'
                       f'{escape(_short_url(url))}</a>{escape(trailing)}')
        else:
            out.append(_chem(str(escape(part))))
    return Markup(''.join(out))


# 旧テンプレート互換
app.add_template_filter(rich_filter, 'linkify')

ME_RE = re.compile(r'(Chihaya\.?\s+Fujiwara|C\.\s?Fujiwara|藤原\s?千隼|千隼\s?藤原)')


@app.template_filter('authors')
def authors_filter(text):
    """著者リスト中の自分の名前を強調する。"""
    if not text:
        return ''
    escaped = str(escape(str(text)))
    return Markup(ME_RE.sub(r'<strong class="me">\1</strong>', escaped))


@app.template_filter('doi')
def doi_filter(text):
    """'doi: 10.xxxx/...' → '10.xxxx/...'（空なら空文字）"""
    if not text:
        return ''
    return re.sub(r'^\s*doi:\s*', '', str(text), flags=re.I).strip()


# ------------------------------------------------------------
# ルーティング
# ------------------------------------------------------------
@app.route('/')
def index():
    news = read_csv('news.csv')
    return render_template('index.html', news=news)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/research')
def research():
    return render_template('research.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/publications')
def publications():
    return render_template('publications.html',
                           data_paper=read_csv('data_paper.csv'),
                           int_pre=read_csv('int_pre.csv'),
                           dom_pre=read_csv('dom_pre.csv'))


@app.route('/conferences')
def conferences():
    return redirect(url_for('publications', lang=get_lang(), _anchor='intl-conferences'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/note/python')
def note_python():
    return render_template('note_python.html')


@app.route('/note/first_principles')
def note_first_principles():
    return render_template('note_first_principles.html')


if __name__ == '__main__':
    app.run(debug=True)
