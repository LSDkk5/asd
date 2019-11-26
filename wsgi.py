from web import app
import sqlite3, os
import sys
sys.path.append('..')

@app.cli.command('create-db')
def create_database():
    from web import db
    try:
        db.drop_all()
        db.create_all()
        print('[DATABASE] Baza danych została pomyślnie stworzona!')
    except:
        print('[DATABASE] Nie udało się stworzyć bazy danych!')

@app.cli.command('dump-sql3')
def dump_database():
    con = sqlite3.connect(f'web/{app.config["SQLALCHEMY_DATABASE_URI"].split("///")[1]}')
    with open('dump.sql', 'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
