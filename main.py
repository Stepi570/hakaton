from flask import Flask, render_template,request,redirect, url_for,flash
from bd import *

app=Flask(__name__)

@app.route('/rigister', methods=['POST', 'GET'])
def rigister():
    return render_template('home.html') 

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/inlet', methods=['POST', 'GET'])
def inlet():
    return redirect(url_for('home'))

@app.route('/')
def start():
    return render_template('vibor.html')

if __name__=="__main__":
    print(clasic_transaktion(4111111111111111,7890123456789012, 500))
    new()
    app.run(debug=True)
    