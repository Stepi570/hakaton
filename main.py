from time import sleep
from flask import Flask, render_template,request,redirect, url_for,flash
from bd import *
import threading
import datetime

app=Flask(__name__)

@app.route('/rigister', methods=['POST', 'GET'])
def rigister():
    return render_template('home.html') 

@app.route('/home/<string:id>/pays', methods=['GET', 'POST'])
def home_pays(id):
    all_info=all_human(id)
    if request.method=="GET":
        if all_info==[]:
            return render_template('erorr.html')
        all_info=all_info[0]
        return render_template('webHV2.html', id=id,card_last=(str(all_info[7]))[12:],money=all_info[6],info="Новый перевод")
    else:
        kard=(request.form["cardNumber"]).replace(" ","")
        summa=(request.form["amount"])
        if all_info==[]:
            return render_template('erorr.html')
        all_info=all_info[0]
        if chek_card(kard):
            return render_template('webHV2.html', card_last=(str(all_info[7]))[12:],money=all_info[6],info="Данный номер карты не найден. Пожалуйста, проверьте правильность введенного номера карты",id=id)
        oplsta=(clasic_transaktion((all_info)[7],kard,summa))
        if "Ошибка" in str(oplsta):
            return render_template('webHV2.html', card_last=(str(all_info[7]))[12:],money=all_info[6],info=f"{oplsta}",id=id)
        else:
            return render_template('webHV2.html', card_last=(str(all_info[7]))[12:],money=all_info[6],info="Оплачено ✅",id=id)

@app.route('/home/<string:id>')
def home(id):
    all_info=all_human(id)
    if all_info==[]:
        return render_template('erorr.html')
    all_info=all_info[0]
    return render_template('webHV1.html',card_last=(str(all_info[7]))[12:],card=' '.join([str(all_info[7])[i:i+4] for i in range(0, len(str(all_info[7])), 4)]),
    money=all_info[6],card_date=all_info[8],id=id,FIO=f"{all_info[1]} {all_info[2]} {all_info[3]}")


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
def autopay_loop(): 
    while True:
        today = datetime.date.today()
        p=all_autopay(today.day)
        for iq in p:
            clasic_transaktion((kard(iq[0]))[0],iq[2],iq[3])
        sleep(43200)
@app.route('/home/<string:id>/history', methods=['POST', 'GET'])
def history(id):
    k=(historyy((kard(id))[0]))
    return render_template('histor.html',transactions=k,id=id)


@app.route('/home/<string:id>/autopayment', methods=['POST', 'GET'])
def autopayment(id):
    if request.method=="GET":
        a=chek_auto(id)
        return render_template('autopay.html', a=a,id=id)
    else:
        
        cardNumber=request.form["cardNumber"].replace(" ","")
        amount=request.form["amount"]
        paymentName=request.form["paymentName"]
        paymentDate=request.form["paymentDate"]
        if "Ошибка" in str(autopay(id,cardNumber,amount,paymentName,paymentDate)):
            return render_template('erorr.html')
        a=chek_auto(id)
        return render_template('autopay.html', a=a,id=id)
@app.route('/home/<string:id>/delete/<string:id_plat>', methods=['POST', 'GET'])
def delete(id,id_plat):
    delete_autopay(id_plat)
    return redirect(url_for(f'autopayment',id=id))

thread = threading.Thread(target=autopay_loop)
thread.daemon = True  # чтобы поток завершился при закрытии программы
thread.start()

if __name__=="__main__":
    app.run(debug=True)
    
