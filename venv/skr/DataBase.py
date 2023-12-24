import pymysql


class DataBase:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def open_connection(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def get_data(self, from_get, value=(), transaction=False):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(from_get, value)
                results = cursor.fetchall()
                return results
            except Exception as e:
                print(f"Error during data retrieval: {e}")
                raise
            finally:
                if transaction is not True:
                    self.close_connection()

    def set_data(self, insert_query, types_data="None", value=None):
        with self.connection.cursor() as cursor:
            try:
                if types_data == "list":
                    cursor.executemany(insert_query, value)
                    self.connection.commit()
                elif value is None:
                    cursor.execute(insert_query)
                    self.connection.commit()
                else:
                    cursor.execute(insert_query, value)
                    self.connection.commit()
            except Exception as e:
                print(f"Error during data insertion: {e}")
                self.connection.rollback()
                raise
            finally:
                self.connection.close()
