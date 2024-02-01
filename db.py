import sqlite3

from config import DB_PATH


def db_init():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS answer
                  (question TEXT, answer TEXT, users_answer TEXT, date_time TEXT)
                    ''')
    connection.commit()
    connection.close()


def db_append(question, answer, users_answer, date_time):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO answer (question, answer, users_answer, date_time) VALUES (?, ?, ?, ?)", (question, answer, users_answer, date_time))
    connection.commit()
    connection.close()


def db_load() -> list[tuple]:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM answer")
    events = cursor.fetchall()
    for a in events:
        print(a)
    connection.close()
