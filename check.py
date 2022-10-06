


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

def complex_two_no_zero(get_complex):
    
    try:
        if get_complex != 0:
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


def get_symbol(user_choice, number):
    '''
    Проверка символа для действий
    '''
    if user_choice in '+-/*':
        if user_choice == '/':
            number != '0'
            return True
        else:
            return False
    else:
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
