import os
import shutil
import datetime
import pythonping


def if_ARM_online(arm):
    response = pythonping.ping(arm, count=1)
    if response.success():
        print(arm + ' доступен')
    else:
        print(arm + ' не доступен')
        return False

def logwritting(data):
    with open(way_to + '\\log.txt', 'a')as logfile:
        logfile.write(data + '\n')


# динамический путь
way_to = os.path.abspath(__file__)
way_to = os.path.dirname(way_to)
#print(way_to)

DT_version = "Drv_15_33\\vid.bat"
user = "gmc\\" + input("input username ")
pasw = input("iput password ")
linebreake = '********************'

# подгатавливаем файл логов к записи событий данной сессии
with open(way_to + '\\log.txt', 'w') as logfile:
    logfile.write(str(datetime.datetime.now()) + '\n')

with open(way_to + "\list.txt") as list_of_arms:  # читаем названия армов из файла list.txt
    for row in list_of_arms:
        row = row.strip()
        logwritting(linebreake)
        logwritting(row)

        print(linebreake)  # отделить строчкой утсановку разных армов

        # определяем, доступен ли АРМ, если нет покидаем данную итерацию
        if if_ARM_online(row) == False:
            logwritting('не доступен')
            continue

        try:  # копирование дистрибутива
            print('Starting instalation, copy distrib file to ' + row)
            shutil.copytree(way_to + "\soft", '\\\\' + row + "\c$\pack")
        except FileExistsError:
            print('folder allready exist, deleting')
            shutil.rmtree('\\\\' + row + "\c$\pack")
            print('trying to copy one more time')
            shutil.copytree(way_to + "\soft", '\\\\' + row + "\c$\pack")
            print('file copyng complete')

        # устанавливаем новую версию
        print('installing new version of soft')
        os.system(
            way_to + '\\psexec.exe \\\\' + row + ' -u ' + user + ' -p ' + pasw + ' -h \"C:\\pack\\' + DT_version + '\"')
        print('delete remote folder with distrib file')
        shutil.rmtree('\\\\' + row + "\c$\pack")
        print('installing on ' + row + ' complete')
        logwritting("OK")