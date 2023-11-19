class Study:
    """
    Gives questions and answers to client though JSON
    response. This is a placeholder.
    """

    def __init__(self):
        self.questions = { # Key is the question, value is the answer
            "2x+5 = 19 - Find x": "7",
            "y=2x+3 - What is the slope?": "2",
            "y=2x+3 - What is the y-intercept?": "3",
            "Find the slope with these 2 points\n(2, 1) (5, 7)": "2",
            "3x+12=2x+18 - Find x": "6"
        }
    
    def get_quiz(self):
        return self.questions
