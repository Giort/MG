### MG
##### Input form check
###### скрипт для проверки работы форм для заполнения МГ при вводе корректных данных:
 
    В лог выводится сообщение "ОК", если данные были отправлены и отобразилось сообщение об успехе
    В лог выводится сообщение "ERROR", если это сообщение не отобразилось 
        или если форма не была найдена по селектору
                     
##### MG block availability check
###### скрипт проверяет, присутствуют ли все блоки на МГ:
 
    В лог выводится сообщение "ОК", если блок виден
    В лог выводится сообщение "ERROR", если блок не виден

##### Service check
###### скрипт проверяет, что сайты МГ в апе:
 
    В лог выводится сообщение "ОК", если ресурс доступен
    В лог выводится сообщение "ERROR", если не удалось дождаться 
        загрузки элемента, по которому проводится проверка

##### SOW modal window check
###### скрипт проверяет, что слайдеры СП загружены и в них открываются окна: 
 
    В лог выводится сообщение "ОК", если слайдер есть и "ОК" если окно открылось
    В лог выводится сообщение "ERROR", если не удалось найти кнопку на карточке в слайдере
        или если не открылось окно

##### Genplan check
###### скрипт проверяет, что Генплан на сайтах посёлков загружается: 
 
    В лог выводится сообщение "ОК", если отображается элемент на загруженном генплане
    В лог выводится сообщение "ERROR", если этот элемент не загрузился

##### SO qty check
###### скрипт проверяет, сколько участков СП осталось в посёлке: 
 
    В лог выводится сообщение "ERROR", если участков осталось два или меньше


test - скрипты для отработки кода                     
