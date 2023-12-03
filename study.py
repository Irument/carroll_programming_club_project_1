import sqlite3
import copy
import string

class Study:
    """
    Uses an SQL database to store multiple quizes.
    Each quiz has an ID, and quizes are seperate tables
    with the ID. IDs given by the user should be checked
    for any special characters or spaces. It is vulnerable
    to SQL injection otherwise.
    """

    def __init__(self, db):
        self.db = db
        db, cur = self.get_db()
        cur.execute('CREATE TABLE IF NOT EXISTS quizes(quiz_id TEXT, quiz_name TEXT)')
        self.close_db(db, cur)

        self.questions = { # Key is the question, value is the answer. This is not used anymore, but it is kept here for examples in the future
            "2x+5 = 19 - Find x": "7",
            "y=2x+3 - What is the slope?": "2",
            "y=2x+3 - What is the y-intercept?": "3",
            "Find the slope with these 2 points\n(2, 1) (5, 7)": "2",
            "3x+12=2x+18 - Find x": "6"
        }
    
    def check_safe(self, text):
        """
        Checks for special characters/spaces
        to prevent SQL injection
        """

        allowed_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

        safe = True
        for character in text:
            if not character in allowed_characters:
                safe = False
                break
        
        if len(text) > 10:
            safe = False

        return safe

    """
    Functions for simplifying connecting to the DB.
    """

    def get_db(self):
        db = sqlite3.connect(self.db)
        cur = db.cursor()
        return db, cur
    def close_db(self, db, cur):
        cur.close()
        db.commit()
        db.close()

    def create_quiz(self, quiz_name, quiz_id, questions):
        """
        Creates a new table with the questions.
        The questions parameter takes the same
        format that the parse_questions function
        uses.
        """

        if not self.check_safe(quiz_id):
            return False
        
        db, cur = self.get_db()
        cur.execute('CREATE TABLE IF NOT EXISTS quiz_{}(question TEXT, answer TEXT, choice1 TEXT, choice2 TEXT, choice3 TEXT)'.format(quiz_id))
        cur.execute('INSERT INTO quizes VALUES(?, ?)', (quiz_id, quiz_name))
        for question in questions:
            if question['choices'] == []:
                choices = [None, None, None]
            else:
                choices = question['choices']
            cur.execute('INSERT INTO quiz_{} VALUES(?, ?, ?, ?, ?)'.format(quiz_id), [question['question'], question['answer']] + choices)
        self.close_db(db, cur)

    def delete_quiz(self, quiz_id):
        """
        Removes the quiz table and its entry
        in the quizes table.
        """

        if not self.check_safe(quiz_id):
            return False

        db, cur = self.get_db()
        cur.execute('DROP TABLE quiz_{}'.format(quiz_id))
        cur.execute('DELETE FROM quizes WHERE quiz_id=?', (quiz_id,))
        self.close_db(db, cur)

    def parse_questions(self, data):
        """
        Parses the entries in the DB into something
        more readable
        """

        questions = []
        for entry in data:
            if not entry[2] == None:
                choices = list(copy.copy(entry))
                choices.pop(0)
                choices.pop(0)
            else:
                choices = []
            entry_data = {
                'question': entry[0],
                'answer': entry[1],
                'choices': copy.copy(choices)
            }
            questions.append(entry_data)
        return questions

    def quiz_exists(self, quiz_id):
        """
        Checks if a quiz exists
        """

        if not self.check_safe(quiz_id):
            return False

        quizes = self.get_quizes()
        return quiz_id in quizes

    def get_quizes(self):
        """
        Gets all quizes from the quizes
        table
        """

        db, cur = self.get_db()
        cur.execute('SELECT * FROM quizes')
        data = cur.fetchall()
        quizes = []
        for entry in data:
            quizes.append(entry[0])
        self.close_db(db, cur)
        return quizes

    def get_quiz(self, quiz_id):
        """
        Gets data from the quiz table and
        parses it with parse_questions function
        """

        if not self.check_safe(quiz_id):
            return False

        db, cur = self.get_db()
        cur.execute('SELECT * FROM quiz_{}'.format(quiz_id))
        data = cur.fetchall()
        cur.execute('SELECT * FROM quizes WHERE quiz_id=?', (quiz_id,))
        quiz_name = cur.fetchall()[0][1]
        self.close_db(db, cur)
        questions = self.parse_questions(data)
        return [questions, quiz_name]
