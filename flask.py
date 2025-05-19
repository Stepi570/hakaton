from flask import Flask, render_template,request,redirect, url_for,flash
from bd import *
app=Flask(__name__)
new()
@app.route('/rigister', methods=['POST', 'GET'])
def rigister():
   


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
    app.run(debug=True)
