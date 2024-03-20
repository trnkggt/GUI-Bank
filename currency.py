import requests
from tkinter import *
from tkinter import ttk

url = 'https://api.exchangerate-api.com/v4/latest/USD'

response = requests.get(url)
data =response.json()

#wish = input('how many dollars?: ')

#converted_num = (data['rates']['USD']*data['rates']['GEL'])*float(wish)
#print(f'{wish}$ is {converted_num} GEL')

def convert():
    from_cur = from_currency.get()
    to_cur = to_currency.get()

    the_amount = amount.get()

    result = (data['rates'][from_cur]*data['rates'][to_cur])*float(the_amount)


    result_label.config(text=f'{the_amount} {from_currency_box.get()} is {round(result,2)} {to_currency_box.get()}')


print(data['rates'])
window = Tk()
window.title('Curency Converter')
window.geometry('500x500')


intro_label = ttk.Label(window, text='Welcome to Currency Converter',borderwidth=3)
intro_label.place(x=100,y = 15)
intro_label.config(foreground='blue',font='25')

date_label = ttk.Label(window, text=f'Current date is {data["date"]}')
date_label.place(x = 120, y = 40)
date_label.config(foreground='blue',font = 20)

from_currency = StringVar()
to_currency = StringVar()

from_currency_box = ttk.Combobox(window,textvariable=from_currency,justify=CENTER,state='readonly')
from_currency_box['values']= list(data['rates'].keys())
from_currency_box.current(0)
from_currency_box.place(x = 70,y = 100)

to_currency_box = ttk.Combobox(window,textvariable=to_currency,justify=CENTER,state='readonly')
to_currency_box['values'] = list(data['rates'].keys())
to_currency_box.current(0)
to_currency_box.place(x = 280, y = 100)

amount = IntVar()
amount_entry = ttk.Entry(window,textvariable=amount)
amount_entry.place(x = 180, y = 160)


result_label = ttk.Label(window,text='')

result_label.place(x = 180, y = 240 )
result_label.config(width=40, foreground='red', font='20')

submit_button = ttk.Button(window, text='Convert',command = convert)
submit_button.place(x = 180, y = 300)


window.mainloop()
