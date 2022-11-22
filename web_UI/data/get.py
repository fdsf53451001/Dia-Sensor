import sqlite3

SQLITE_DB_PATH = 'backend/foothow.db'
SQLITE_DB_SCHEMA = 'backend/create_db.sql'

db = sqlite3.connect(SQLITE_DB_PATH)

def get_histories_by_account(account, /, db = db, n = None):

    data = db.cursor()

    data.execute('SELECT id FROM members WHERE account = ?', (account, ))
    number = data.fetchone()[0]

    data.execute('SELECT * FROM histories WHERE memberid = ?', (number, ))
    histories = list(data.fetchall())
    
    n = n if n else len(histories)
    n = len(histories) if len(histories) < n else n

    #histories.reverse()
    return histories[0:n]

def get_temp_record_by_id(id, /, db = db):
    
    data = db.cursor()

    data.execute('SELECT * FROM temp WHERE id = ?', (id, ))
    return list(data.fetchone())[1:]

def get_test_record_by_id(id, /, db = db):
    
    data = db.cursor()

    data.execute('SELECT * FROM test WHERE id = ?', (id, ))
    return list(data.fetchone())[1:]


if __name__ == '__main__':
    print(get_test_record_by_id(1, db))
