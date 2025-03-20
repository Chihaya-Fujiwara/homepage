from flask import Flask, render_template, request

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

@app.route('/research/python')
def research_python():
    lang = request.args.get('lang', 'ja')
    return render_template('research_python.html', lang=lang)

@app.route('/research/dft')

def research_dft():
    lang = request.args.get('lang', 'ja')
    return render_template('research_dft.html', lang=lang)

@app.route('/projects')
def projects():
    lang = request.args.get('lang', 'ja')
    return render_template('projects.html', lang=lang)

@app.route('/publications')
def publications():
    lang = request.args.get('lang', 'ja')
    return render_template('publications.html', lang=lang)

@app.route('/conferences')
def conferences():
    lang = request.args.get('lang', 'ja')
    return render_template('conferences.html', lang=lang)

@app.route('/contact')
def contact():
    lang = request.args.get('lang', 'ja')
    return render_template('contact.html', lang=lang)

@app.route('/research/accordion')
def research_accordion():
    lang = request.args.get('lang', 'ja')
    return render_template('research_accordion.html', lang=lang)

@app.route('/gallery')
def gallery():
    lang = request.args.get('lang', 'ja')
    return render_template('gallery.html', lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
