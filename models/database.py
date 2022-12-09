from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# Global Variables
SQLITE                  = 'sqlite'
# MYSQL                   = 'mysql'
# POSTGRESQL              = 'postgresql'
# MICROSOFT_SQL_SERVER    = 'mssqlserver'

# Table Names
USERS           = 'users'
POSTS           = 'posts'
VIEW            = 'view'


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        # MYSQL: 'mysql://scott:tiger@localhost/{DB}',
        # POSTGRESQL: 'postgresql://scott:tiger@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://scott:tiger@hostname:port/{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname='users.db'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(engine_url)
            print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        users = Table(USERS, metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('user_id', Integer),
                      Column('balance', Integer),
                      Column('tasks', Integer),
                      Column('skips', Integer),
                      )
        
        posts = Table(POSTS, metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('user_id', Integer),
                      Column('link', String),
                      Column('count', Integer),
                      Column('comms', Integer),
                      )
        
        view = Table(VIEW, metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('user_id', Integer),
                      Column('post_id', Integer),
                      )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return

        print (query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)


    def get_all(self, db, columns='*'):
        query = "SELECT {0} FROM '{1}';".format(columns, db)
        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                res = result.all()
                result.close()
                return res

        print("\n")

    # Examples

    def get_by(self, db, columns='*', vals=''):
        query = "SELECT {0} FROM '{1}' WHERE {2};".format(columns, db, vals)
        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                res = result.all()
                result.close()
                return res

    def delete(self, db, vals):
        # Delete Data by Id
        query = "DELETE FROM {0} WHERE {1}".format(db, vals)
        self.execute_query(query)

        # Delete All Data
        '''
        query = "DELETE FROM {}".format(USERS)
        self.execute_query(query)
        '''

    def insert(self, db, vals, columns):
        # Insert Data
        query = "INSERT INTO {0} ({1}) " \
                "VALUES ({2});".format(db, columns, vals)
        self.execute_query(query)

    def update(self, db, set, vals):
        # Update Data
        query = "UPDATE {0} set {1} WHERE {2}"\
            .format(db, set, vals)
        self.execute_query(query)
