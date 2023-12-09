from flask import Flask
from flask import render_template
from main import Data

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    a = Data()
    data = a.getData()
    return render_template("index.html", data=data)


app.run(debug = True)