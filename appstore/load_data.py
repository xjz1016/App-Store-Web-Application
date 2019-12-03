import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

fname = 'Apple-app-store.csv'
with open(fname) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    t = 0
    for line in readCSV:
        if t==0:
            t += 1
            continue
        # if t>=2:
        #     break
        cur.execute('SELECT * FROM app_developer WHERE developer_name = ? ', (line[5],))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO app_developer (developer_name, developer_account_id)
                    VALUES (?,?)''', (line[5], 1000+t))
        else:
            print('%s already exists' %line[5])
        cur.execute('SELECT * FROM app_developer WHERE developer_name = ? ', (line[5],))
        row = cur.fetchone()
        developer_id = row[0]

        cur.execute('SELECT * FROM app_category WHERE category_name = ? ', (line[12],))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO app_category (category_name)
                    VALUES (?)''', (line[12],))
        else:
            print('%s already exists' %line[12])
        cur.execute('SELECT * FROM app_category WHERE category_name = ? ', (line[12],))
        row = cur.fetchone()
        category_id = row[0]

        languages = line[10].split(',')
        lan_id = []
        for language in languages:
            cur.execute('SELECT * FROM app_language WHERE language_name = ? ', (language,))
            row = cur.fetchone()
            if row is None:
                cur.execute('''INSERT INTO app_language (language_name)
                        VALUES (?)''', (language,))
            else:
                print('%s already exists' %language)
            cur.execute('SELECT * FROM app_language WHERE language_name = ? ', (language,))
            row = cur.fetchone()
            lan_id.append(row[0])

        cur.execute('SELECT * FROM app_app WHERE app_name = ? ', (line[1],))
        row = cur.fetchone()
        version = line[11].split()[-1]
        if row is None:
            cur.execute('INSERT INTO app_app(app_name, developer_id, price, size, version, category_id, rating, date_created, date_updated) VALUES (?,?,?,?,?,?,0,?,?)', (line[1], developer_id, 0, line[9], version, category_id,'2019-12-03 01:13:55.130258','2019-12-03 01:13:55.130258'))
            cur.execute('SELECT * FROM app_app WHERE app_name = ? ', (line[1],))
            row = cur.fetchone()
            for id in lan_id:
                cur.execute('''INSERT INTO app_app_to_language (app_id, language_id)
                        VALUES (?,?)''', (row[0], id))
        else:
            print('%s already exists' %line[1])
        conn.commit()
        t += 1
        
# for line in fh:
#     if not line.startswith('From: '): continue
#     pieces = line.split()
#     org = pieces[1].split('@')[1]
#     cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
#     row = cur.fetchone()
#     if row is None:
#         cur.execute('''INSERT INTO Counts (org, count)
#                 VALUES (?, 1)''', (org,))
#     else:
#         cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
#                     (org,))
#     conn.commit()

# # https://www.sqlite.org/lang_select.html
# sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

# for row in cur.execute(sqlstr):
#     print(str(row[0]), row[1])

cur.close()
