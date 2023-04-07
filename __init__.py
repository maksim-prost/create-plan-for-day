# import json
# from random import choice
import os
# import re
import glob
import docx
import shutil
from send_mail import message_sender

from wath import ListWath
from build_doc_template import BuildDocTemplate
from config import (
    PATH_TO_DIR_WITH_SCHEDULE,
    # PATH_TO_SAVE_SCHEDULE,
    BEGIN_DAY,
    list_dict_wath,
)
from config_api import (
    api_key,
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    HOST,
)
from gpt import create_answere



# MONTH_TO_SCHEDULE = LIST_WATH[0].number_current_month
# list_wath.get_title_month() = LIST_WATH[0].current_month


def create_docx_from_doc(number_month) -> str:
    # print(f'libreoffice  --headless --convert-to docx "{PATH_TO_DIR_WITH_SCHEDULE}{number_month}*.doc"')
    cwd = os.getcwd()
    os.chdir(PATH_TO_DIR_WITH_SCHEDULE)
    os.system(f'libreoffice  --headless --convert-to docx {number_month}*.doc > /dev/null 2>&1')
    # list_convert_docx = [file_name for file_name in os.listdir(PATH_TO_DIR_WITH_SCHEDULE) if re.search(rf'{number_month}.*\.docx', file_name)]
    list_convert_docx = glob.glob(f'{PATH_TO_DIR_WITH_SCHEDULE}{list_wath.get_number_month()}*.docx')
    os.chdir(cwd)
    if list_convert_docx:
        return docx.api.Document(list_convert_docx[0])
        return list_convert_docx[0]


def load_hour_lesson(doc):
    schedule = doc.tables[0]
    return [
        (b.text.strip().split('\n'), (c.text.strip(), d.text and d.text.strip(), e.text.strip(), f.text.strip()))
        for (_, b, c, d, e, f) in map(lambda row: row.cells, schedule.rows[1:])
    ]


def create_plan_for_day(list_wath, hour_lesson):
    builder = BuildDocTemplate(create_answere(api_key))
    for lessons_by_day in builder.parsing_hours(hour_lesson):
        builder.build_template(lessons_by_day)
        for wath_update in list_wath.get_wathes_data():
            builder.update(wath_update)
    builder.create_doc()
    list_wath.save(builder.get_temporary_folder())
    # return builder


if (__name__ == '__main__'):
    list_wath = ListWath(list_dict_wath, BEGIN_DAY, message_sender(EMAIL_ADDRESS, EMAIL_PASSWORD, HOST))
    doc = create_docx_from_doc(list_wath.get_number_month())
    create_plan_for_day(list_wath, load_hour_lesson(doc))
