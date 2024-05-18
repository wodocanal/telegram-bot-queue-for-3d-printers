with open('token.txt') as file:
    TOKEN = file.read()


class Role:
    def __init__(self):
        self.user = 0
        self.admin = 1
        self.ban = 2

class Status:
    def __init__(self):
        self.not_begin = 0
        self.decline = 1
        self.in_progress = 2
        self.finished = 3
        

role = Role()
status = Status()

USER = role.user
ADMIN = role.admin
BANNED = role.ban

NOT_BEGIN = status.not_begin
DECLINE = status.decline
IN_PROGRESS = status.in_progress
FINISHED = status.finished

extensions = ['stl', 'stp', '3mf', 'm3d']
amdin_extensions = ['stl', 'stp', '3mf', 'm3d', 'gcode']


models_folder_path = '.\\models\\'

START_TEXT_1 = 'как тебя зовут'
START_TEXT_2 = 'ты уже есть в списках'
START_TEXT_3 = 'можешь начать пользоваться'

MAIN_MENU_TEXT = '''Главное меню
этот бот предназначен для осуществления очереди на 3д принтеры
сейчас есть возможность увидель это меню
'''


MAIN_MENU_BUTTON_1 = "Добавить модель"
MAIN_MENU_BUTTON_2 = "Посмотреть очередь"
MAIN_MENU_BUTTON_3 = "журнал ремонта \n(в разработке)"
MAIN_MENU_BUTTON_4 = "получить конфиг PrusaSlicer \n(в разработке)"


CHOISE_TEXT_1 = 'Пришли файл модели поторую хочешь поставить на печать'
CHOISE_TEXT_2 = 'текущая очередь на печать'
CHOISE_TEXT_3 = 'сейчас это недоступно'
CHOISE_TEXT_4 = 'такой команды нет'
TEXT_BACK = 'назад'

ADD_TEXT_1 = "Успешно сохранено."
ADD_TEXT_2 = 'описание, пожелания'
ADD_TEXT_3 = 'неправильное расширение'
ADD_TEXT_4 = "ошибка"
ADD_TEXT_5 = 'модель поставлена в очередь, остается только ждать'

TEXT_GET_1 = 'получить модель'
TEXT_GET_2 = 'введи номер модели которая тебе нужна'

