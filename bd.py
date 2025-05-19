import psycopg2
from config import db_name,host,password,user

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
        print(f"Ошибка: {e}")
        return None
    finally:
        if connection:
            connection.close()
            print("Соединение закрыто")

def chek_human(user,password):
    h=f"SELECT * FROM users WHERE us='{user}' AND password='{password}'"
    return sql(h)

def chek_email(email):
    h=f"SELECT * FROM users WHERE email='{email}'"
    return sql(h)

def chek_name(name):
    h=f"SELECT * FROM users WHERE us='{name}'"
    return sql(h)

def new_human(user,pas,email):
    h=f"INSERT INTO users (us,password,email) VALUES ('{user}','{pas}','{email}')"
    return sql(h)

def new():
    h="DROP TABLE users;"
    sql(h)
    h="CREATE TABLE users (us VARCHAR(50)  NOT NULL,password VARCHAR(255) NOT NULL,email VARCHAR(255));"
    return sql(h)