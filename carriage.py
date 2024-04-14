import threading
import requests
import re
import datetime

def request():
    # Ссылка с сайта railways.kz Атырау -> Актобе на дату 14.04.2024 после выбора поезда
    url = 'https://bilet.railways.kz/sale/default/car/search?car_search_form%5BdepartureStation%5D=2704830&car_search_form%5BarrivalStation%5D=2704600&car_search_form%5BforwardDirection%5D%5BdepartureTime%5D=2024-04-14T14%3A35%3A00&car_search_form%5BforwardDirection%5D%5BfluentDeparture%5D=&car_search_form%5BforwardDirection%5D%5Btrain%5D=691Х&car_search_form%5BforwardDirection%5D%5BisObligativeElReg%5D=0&car_search_form%5BbackwardDirection%5D%5BdepartureTime%5D=&car_search_form%5BbackwardDirection%5D%5BfluentDeparture%5D=&car_search_form%5BbackwardDirection%5D%5Btrain%5D=&car_search_form%5BbackwardDirection%5D%5BisObligativeElReg%5D='
    html = requests.get(url).text  # Получить html код сайта
    return html # Возвратить html

def search():
    bot_q = 0 # Переменная для количества нижних мест
    top_q = 0 # Переменная для количества верхних мест
    # pattern = '<divclass="cabins"><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><divclass="cabin"><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><divdata-tooltip="(?:.*)"class="seatuicheckbox(.*)">(?:.*)<\/div><\/div><\/div>'
    # pattern = """<div data-tooltip="(?:.*)" class="seat ui checkbox(?:.*)"><input value="(\d{1,})" class="places" name="buy_form_contract(?:.*)" type="checkbox"(?:.*)>"""
    find_bot = '(?:br|bl)(?:\s)"><input value="(\d{1,})"' # Паттерн для поиска доступных нижних мест
    find_top = '(?:tr|tl)(?:\s)"><input value="(\d{1,})"' # Паттерн для поиска доступных верхних мест
    string = request() # Получить html
    match = re.finditer(find_bot, string) # Поиск ВСЕХ совпадений по Паттерну из html строки
    for _ in match: # Цикл который проходит по всем совпадениям
        bot_q += 1 # Подсчет количества доступных мест (по совпадению)

    if bot_q > 3: # Если доступных мест больше трех
        return bot_q # Возвратить

def parse():
    interval = 30 # Интервал в секундах
    threading.Timer(interval, parse).start()
    result = search() # Получить результаты
    bot(result) # Отправить результаты

def bot(seats):
    TOKEN = '6984088135:AAHEcTblcBw96w-jqQdo9apCpRWJP_yEkig' # Токен полученный с BotFather в телеграме
    chat_ids = [542347555] #1065800222, Создание списка тех кому нужно отправить сообщение
    if seats: # Если есть места
        for chat_id in chat_ids: # Отправить по циклу сообщения тем кто есть в списке
            message = f"Нижних мест: {seats}" # Создание сообщения
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}" # Отправка сообщения
            requests.get(url).json() # Отправить GET запрос
            print("Билеты появились", datetime.datetime.now().strftime('%H:%M:%S')) # Выводить в консоль результаты
    else: # Если билетов нету
        print("Билетов пока мало", datetime.datetime.now().strftime('%H:%M:%S')) # Выводить в консоль это сообщение с датой когда случилась ошибка или не было билетов

def chat():
    TOKEN = '6984088135:AAHEcTblcBw96w-jqQdo9apCpRWJP_yEkig' # Токен полученный с BotFather в телеграме
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates" # Вывести в консоль последние обновления, также получить идентификатор чата
    print(requests.get(url).json()) # Отправить запрос и вывести в консоль

if __name__ == '__main__':
    # chat()
    # print(search())
    parse()
    # print(request())