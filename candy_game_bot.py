import logging
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import random
# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
CANDY_COUNT, CANDY_PER_MOVE , TOSS, PLAYER_TURN, COMPUTER_TURN = range(5)

# функция обратного вызова точки входа в разговор
def start(update, _):
    update.message.reply_text(
        'Это игра с конфетами. Цель игры, чтобы ваш противник взял последнюю конфету.\n'
        'Команда /cancel, чтобы прекратить разговор.\n'
        'Введите кол-во конфет в куче: ')    
    return CANDY_COUNT


def candy_count(update, context):
    user = update.message.from_user
    logger.info("Кол-во конфет: %s: %s", user.first_name, update.message.text)
    candy_count = update.message.text
    if check_input_int(candy_count):
        context.user_data['candy_count'] = candy_count
        update.message.reply_text(
            f'В куче {candy_count} конфет\n'
            'Введите кол-во конфет, которое можно забрать за ход.\n'
            '(Оно должно быть меньше общего колличества конфет в куче): ')  
        return CANDY_PER_MOVE
    else:
         update.message.reply_text(
            f'Вы ввели не число\n')
    

def check_input_int(candy_count):
    try:
        candy_count = int(candy_count)
        return True
    except ValueError:
        return False

def get_candy_per_move(candy_count, candy_per_move):
    try:
        candy_per_move = int(candy_per_move)
        if candy_per_move > 0 and candy_per_move < int(candy_count):
            return True
    except ValueError:
        return False

def candy_per_move(update, context):
    user = update.message.from_user
    logger.info("Кол-во конфет за ход %s: %s", user.first_name, update.message.text)
    candy_count = context.user_data.get('candy_count')
    candy_per_move = update.message.text
    if get_candy_per_move(candy_count, candy_per_move):
        context.user_data['candy_per_move'] = candy_per_move
        update.message.reply_text(
            f'Введите 1 или 2, чтоюбы монетка определила выбор хода')
        return TOSS
    else:
         update.message.reply_text(
            f'Вы ввели не правильное значение\n')

def check_toss(toss):
    try:
        toss = int(toss)
        if toss == 1 or toss == 2:
            return True
        else:
            return False
    except ValueError:
        return False

def get_toss(toss):
    r = random.randint(1,2)
    if int(toss) == r:
        return True
    else:
        return False


def toss(update, context):
    user = update.message.from_user
    logger.info("Выбор очередности %s: %s", user.first_name, update.message.text)
    toss = update.message.text
    candy_per_move = context.user_data.get('candy_per_move')
    count = 1
    context.user_data['count'] = count
    player1_move = 0
    context.user_data['player1_move'] = player1_move
    if check_toss(toss):    
        if get_toss(toss):
            update.message.reply_text(
                f'Ваш ход. За ход можно брать от 1 до {candy_per_move} конфет')
            return PLAYER_TURN
        else:
            return computer_turn(update, context)
    else:
        update.message.reply_text(
            f'Вы ввели не правильное значение\n')


def check_player_move(player1_move, candy_per_move):
    try:
        player1_move = int(player1_move)
        if player1_move > 0 and player1_move <= candy_per_move:
            return True
    except ValueError:
        return False

def player_turn(update, context):
    user = update.message.from_user
    logger.info(
        "Ход игрока %s: %f / %f", user.first_name, update.message.text)
    candy_per_move = int(context.user_data.get('candy_per_move'))
    candy_count = int(context.user_data.get('candy_count'))
    player1_move = update.message.text
    count = context.user_data.get('count')
    if check_player_move(player1_move, candy_per_move):
        player1_move = int(player1_move)
        candy_count -= player1_move
        if candy_count == 1:
            update.message.reply_text(
                        f'Игрок {user.first_name} выграл')
            return ConversationHandler.END
        context.user_data['candy_count'] = candy_count
        update.message.reply_text(
                f'Вы ввели {player1_move} конфет. В куче осталось {candy_count}: '
                'Внимание ходит бот...')
        context.user_data['player1_move'] = player1_move
        count+=1
        context.user_data['count'] = count       
        return computer_turn(update, context)
    else:
        update.message.reply_text(
                        f'Вы ввели не то')    
    
        
def computer_turn(update, context):
    player1_move = int(context.user_data.get('player1_move'))
    candy_count = int(context.user_data.get('candy_count'))
    candy_per_move = int(context.user_data.get('candy_per_move'))
    count = int(context.user_data.get('count'))
    
    player2_move = bot(candy_per_move, candy_count, player1_move, count)
    candy_count -= player2_move
    count+=1
    context.user_data['count'] = count
    if candy_count == 1:
        update.message.reply_text(
                        f'Бот проиграл')
        return ConversationHandler.END 
    context.user_data['candy_count'] = candy_count
    update.message.reply_text(
            f'Бот походил на {player2_move} конфет. В куче осталось {candy_count}: '
            f'Ваш ход. Введите число в диапазоне от 1 до {candy_per_move}: ')    
    return PLAYER_TURN
        

def bot(candy_per_move, candy_count, player1_move, count):
    
    if count == 1:
        if candy_count % (candy_per_move +1) == 0 or candy_count % (candy_per_move +1) == 1:
            bot_move = 1
        else:
            bot_move = (candy_count % (candy_per_move +1)) - 1
    else:
        if candy_count <= candy_per_move*2 + 2 and candy_count > candy_per_move +1:
            bot_move = (candy_count - candy_per_move) - 2
        elif candy_count <= candy_per_move +1:
            bot_move = candy_count - 1
        else:
            bot_move = (candy_per_move +1)- player1_move
    return bot_move

    
    
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.', 
    )
    return ConversationHandler.END


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Определяем обработчик разговоров `ConversationHandler` 
    # с состояниями GENDER, PHOTO, LOCATION и BIO
    game_conversation_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            CANDY_COUNT:[
                MessageHandler(Filters.text, candy_count),
                CommandHandler('cancel', cancel)
                ] ,
            CANDY_PER_MOVE: [
                MessageHandler(Filters.text, candy_per_move),
                CommandHandler('cancel', cancel)
                ],
            TOSS: [
                MessageHandler(Filters.text, toss),
                CommandHandler('cancel', cancel)
                ],
            PLAYER_TURN:[
                MessageHandler(Filters.text, player_turn),
                CommandHandler('cancel', cancel)
                ],
            COMPUTER_TURN: [MessageHandler(Filters.text, computer_turn)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(game_conversation_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()