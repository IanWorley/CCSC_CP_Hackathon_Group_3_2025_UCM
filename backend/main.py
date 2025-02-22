

import sqlite3
import requests

def main():
    conn = sqlite3.connect('./backend/database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS machines (type TEXT, id TEXT, state TEXT, state_time INTEGER)''')
    c.execute('''insert into users values ('admin', 'admin')''')

    response = requests.get('http://127.0.0.1:5000/machines')
    machines = response.json()
    print(machines)

    # Insert machine data into the database
    for machine in machines:
        c.execute('''INSERT INTO machines VALUES (?, ?, ?, ?)''', 
                  (machine['type'], machine['id'], machine['state'], machine['state_time']))


    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()