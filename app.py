from flask import Flask, render_template, request
from markupsafe import Markup, escape
import pandas as pd
import requests
import json
import re

app = Flask(__name__)

# ------------------------------------------------------------
# Jinja カスタムフィルタ: テキスト中の http(s) URL を <a> に変換
# ------------------------------------------------------------
URL_RE = re.compile(r'(https?://[^\s<>"\'()]+)')

@app.template_filter('linkify')          # ← デコレータで登録
def linkify_filter(text):
    """テキスト中の http(s) URL を別タブで開く <a> タグに変換する。"""
    if not text:
        return ''
    text = str(text)
    parts = URL_RE.split(text)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            url = part
            trailing = ''
            while url and url[-1] in '.,;:!?)':
                trailing = url[-1] + trailing
                url = url[:-1]
            out.append(
                f'<a href="{escape(url)}" target="_blank" '
                f'rel="noopener noreferrer">{escape(url)}</a>'
                f'{escape(trailing)}'
            )
        else:
            out.append(str(escape(part)))
    return Markup(''.join(out))
# ------------------------------------------------------------

@app.route('/')
def index():
    lang = request.args.get('lang', 'ja')
    news = pd.read_csv("news.csv", encoding="utf-8-sig", keep_default_na=False)
    news = news.to_dict(orient="records")
    return render_template('index.html', lang=lang, news=news)

@app.route('/about')
def about():
    lang = request.args.get('lang', 'ja')
    return render_template('about.html', lang=lang)

@app.route('/research')
def research():
    lang = request.args.get('lang', 'ja')
    return render_template('research.html', lang=lang)

@app.route('/projects')
def projects():
    lang = request.args.get('lang', 'ja')
    return render_template('projects.html', lang=lang)

@app.route('/publications')
def publications():
    lang = request.args.get('lang', 'ja')
    url = "https://api.researchmap.jp/C_Fujiwara"
    response = requests.get(url)
    jsonData = response.json()

    data_paper = pd.read_csv("data_paper.csv", encoding="Shift-Jis")
    int_pre    = pd.read_csv("int_pre.csv",    encoding="Shift-Jis")
    dom_pre    = pd.read_csv("dom_pre.csv",    encoding="Shift-Jis")

    data_paper = data_paper.to_dict(orient="records")
    int_pre    = int_pre.to_dict(orient="records")
    dom_pre    = dom_pre.to_dict(orient="records")

    return render_template('publications.html',
                           lang=lang,
                           data_paper=data_paper,
                           int_pre=int_pre,
                           dom_pre=dom_pre)

@app.route('/conferences')
def conferences():
    lang = request.args.get('lang', 'ja')
    return render_template('conferences.html', lang=lang)

@app.route('/contact')
def contact():
    lang = request.args.get('lang', 'ja')
    return render_template('contact.html', lang=lang)

@app.route('/note/python')
def note_python():
    lang = request.args.get('lang', 'ja')
    return render_template('note_python.html', lang=lang)

@app.route('/note/first_principles')
def note_first_principles():
    lang = request.args.get('lang', 'ja')
    return render_template('note_first_principles.html', lang=lang)

if __name__ == '__main__':
    app.run(debug=True)