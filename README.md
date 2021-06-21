# vista-phone-book
**Тестовое задание для ВистаМед, телефонная книжка**

Телефонная книжка - приложение для записи контактов 
с их телефонами и датами рождения.

## Стэк
* Python 3.7
* PyQt5
* MariaDB

## Схема ДБ
![схема](https://github.com/plaunezkiy/vista-phone-book/blob/main/db_schema.PNG)

## Установка и запуск проекта
* Склонируйте репозиторий
    * ```git clone https://github.com/plaunezkiy/vista-phone-book.git```
    

* Установите и активируйте виртуальную среду
    * ```python -m venv venv```
    * Windows GitBash:
        * ```source venv/scripts/activate```
    * Linux:
        * ```source venv/bin/activate```
    

* Установите зависимости проекта
    * ```pip install -r requirements.txt```
    

* Заполнить конфиг для подключения к базе данных
    * Запустить mysql сервер MariaDB
    * вписать значения в начало файла phone_book/modules/db.py


* При желании, инициализируйте базу и загрузите тестовые данные
    * см. файл phone_book/modules/db.py
    * раскомментируйте команды в __main__
    * запустите файл db.py:
        * ```python phone_book/modules/db.py```
    

* Запустите приложение и звоните друзьям, чтобы поздравить с днем рождения
    * ```python phone_book/main.py```
