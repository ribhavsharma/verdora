import mysql.connector

class MysqlManager:
    
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="verdora",
            port="3310"
        )

        self.cursor = self.conn.cursor()

    def insert_data(self, table, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        values = tuple(data.values())
        self.cursor.execute(query, values)
        self.conn.commit()

    def select_data(self, table, columns="*", where_clause=None):
        query = f"SELECT {columns} FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_data(self, table, where_clause):
        query = f"DELETE FROM {table} WHERE {where_clause}"
        self.cursor.execute(query)
        self.conn.commit()

