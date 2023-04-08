### MG
##### Input form check
###### скрипт для проверки работы форм для заполнения МГ при вводе корректных данных:
 
    В лог выводится сообщение "ОК", если данные были отправлены и отобразилось сообщение об успехе
    В лог выводится сообщение "ERROR", если не получилось успешно завершить процесс отправки данных 
        или если форма не была найдена по локатору
                     
##### MG block availability check
###### скрипт проверяет, присутствуют ли все блоки на МГ, и в некоторых из них проверяет наличие их внутренних 
###### элементов
 
    В лог выводится сообщение "ОК", если блок виден
    В лог выводится сообщение "ERROR", если блок не виден или не виден какой-либо из внутренних элементов

##### Service check
###### скрипт проверяет, что сайты МГ доступны:
 
    В лог выводится сообщение "ОК", если ресурс доступен
    В лог выводится сообщение "ERROR", если не удалось дождаться 
        загрузки элемента, по которому проводится проверка

##### SOW modal window check
###### скрипт проверяет, что модальные окна Спецпредложений на сайтах МГ работают корректно 
 
    В лог выводится сообщение "ОК", если есть слайдер; окно открылось; заявка была отправлена
    В лог выводится сообщение "ERROR", если не удалось найти кнопку на карточке в слайдере; не открылось окно;
        не получилось успешно завершить процесс отправки данных

##### Genplan check
###### скрипт проверяет, что Генплан на сайтах посёлков загружается: 
 
    В лог выводится сообщение "ОК", если отображается элемент на загруженном генплане
    В лог выводится сообщение "ERROR", если этот элемент не загрузился

##### SO qty check MG
###### скрипт проверяет, сколько участков СП осталось у посёлка на сайте МГ: 
 
    В лог выводится сообщение "ERROR", если участков осталось два или меньше, а также 
        выводятся сообщения с количеством участков в каждом посёлке и общее количество участков
    Прим.: скрипт использует страницу, которая больше не включена в карту сайта МГ, однако на ней по-прежнему 
        выводятся актуальные предложения, которые соответствуют данным на действующих страницах

##### SO qty check LP
###### скрипт проверяет, сколько участков СП осталось на страницах посёлков: 
 
    В лог выводится сообщение "ERROR", если участков осталось два или меньше

##### Vurtour check
###### скрипт проверяет, загружается ли Виртуальный тур на страницах посёлков: 
 
    В лог выводится сообщение "ОК", если отображается элемент на загруженном Виртуальном туре
    В лог выводится сообщение "ERROR", если этот элемент не загрузился

##### LP forms check
###### группа скриптов, которые проверяют, отправляются ли данные из модальных окон и форм 
###### на лендингах посёлков
 
    В лог выводится сообщение "ОК", если данные были успешно отправлены и отобразился подтверждающий элемент
    В лог выводится сообщение "ERROR", если проверка формы не удалась

##### mail option check + credentials
###### скрипт для массового изменения пользовательских настроек в аккаунтах на Я.Почте  
 
    Скрипт последовательно заходит на страницы настроек в аккаунтах и отмечает нужный чекбокс


test - скрипты для отработки кода                     
