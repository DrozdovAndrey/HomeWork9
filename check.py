import logger


def get_number_int(input_string: str) -> int:
    '''
    Проверка целого числа
    '''
    try:
        if len(input_string) == 2:
            input_string[0] = int(input_string[0])
            input_string[1] = int(input_string[1])
            return True
    except ValueError:
        return False

def get_number_int_0(input_string: str) -> int:
    '''
    Проверка целого числа
    '''
    try:
        if len(input_string) == 2:
            input_string[0] = int(input_string[0])
            input_string[1] = int(input_string[1])
            if complex(input_string[0], input_string[1]):
                return True
    except ValueError:
        return False

def get_number_float(get_rational):
    '''
    Проверка числа с плавающей точкой
    '''
    try:
        get_rational = float(get_rational)
        return True
    except ValueError:
        return False

def rational_two_no_zero(get_rational):
    '''
    Проверка числа с плавающей точкой
    '''
    try:
        if int(get_rational) != 0:
            return True
    except ValueError:
        return False


def get_symbol(user_choice):
    '''
    Проверка символа для действий
    '''
    
    try:
        if user_choice not in '+-/*':
            return True
    except ValueError:
        return False


def get_selection(user_choice) -> int:
    '''
    Проверка числа для выбора результата
    '''
    try:
        char = user_choice
        if char in '12':
            return True   
    except ValueError:
        return False


def get_zero_division_error(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    if num2 == 0.0:
        return False
    else:
        return True


def complex_get_zero_division_error(a_re, a_im, b_re, b_im):
    x = 0
    y = 0
    x = complex(a_re, a_im)
    y = complex(b_re, b_im)
    if y == 0:
        return False
    else:
        return True


'''
Нумератор для удобства отображения чисел в контроллере
'''


def num_to_word(num: str) -> str:

    if num == 1:
        return 'первого'
    elif num == 2:
        return 'второго'
    else:
        print('Метод может принимать только 1 или 2, проверьте что приходит в метод num_to_word ')
        logger.log(
            num, 'Метод может принимать только 1 или 2, проверьте что приходит в метод num_to_word ')
        exit()


def zero_division_check(def_part):
    try:
        def_part
    except ZeroDivisionError:
        if ZeroDivisionError:
            print('') 