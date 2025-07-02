import sqlite3


def create_tables():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('''DROP TABLE IF EXISTS Branch''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Branch (
    id INTEGER PRIMARY KEY,
    internal_id INTEGER,
    name TEXT NOT NULL,
    visible_name TEXT NOT NULL,
    address TEXT NOT NULL,
    visible_address TEXT NOT NULL,
    opendate TEXT NOT NULL,
    parent TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()


def add_branch(branch):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute(
        'INSERT INTO Branch (internal_id, name, visible_name, address, visible_address, opendate, parent) VALUES (?,?,?,?,?,?,?)',
        (branch["internal_id"], branch["name"], branch["visible_name"], branch["address"], branch["visible_address"],
         branch["opendate"],
         branch["parent"]))

    connection.commit()
    connection.close()


def get_branches():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    result = cursor.execute('SELECT * FROM BRANCH').fetchall()
    connection.close()
    return result


def get_branch_by_pattern(pattern: str):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    pattern = pattern.lower()
    # result = cursor.execute('SELECT * FROM BRANCH WHERE name LIKE ?', ('Евпа',)).fetchall()
    sql = 'SELECT * FROM BRANCH WHERE name LIKE ? OR address LIKE ? '

    result = cursor.execute(sql, ('%' + pattern + '%', '%' + pattern + '%')).fetchall()


    return result
