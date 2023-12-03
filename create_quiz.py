import study as study_mod
import uuid

study = study_mod.Study('main.db')

quiz = []
quiz_name = input('Quiz Name: ')
question_number = 1

questions = []

while True:
    print('-- Question {} --'.format(question_number))
    question = input('Question: ')
    answer = input('Answer: ')
    try:
        int(answer)
    except: # Text-based
        choices = []
        for x in range(1, 4):
            choices.append(input('Choice {}: '.format(x)))
    else: # Number-based
        choices = []
    questions.append({'question': question, 'answer': answer, 'choices': choices})
    another_question = input('Would you like another question? (y, n): ')
    if another_question == 'n':
        break

quiz_id = str(uuid.uuid4())[:8]

study.create_quiz(quiz_name, quiz_id, questions)

print('-- Quiz created --')
print('Quiz ID: {}'.format(quiz_id))
print('Quiz Name: {}'.format(quiz_name))
