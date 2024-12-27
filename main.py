import flet as ft
import time
import serial

'''
Краткий обзор:

    Поле вывода данных score_field - показывает количество импульсов полученных с Arduino
    Кнопка Включения start_btn - устанавливает связь с Arduino и выводит занчение кол-ва импульсов в поле данных
    Кнопка выключения stop_btn - останавливает получение данных с Arduino
    Поле ИИ set_btn - моделирует источник ИИ, сколько импульсов может получить Arduino
    Иконка оповещения об опастности - оповещает об угрозе, если значение кол-ва полученных импульсов больше установленных (по умолчанию 500) 
'''

'''
Функция data_arduino получает данные с ардуино при кадом вызове с задержкой в 1 секунду
'''
def data_arduino(b = 500):
    # Открываем Serial порт
    ser = serial.Serial('COM2', 9600)

    # Читаем ответ от Arduino через Serial порт и Декодируем ответ из байтов в строку с использованием UTF-8
    response = ser.readline()
    decoded_response = response.decode('utf-8')

    ser.close()
    print(decoded_response)
    return decoded_response

""" 
Функция main создает окно для вывода данных полученных с Arduino
"""
def main(page: ft.Page):
    page.title = "Счетчик"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = 'light'
    page.window.width = 500
    page.window.height = 320
    page.window.resizable = False
    page.window.maximizable = False

    # Функция получения данных
    def start_getdata_arduino(e):
        start_btn.disabled = True
        set_btn.disabled = True
        stop_btn.disabled = False
        while not stop_btn.disabled:
            score_field.value = str(data_arduino(int(set_btn.value)))
            if int(score_field.value) > 500:
                warning_icon.color = ft.Colors.RED_600
            else:
                warning_icon.color = ft.Colors.GREY
            page.update()
            time.sleep(1)

    # Фунцкия остановки получения данных
    def stop_getdata(e):
        start_btn.disabled = False
        set_btn.disabled = False
        stop_btn.disabled = True
        warning_icon.color = ft.Colors.GREY
        page.update()

    # Поле вывода количества импульсов
    score_field = ft.TextField(
        value="0",
        text_align=ft.TextAlign.END,
        read_only=True
    )
    # Кнопка включения
    start_btn = ft.ElevatedButton(
        text="Включить",
        width=150,
        height=50,
        on_click=start_getdata_arduino
    )
    # Кнопка выключения
    stop_btn = ft.ElevatedButton(
                                text='Выключить',
                                on_click=stop_getdata,
                                width=150,
                                height=50
    )
    # Поле установки занчения ИИ
    set_btn = ft.TextField(label='Ионизирующее Излучение', width=200, value='500', text_align=ft.TextAlign.CENTER)
    # Иконка показывающая уведомление об опастности, если кол-во импульсов больше определенного значения
    warning_icon = ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.GREY)

    column_field = ft.Column(
        [
            score_field,
            ft.Row([start_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([stop_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([set_btn], alignment=ft.MainAxisAlignment.CENTER),
            warning_icon
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    page.add(
        column_field
    )



if __name__ == "__main__":
    ft.app(target=main)