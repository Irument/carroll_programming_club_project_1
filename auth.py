import sqlite3
import bcrypt

class AccountNotFound(Exception):
    pass

class Auth:
    def __init__(self):
        self.db = 'main.db'
        db, cur = self.connect_to_db()
        cur.execute('CREATE TABLE IF NOT EXISTS accounts(username TEXT, password TEXT, admin BOOL)')
        self.close_db(db, cur)
    
    def connect_to_db(self):
        """
        Returns db and cursor objects
        """
        db = sqlite3.connect(self.db)
        cur = db.cursor()
        return db, cur
    def close_db(self, db, cur):
        """
        Closes db and cursor objects.
        """

        cur.close()
        db.commit()
        db.close()

    def hashpasswd(self, password):
        """
        Hashes the given password
        """

        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    def check_if_exists(self, db, cur, username):
        """
        Checks if an account already exists
        """

        cur.execute('SELECT * FROM accounts WHERE username=?')
        return not len(cur.fetchone()) == 0

    def check_admin(self, username):
        """
        Checks if an account has administrator privileges
        """

        db, cur = self.connect_to_db()
        admin = False
        if self.check_if_exists(db, cur, username):
            cur.execute('SELECT admin FROM accounts WHERE username=?', (username,))
            if cur.fetchone()[0][0]:
                admin = True
        else:
            self.close_db(db, cur)
            raise AccountNotFound('Tried to find out if a non-existant account has admin')
        self.close_db(db, cur)
        return admin

    def create_account(self, username, password):
        """
        Creates an account
        """

        db, cur = self.connect_to_db()
        if self.check_if_exists(db, cur, username):
            return False
        cur.execute('INSERT INTO accounts VALUES(?, ?)', (username, self.hashpasswd(password)))
        self.close_db(db, cur)
        return True
    def delete_account(self, username):
        """
        Deletes an account
        """

        db, cur = self.connect_to_db()
        if not self.check_if_exists(db, cur, username):
            return False
        cur.execute('DELETE FROM accounts WHERE username=?', (username,))
        self.close_db(db, cur)
        return True

    def check(self, username, password):
        """
        Checks if login is correct
        """

        db, cur = self.connect_to_db()

        if not self.check_if_exists(db, cur, username):
            self.close_db(db, cur)
            return False
        
        cur.execute('SELECT username, password FROM accounts WHERE username=?', (username,))
        db_user, hashed = cur.fetchone()[0]

        correct = False
        if bcrypt.checkpw(password.encode(), hashed.encode()):
            correct = True
        
        self.close_db(db, cur)
        return correct
    