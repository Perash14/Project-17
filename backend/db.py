import psycopg2

class ChatDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="Proj17",
            user="postgres",
            password="12345678",
            host="localhost"
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def insert_user(self,username,room_number):
        try:
            self.cur.execute("INSERT INTO users (username,room_number) VALUES(%s,%s) RETURNING id",(username,room_number))
            user_id = self.cur.fetchone()[0]
            return user_id
        except ValueError as e:
            raise e

    def get_messages(self,room_number):
        self.cur.execute("SELECT users.username, messages.text FROM messages INNER JOIN users ON users.id=messages.user_id WHERE users.room_number=%s",(room_number,))
        return self.cur.fetchall()
    
    def add_message(self, message,userID):
        try:
            self.cur.execute("INSERT INTO messages (text,user_id) VALUES(%s,%s)",(message,userID,))
        except ValueError as e:
            print(e)