import psycopg2, psycopg2.extensions, psycopg2.extras, click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            current_app.config['DATABASE'],
            cursor_factory=psycopg2.extras.RealDictCursor
            # database = "expenny",
            # user="postgres",
            # password="root",
            # host="localhost",
            # port="5432"
        )

        psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
        psycopg2.extensions.register_adapter(list, psycopg2.extras.Json)
    
    return g.db

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        sql = f.read().decode('utf8')
        cur = db.cursor()
        cur.execute(sql)
        cur.close()
        db.commit()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)