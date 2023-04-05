import json
import re
from docxtpl import DocxTemplate
from os.path import join
import os
from tempfile import TemporaryDirectory

TEMPLATE_WORKING_OUT = "Повторение обязанностей, работа с документацией, изучение документацией предварительного планирования."


is_lecture = lambda lesson: bool(
    re.match(".*([Кк][Лл].*[Гг][Рр])|([Лл][еЕ][кК][цЦ][иИ][яЯ])", lesson)
)
format_working_out = lambda working_out: list(
    map(lambda obj: ' '.join(obj), working_out)
)


class LessonDay:
    def __init__(self):
        self.lessons = []
        self.number_standart = None
        self.learning_obj = None

    def __repr__(self) -> str:
        return f'''
            lessons={self.lessons},
            number_standart={self.number_standart},
            learning_obj={self.learning_obj},
        '''

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def get_lessons_for_summary(self):
        return self.lessons[:3]

    def get_all_lessons(self):
        return self.lessons

    def get_sport_normativ(self):
        return self.lessons[4][0].split('\n')[0].split(':')[1].strip()

    def add_number_standart(self, lesson):
        self.number_standart = lesson.split('№')[1].lstrip().split(' ')[0]

    def get_normativs(self):
        # возвращает список для возможности добавлять дополнительный норматив
        # которого нет в расписание
        return [self.number_standart, ]

    def add_learning_obj(self, lesson):
        self.learning_obj = lesson

    def get_learning_obj(self):
        return self.learning_obj


class BuildDocTemplate():

    def __init__(self, create_answere) -> None:
        self.path_to_self = os.path.dirname(__file__)
        self.working_out_dict = self.load_file('source/plan_study_obj.json')
        self.sport_standarts = self.load_file('source/phiz_normativ.json')
        self.normativs = self.load_file('source/prof_normativ.json')
        self.temp_dir = TemporaryDirectory()
        self.path_for_save = self.temp_dir.name
        # path_to_save_schedule
        self.month_lessons = {}
        self.day_lessons = []
        self.list_templates_month = []
        # self.bot_gpt = BotGPT(phone, api_id, api_hash)
        self.get_answer = create_answere

    def get_temporary_folder(self):
        return self.path_for_save

    def load_file(self, title_file):
        path_to_file = join(self.path_to_self, title_file)
        with open(path_to_file) as file:
            return json.load(file)

    def parsing_hours(self, hour_lesson) -> LessonDay:
        lesson_day = LessonDay()
        for hour, lesson in hour_lesson:
            for h in hour:
                if h == '11.40-12.25':
                    lesson_day.add_number_standart(lesson[0])
                if h == '14.00-15.30':
                    lesson_day.add_learning_obj(lesson[0])
                else:
                    lesson_day.add_lesson(lesson)
                if h == '21.00-21.20':
                    yield lesson_day
                    lesson_day = LessonDay()
        return

    def build_template(self, lesson_day: LessonDay):
        self.list_templates_by_day = []
        self.create_sport_normativ(lesson_day)
        self.create_normativ(lesson_day)
        self.create_lesson(lesson_day)
        self.create_plan_for_day(lesson_day)

    def create_sport_normativ(self, lesson_day):
        sport_normativ = lesson_day.get_sport_normativ()
        context = {
            'theme': sport_normativ,
            'subject_standart': self.sport_standarts.get(sport_normativ, sport_normativ),
        }
        self.list_templates_by_day.append(
            ('templates/методический план физ.подготовка.docx', context)
        )

    def create_normativ(self, lesson_day: LessonDay):
        for number in lesson_day.get_normativs():
            normativ = self.normativs[number]
            context = {
                'number_standart': number,
                'theme': normativ['title'],
                'subject_standart': normativ['process'],
                'result_time': normativ['score'],
                'devices': normativ['devices'],
            }
            self.list_templates_by_day.append(
                ('templates/методический план нормативы.docx', context)
            )

    def create_lesson(self, lesson_day: LessonDay):
        list_lesson = lesson_day.get_lessons_for_summary()
        for (c, d, e, f) in set(list_lesson):
            if 'пнк' not in f.lower():
                continue

            print(c)
            template, *questions = c.split('\n')
            subject_study = template.split(':')[0]
            if '«' in template:
                theme = template.split('«')[1].split('»')[0]
            else:
                theme = template.split(':')[1].split('.')[0]
            # quest_and_answ = [(quest, self.bot_gpt.create_educational_question (subject_study, theme, quest))
            #                         for quest in questions]
            quest_and_answ = [
                (quest, self.get_answer(subject_study, theme, quest))
                for quest in questions
            ]

            context = {
                'lecture': is_lecture(e),
                'theme': theme,
                'questions': quest_and_answ,
                'list_of_sources': d or '',
                'count_hour': list_lesson.count((c, d, e, f)),
                'subject_study': subject_study,
            }
            self.list_templates_by_day.append(
                ('templates/шаблон для план-конспекта на сутки.docx', context)
            )

    def create_plan_for_day(self, lesson_day: LessonDay):
        learning_obj = lesson_day.get_learning_obj()
        n_l = '\n'
        current_day_lesson = [
            f'{c.split(n_l)[0]} ({e.strip().replace(n_l, " ")}) проводит {f.strip().replace(n_l, " ")}'
            for c, _, e, f in lesson_day.get_all_lessons()
        ]
        # print(len(current_day_lesson), current_day_lesson)
        self.day_lessons = [
            lesson for lesson in set(
                lesson_day.get_all_lessons()[:3]
            ) if is_lecture(lesson[2])
        ]
        context = {
            'learning_obj': learning_obj and learning_obj.split(n_l)[0] or TEMPLATE_WORKING_OUT,
            'current_day_lesson': current_day_lesson,
            'theme': 'План работы на день'
        }
        self.list_templates_by_day.append(('templates/план работы на сутки.docx', context))
        # self.save_in_docx(context,'план работы на сутки.docx',f"{self.folder}/план работы на {context['date_of_event']}.docx")

    def update(self, wath_info):
        # print(wath_info['folder'],)
        current_day = wath_info['date_of_event']
        self.month_lessons.setdefault(
            wath_info['folder'], []).extend(
                (current_day,) + lesson for lesson in self.day_lessons
            )
        for template in self.list_templates_by_day:
            template[1].update(wath_info)
            template[1]['lesson_obj_for_plan'] = self.working_out_dict.get(current_day, [])
        self.list_templates_month.extend([(templates[0], templates[1].copy()) for templates in self.list_templates_by_day])

    def save(self):
        for title_template, template in self.list_templates_month:
            folder_for_save = join(self.path_for_save, template['folder'], template['date_of_event'])
            os.makedirs(folder_for_save, exist_ok=True)
            title_template = join(self.path_to_self, title_template)
            title_save = join(folder_for_save, template["theme"].replace('/', '')[:45] + '.docx')
            run_template(title_template, template, title_save)

        for folder, render_month_lessons in self.month_lessons.items():
            title_template = join(self.path_to_self, 'templates/список занятий на месяц.docx')
            template = {'list_lesson': render_month_lessons}
            title_save = join(self.path_for_save, folder, 'список занятий на месяц.docx')
            run_template(title_template, template, title_save)
        return


def run_template(title_template, render, title_save):
    doc = DocxTemplate(title_template)
    doc.render(render)
    doc.save(title_save)
