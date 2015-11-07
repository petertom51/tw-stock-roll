import sqlite3

db_path = "./data.db"

def _init_database():
    """ init the database and returns connection and cursor. The caller
    should close the connection """
    open(db_path, 'a').close()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS rolls ('
            'ID INTEGER PRIMARY KEY, '
            'ROLL_DATE     DATE      NOT NULL, '
            'STOCK_NAME    TEXT      NOT NULL, '
            'STOCK_ID      INTEGER   NOT NULL, '
            'START_DATE    DATE      NOT NULL, '
            'END_DATE      DATE      NOT NULL, '
            'SHARE_NUM     INTEGER   NOT NULL, '
            'SELL_PRICE    REAL      NOT NULL, '
            'CUR_PRICE     REAL, '
            'PERCENT_PRICE REAL )')
    conn.commit()
    return conn, cursor
    
def getall():
    conn, cursor = _init_database()
    cursor.execute('SELECT * FROM rolls')
    rolls = cursor.fetchall()
    conn.close()
    return rolls
    
def delete(rollid):
    conn, cursor = _init_database()
    print('DELETE FROM rolls WHERE STOCK_ID = {}'.format(rollid))
    cursor.execute('DELETE FROM rolls WHERE ID = %s' %  rollid)
    conn.commit()
    conn.close()

def insert(roll):
    conn, cursor = _init_database()
    cursor.execute("INSERT INTO rolls "
                   "(ID, ROLL_DATE, STOCK_NAME, STOCK_ID, START_DATE, END_DATE, SHARE_NUM, SELL_PRICE) "
                   "VALUES(?,?,?,?,?,?,?,?)",
                   (roll['ID'], roll['ROLL_DATE'], roll['STOCK_NAME'], roll['STOCK_ID'], roll['START_DATE'], roll['END_DATE'], roll['SHARE_NUM'], roll['SELL_PRICE']))
    conn.commit()
    conn.close()

def erase():
    conn, cursor = _init_database()
    cursor.execute('DELETE FROM rolls')
    conn.commit()
    conn.close()

