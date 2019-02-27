# -*- coding: utf-8 -*-
import copy
import collections
import re
from datetime import date, time

class Parser():
    def writeinfile(self, sym, svodka, allsym, user_proc):
        lesson2 = open("lesson2.txt", "w")
        lesson2.write('Всего коммитов за весь период: '+str(sym))
        print('Всего коммитов за весь период: '+str(sym))
        for key, val in svodka.items():
            #for i in val:
            lesson2.write('\nПользователь '+str(key)+' сделал '+str(val[0])+' коммитов, это составило '+str(val[1])+' от общего количества коммитов за период.')
            print('\nПользователь '+str(key)+' сделал '+str(val[0])+' коммитов, это составило '+str(val[1])+' от общего количества коммитов за период.')
        lesson2.write('\n\nВсего коммитов за период c последнего коммита 2019 года по декабрь 2018: '+str(allsym))
        print('\n\nВсего коммитов за период c последнего коммита 2019 года по декабрь 2018: '+str(allsym))
        for key, val in user_proc.items():
            lesson2.write('\nПользователь '+str(key)+' сделал '+str(val[0])+' коммитов за период, это составило '+str(val[1])+' от общего количества коммитов за период.')
            print('\nПользователь '+str(key)+' сделал '+str(val[0])+' коммитов за период, это составило '+str(val[1])+' от общего количества коммитов за период.')
        lesson2.close()
        print('Файл создан')
        return 
    def user_procent(self, allsym, kol_commit_user_for_per):
        user_proc={}
        for key, val in kol_commit_user_for_per.items():
            u=[]
            for i in val:
                u.append(i)
                u.append(str(float((i*100)/allsym))+' %')
            user_proc.update({key:u})
        return user_proc

    def kol_commit_in_period(self, low_date_array, high_date_array, user_date):
        allsym=0
        kol_commit_user_for_per={}
        for key, val in user_date.items():
            high_date = high_date_array.get(key)
            low_date = low_date_array.get(key)
            sym=0
            user_commit_and_procent=[]
            for i in val:
                if high_date>=i>=low_date:
                    sym+=1
            allsym=allsym+sym
            if sym!=0:
                #print(key, sym, float((sym*100)/allsym))
                user_commit_and_procent.append(sym)
                #user_commit_and_procent.append(float(sym*100)/allsym)
            if user_commit_and_procent!=[]:
                kol_commit_user_for_per.update({key: user_commit_and_procent })

        return allsym, kol_commit_user_for_per
    def previous_month(self, high_date_array, month):
        low_date_array = copy.deepcopy(high_date_array)
        for key, val in low_date_array.items():
            #print(high_date_array[val].year)
            yyyy = int(((val.year* 12 + val.month) + month)/12)
            mm = int(((val.year * 12 + val.month) + month)%12)
            if mm == 0:
                yyyy -= 1
                mm = 12
            low_date_array[key]=val.replace(year=yyyy, month=mm)
        #print(low_date_array)

        return low_date_array

    def high_date(self, user_date):
        high_date_array={}
        date_list=[]
        y=date(2015, 1, 1)
        for key, val in user_date.items():
            u=[]
            for i in range(len(val)):
                if y<val[i]:
                    y=val[i]
            high_date_array[key]=y
        return high_date_array

    def date_parsing(self, array):
        #date=[]
        user_date={}
        #dateafterpars = datetime.date()
        for key, val in array.items():#уровень значений словарей, которые списки\
            ymd=[]
            for i in val:# уровень перебора списка
                #print(i)
                pars_data = re.split('-', i)# парсинг элемента списка
                dateafterpars = date(int(pars_data[0]), int(pars_data[1]), int(pars_data[2]))#.strftime("%Y-%m-%d")
                #print(dateafterpars.strftime("%Y-%m-%d"))
                #for x in pars_data:#перебор элементов даты
                #    date.append(int(x))
                #print(date)
                ymd.append(dateafterpars)
                #print(ymd)
                #dateafterpars=[]
                #print(date)
            user_date[key]=ymd
            #print(key)
        return user_date



    def svodka(self, array, sum):
        svod={}
        g=[]
        for key, val in array.items():
            if len(val) != 0:
                g.append(str(len(val)))
                b= float('{:.3f}'.format((len(val)*100)/sym))
                g.append(b)
                svod.update({key : g})#допиши знак % в файл
                g=[]
        return svod

    def vsego(self, array):
        sym=0
        for key, val in array.items():
            sym=sym+len(val)
        return sym

    def open_file(self, src):
        try:
            log_file = open(src, 'r')
        except(IOError)as e:
            print('Вы ввели неверный путь')
        else:
            log = log_file.read()
            log_file.close()
            print('Все хорошо')
            return log

    def sort(self, log):
         dict_my=[]
    	 text = re.split('--', log)
    	 for line in text:
            if line != '':
                dict_my.append(line)
         array={}
         user_list = re.findall(r'us\w*', log)
         result = collections.Counter(user_list)
         for elem in result:
            array.update({elem : '' })
         g = []
         for key in array:
            for line in dict_my:
               if key in line:
                   yu = re.search(r'us\w*', line)
                   yer = re.search(r'\d\d\d\d-\d\d-\d\d', line)
                   if yer is not None:
                       fg = yer.group(0)
                   if yu is not None:
                       fgf = yu.group(0)
                   if len(key) == len(fgf):
                       g.append(fg)
            array[key]=g
            g= []
         return array
if __name__ == "__main__":
    parser1 = Parser()
    src = raw_input('Введите путь к файлу: ')
    log = parser1.open_file(src)
    array = parser1.sort(log)
    sym = parser1.vsego(array)
    svodka = parser1.svodka(array, sym)
    user_date=parser1.date_parsing(array)
    high_date_array = parser1.high_date(user_date)
    mm=-2
    low_date_array = parser1.previous_month(high_date_array, mm)
    allsym,kol_commit_user_for_per=parser1.kol_commit_in_period(low_date_array, high_date_array, user_date)
    user_proc = parser1.user_procent(allsym,kol_commit_user_for_per)
    parser1.writeinfile(sym, svodka, allsym, user_proc)
