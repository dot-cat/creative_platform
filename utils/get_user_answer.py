def get_user_answer():
    """
    Получить ответ от пользователя (y\n) на некотоырй вопрос
    :return: True - ответ y, False - ответ n
    """
    while True:
        user_input = input('Please, answer y (yes) or n (no)')

        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print('Invalid answer')
            continue
