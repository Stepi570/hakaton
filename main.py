from flask import Flask, render_template,request,redirect, url_for,flash
from bd import *

app=Flask(__name__)

@app.route('/rigister', methods=['POST', 'GET'])
def rigister():
    return render_template('home.html') 

@app.route('/home/<string:id>/pays')
def home_pays(id):
    return render_template('webHV2.html') 

@app.route('/home/<string:id>')
def home(id):
    all_info=all_human(id)
    if all_info==[]:
        return render_template('erorr.html')
    all_info=all_info[0]
    return render_template('webHV1.html',card_last=(str(all_info[7]))[12:],card=' '.join([str(all_info[7])[i:i+4] for i in range(0, len(str(all_info[7])), 4)]),
    money=all_info[6],card_date=all_info[8],id=id)


@app.route('/registr', methods=['POST', 'GET'])
def inlet():
    if request.method=="POST":
        lastName = request.form['lastName']
        firstName = request.form['firstName']
        middleName = request.form['middleName']
        birthDate = request.form['birthDate']
        passportNumber = (request.form['passportNumber']).replace(" ","")
        if chek_pasport(passportNumber):
            return render_template('webHV.html',info="Данный паспорт уже есть в системе")
        if "Ошибка" in str(new_human(lastName,firstName,middleName,passportNumber,birthDate)):
            return render_template('erorr.html')
        id=(chek_pasport(passportNumber))[0][0]
        return redirect(url_for('home',id=id))
    else:
        return render_template('webHV.html',info="Регистрация в банковском приложении")

@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method=="POST":
        user = request.form['pasport_input']
        password=request.form['card_input']
        id=chek_human(user,password)
        if id != []:
            id=id[0]
            return redirect(url_for('home', id=id[0])) #При удачной регестрации проход на страницу 
        else:
            return render_template('vhod.html', info="Неверный паспорт или карта") #При неудачной регестрациии 
    else:
        return render_template('vhod.html', info="Вход в банковское приложение")

if __name__=="__main__":
    app.run(debug=True)
    
