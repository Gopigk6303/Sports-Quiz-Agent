from src.generator import compile_quiz_data
import traceback

try:
    quiz, ctx = compile_quiz_data('Cricket', 'Easy')
    print('QUIZ_OK')
    print(quiz)
except Exception as e:
    print('EXCEPTION')
    traceback.print_exc()
