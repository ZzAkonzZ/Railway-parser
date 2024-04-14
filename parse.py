import threading # Библиотека для таймера
import requests # Библиотека для запроса
import re # Библиотека для регулярных выражений
import datetime # Библиотека для даты и времени

def request():
    # Ссылка с сайта railways.kz Атырау -> Актобе на дату 14.04.2024
    url = 'https://bilet.railways.kz/sale/default/route/search?route_search_form%5BdepartureStation%5D=2704830&route_search_form%5BarrivalStation%5D=2704600&route_search_form%5BforwardDepartureDate%5D=14-04-2024%2C+вск&route_search_form%5BbackwardDepartureDate%5D='
    html = requests.get(url).text  # Получить html код сайта
    return html # Возвратить html

def search():
    pattern = """
    .*<tbody>
        .*<tr>
            .*<td class="left aligned">
                .*<h4 class="ui header">
                    .*Плацкарт
                    .*<span class="sub header">
                        .*\((.*)\s.*\)
                    .*<\/span>
                .*<\/h4>
            .*<\/td>
            .*<td class="right aligned">
                .*<h4 class="ui apple header ">
                    .*(.*)
                .*<\/h4>
            .*<\/td>
        .*<\/tr>
        .*<tr>
            .*<td class="left aligned">
                .*<h4 class="ui header">
                    .*Купе
                    .*<span class="sub header">
                        .*\((.*)\s.*\)
                    .*<\/span>
                .*<\/h4>
            .*<\/td>
            .*<td class="right aligned">
                .*<h4 class="ui apple header ">
                    .*(.*)
                .*<\/h4>
            .*<\/td>
        .*<\/tr>
    .*<\/tbody>
    """ # Паттерн с помощью регулярных выражений для поиска по html поиска доступных мест
    string = request() # Получить html
    match = re.search(pattern, string) # Поиск совпадений по Паттерну из html строки (первое совпадение)
    if match: # Если есть совпадения
        standard, lux = int(match[1]), int(match[3]) # Распределить по переменных 2 группы совпадений (количество свободных мест)
        return {'standard': standard, 'lux': lux} # Возвратить ввиде словаря

def parse():
    interval = 30 # Интервал в секундах
    threading.Timer(interval, parse).start()
    result = search() # Получить результаты
    bot(result) # Отправить результаты

def bot(tickets):
    TOKEN = '6984088135:AAHEcTblcBw96w-jqQdo9apCpRWJP_yEkig' # Токен полученный с BotFather в телеграме
    chat_id = 542347555 # Идентификатор чата для отправки сообщения пользователю (мне)
    if tickets: # Проверка не пуст ли словарь, тоесть наличие свободных мест
        if tickets['lux'] >= 50 or tickets['standard'] >= 30: # Простое условие который можно менять значения
            message = f"Плацкарт: {tickets['standard']}\nКупе: {tickets['lux']}" # Создание сообщения
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}" # Отправка сообщения
            print(requests.get(url).json()) # Отправить GET запрос, Выводить в консоль результаты
    else: # Если билетов нету
        print("Что то пошло не так", datetime.datetime.now()) # Выводить в консоль это сообщение с датой когда случилась ошибка или не было билетов

def chat():
    TOKEN = '6984088135:AAHEcTblcBw96w-jqQdo9apCpRWJP_yEkig' # Токен полученный с BotFather в телеграме
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates" # Вывести в консоль последние обновления, также получить идентификатор чата
    print(requests.get(url).json()) # Отправить запрос и вывести в консоль

if __name__ == '__main__':
    parse() # Запускаем парсинг