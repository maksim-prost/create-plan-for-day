import datetime
import locale
import shutil

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') 

class Wath():
    # number_current_month = (BEGIN_DAY + datetime.timedelta( days=10)).strftime('%-m')
    #расписание занятий может начинаться с последних чисел предыдущего месяца
    # current_month = (BEGIN_DAY + datetime.timedelta( days=10)).strftime('%B')
    
    def __init__(self, template_wath, begin_day, current_month) -> None:
        self.post = template_wath['post']
        self.post_usage = template_wath['post_usage']
        self.name = template_wath['name']
        self.title = template_wath['title']
        self.number = template_wath['number']
        self.cur_day = begin_day + datetime.timedelta( days=self.number-1)
        self.prev_day = self.cur_day - datetime.timedelta( days=4)
        self.folder = f"{current_month}/{self.number} караул"
        self.path_to_save = template_wath['path_to_save']
        self.email = template_wath['email']

    def next_day(self):
        self.prev_day =  self.cur_day
        self.cur_day = self.cur_day + datetime.timedelta( days=4)

    def view_cur_day(self):
        return self.cur_day.strftime('%d %B %Y')
    
    def cur_day_format(self):
        return self.cur_day.strftime('%Y-%m-%d')

    def view_prev_day(self):
        return self.prev_day.strftime('«%d» %B %Yг.')
    
    def get_current_data(self):
        context = self.__dict__.copy()
        context.update( {
            'date_of_approval': self.view_prev_day(),
            'date_of_event': self.view_cur_day(),
        } )
        return context

    def save(self, source_path, send_mail, title_month):
        path_to_direct = f'{source_path}/{self.folder}'
        # print(path_to_direct, source_path)
        if  self.path_to_save:
            shutil.copytree(f'{source_path}/{self.folder}', self.path_to_save, dirs_exist_ok=True)
        if self.email:
            zip_name = shutil.make_archive(path_to_direct, 'zip', path_to_direct)
            # print(zip_name)
            send_mail(title_month, zip_name, f'{self.folder}.zip', self.email)


class ListWath:

    def __init__(self, list_dict_wath, begin_day, send_mail) -> None:
        self.number_current_month = (begin_day + datetime.timedelta( days=10)).strftime('%-m')
        #расписание занятий может начинаться с последних чисел предыдущего месяца
        self.current_month = ( begin_day + datetime.timedelta( days=10)).strftime('%B' )
        self.list_wath = [ Wath( temp_wath, begin_day, self.current_month ) for temp_wath in list_dict_wath ]
        self.send_mail = send_mail

    def get_wathes_data(self):
        for wath in self.list_wath:
            yield wath.get_current_data()
            wath.next_day()

    def get_number_month(self):
        return self.number_current_month
    
    def get_title_month(self):
        return self.current_month
    
    def save(self, source_path):
        for wath in self.list_wath:
            wath.save(source_path, self.send_mail, self.get_title_month())
