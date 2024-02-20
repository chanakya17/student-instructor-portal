import sqlite3

class User:
    def __init__(self, db_file='user.db'):
        self.conn = sqlite3.connect(db_file)
        

    def _get_detail(self, detail, username):
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
    # Create an instance of the User class
    mechi1c = User()
    x=mechi1c._get_detail("first_name","mechi1c")
    print(x)



    
    # Close the database connection
    mechi1c.close()
