from flask import Flask
from flask import render_template
from main import Data

app = Flask(__name__)

@app.route('/')
def start():
    return render_template("index.html")

@app.route('/data.html')
def data():
    a = Data()
    data = a.getData()
    a.saveData(data)
    data = a.getDataFromTable()
    print(data[0][0])
    print(data[0][1])
    print(data[0][2])
    print(data[0][3])
    print(data[0][4])
    return render_template("data.html", data=data)


app.run(debug = True)