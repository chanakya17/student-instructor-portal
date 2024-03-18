import sqlite3

class User:
    def __init__(self, db_file='user.db'):
        self.conn = sqlite3.connect(db_file)
        

    def get_details(self, detail, username):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f'''
                SELECT {detail} FROM users
                WHERE username = ?
            ''', (username,))
            result = cursor.fetchone()
            return result[0] if result else None

    def close(self):
        self.conn.close()

# Example usage:
if __name__ == "__main__":
    user=User()
    x=user.get_details('first_name','mechi1c')
    print(x)
  
