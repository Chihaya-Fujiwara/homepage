from flask import Flask, render_template, request
import pandas as pd
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    lang = request.args.get('lang', 'ja')
    return render_template('index.html', lang=lang)

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
    
    data_paper = pd.read_csv("data_paper.csv",encoding="Shift-Jis")
    int_pre = pd.read_csv("int_pre.csv",encoding="Shift-Jis")
    dom_pre = pd.read_csv("dom_pre.csv",encoding="Shift-Jis")

    data_paper = data_paper.to_dict(orient="records")
    int_pre = int_pre.to_dict(orient="records")
    dom_pre = dom_pre.to_dict(orient="records")
    
    # HTML にデータを渡す
    return render_template('publications.html', lang=lang,data_paper=data_paper,int_pre=int_pre,dom_pre=dom_pre)
    

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

#@app.route('/gallery')
#def gallery():
#    lang = request.args.get('lang', 'ja')
#    return render_template('gallery.html', lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
