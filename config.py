import datetime

begin_day = '31.03.2023'
BEGIN_DAY = datetime.datetime(*map(int, reversed(begin_day.split('.'))))
# Внимание требует формат docx
# PATH_TO_SCHEDULE = '/home/mkornev/Документы/3 карул/Занятия/расписание/11 ноябрь.docx'
PATH_TO_SAVE_SCHEDULE = '/home/mkornev/Документы/3 карул/Занятия/планы/temp'
PATH_TO_DIR_WITH_SCHEDULE = '/home/mkornev/Документы/3 карул/Занятия/расписание/'
TEMPLATE_WORKING_OUT = "Повторение обязанностей, работа с документацией, изучение документацией предварительного планирования."

# list_addres =  ['pch-72med@mail.ru', 'sharov87@bk.ru', 'priora1441@mail.ru' ]

list_dict_wath = [

    {
        'post': "Помощник начальника караула",
        'post_usage': "помощника начальника 1 караула",
        'name': "А.В. Чикуров",
        'title': "прапорщик внутренней службы",
        # 'post': "Командир отделения",
        # 'post_usage': "командира отделения 1 караула",
        # 'name': "С.П. Горячкин",
        # 'title': '',
        'number': 1,
        'email': [],
        # 'email': ['pch-72med@mail.ru',],
        'path_to_save': '',
    },

    {
        'post': "Командир отделения",
        'post_usage': "командира отделения 2 караула",
        # 'name': "В.В. Быков",
        'name': "М.В. Шаров",
        'title': '',
        'number': 2,
        'email': [],
        # 'email': ['sharov87@bk.ru',],
        'path_to_save': '',
    },

    {
        'post': "Помощник начальника караула",
        'post_usage': "помощника начальника 3 караула",
        'name': "М.В.Корнев",
        'title': "прапорщик внутренней службы",

        # 'post': "Командир отделения",
        # 'post_usage': "командира отделения 3 караула",
        # 'name': "Д.В. Ключеров",
        # 'title': '',
        'number': 3,
        'email': ['zendzin@list.ru', ],
        'path_to_save': '/home/mkornev/Документы/3 карул/Занятия/планы/temp3',
    },

    {
        'post': "Командир отделения",
        'post_usage': "командира отделения 4 караула",
        # 'name': "С.К. Гудков",
        'title': '',

        # 'post': "Помощник начальника караула",
        # 'post_usage': "помощника начальника 4 караула",
        'name': "А.И. Савченко",
        # 'title': "старший прапорщик внутренней службы",
        'number': 4,
        # 'email': ['priora1441@mail.ru',],
        'email': [],
        'path_to_save': '',
    },

]
