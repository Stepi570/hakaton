import psycopg2
from config import db_name,host,password,user
import string
from datetime import datetime
import random
def sql(text):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            sslrootcert="/etc/ssl/certs/ca-certificates.crt"
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(text)
            
            if cursor.description:
                result = cursor.fetchall()
                # Если в результате один столбец — преобразуем в плоский список
                if len(cursor.description) == 1:
                    return [row[0] for row in result]  # Пример: [0, 1, 2]
                else:
                    return result  # Пример: [(0, "Ivan"), (1, "Anna")]
            else:
                return cursor.rowcount  # Для INSERT/UPDATE/DELETE
            
    except Exception as e:
        return (f"Ошибка: {e}")
    finally:
        if connection:
            connection.close()
            print("Соединение закрыто")

def chek_human(user,password):
    h=f"SELECT * FROM users WHERE username='{user}' AND password='{password}'"
    return sql(h)

def chek_pasport(pasport):
    h=f"SELECT * FROM users WHERE pasport='{pasport}'"
    if sql(h) == []:
        return False
    else:
        return True

def chek_name(name):
    h=f"SELECT * FROM users WHERE username='{name}'"
    if sql(h) == []:
        return True
    else:
        return False

def new_human(username ,password ,name ,surname ,patronymic ,pasport ,date):
    part1 = f"{random.randint(10, 99):02d}"
    part2 = f"{random.randint(10, 99):02d}"
    h=f"INSERT INTO users (username ,password ,name ,surname ,patronymic ,pasport ,date , balance ,card_number,expiration_date ,CVV) VALUES ('{username}' ,'{password}' ,'{name}' ,'{surname}' ,'{patronymic}' ,'{pasport}' ,'{date}' , 0,{random.randint(10**15, 10**16 - 1)},'{f"{part1}/{part2}"}',{random.randint(100, 999):02d})"
    return sql(h)

def new():
    h="CREATE TABLE users (username VARCHAR(250) NOT NULL, password VARCHAR(255) NOT NULL, name VARCHAR(255), surname VARCHAR(255), patronymic VARCHAR(255), pasport VARCHAR(20), date VARCHAR(30), balance BIGINT, card_number BIGINT, expiration_date VARCHAR(30), CVV SMALLINT); CREATE TABLE transaction (chek VARCHAR(255), sender BIGINT, recipient BIGINT, minutes TEXT DEFAULT TO_CHAR(NOW(), 'HH24:MI'), date DATE DEFAULT CURRENT_DATE, sum BIGINT);CREATE TABLE autopay (sendler BIGINT,recipient BIGINT,summ BIGINT,day SMALLINT);"
    return sql(h)

def clasic_transaktion(card_sender,card_recipient,summ):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(50))
    minutes=(datetime.now()).strftime("%H:%M")
    date=(datetime.now()).strftime("%d.%m.%Y")
    h = f"""
    DO $$
    DECLARE
        rows_affected1 INTEGER;
        rows_affected2 INTEGER;
    BEGIN     
        -- Проверяем достаточность средств
        PERFORM 1 FROM users WHERE card_number = {card_sender} AND balance >= 500;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Недостаточно средств на карте';
        END IF;
        
        -- Выполняем транзакцию
        UPDATE users SET balance = balance + {summ} WHERE card_number = {card_recipient};
        GET DIAGNOSTICS rows_affected1 = ROW_COUNT;
        
        UPDATE users SET balance = balance - {summ} WHERE card_number = {card_sender};
        GET DIAGNOSTICS rows_affected2 = ROW_COUNT;
        
        IF rows_affected1 = 0 OR rows_affected2 = 0 THEN
            RAISE EXCEPTION 'Ошибка при обновлении баланса';
        END IF;
        INSERT INTO transaction (chek ,sender, recipient,sum ) VALUES ('{random_string}',{card_sender},{card_recipient},{summ});
        RAISE NOTICE 'Транзакция успешно выполнена';
    EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION '%', SQLERRM;
    END;
    $$ LANGUAGE plpgsql;
    """
    return sql(h)

def statistik(date,card):
    h=f"SELECT * FROM transaction WHERE date='{date}' AND (sender={card} OR recipient={card}) "
    return sql(h)

def autopay(card_sender,card_recipient,summ,day):
    h=f"INSERT INTO autopay (sendler,recipient ,summ,day) VALUES ({card_sender},{card_recipient},{summ},{day})"
    return sql(h)

def delete_autopay(card_sender,card_recipient,summ,day):
    h=f"DELETE FROM autopay WHERE sendler={card_sender} AND recipient={card_recipient},summ={summ} ,day={day}"
    return sql(h)

def chek_card(card):
    h=f"SELECT * FROM users WHERE card_number={card}"
    if sql(h) == []:
        return True
    else:
        return False