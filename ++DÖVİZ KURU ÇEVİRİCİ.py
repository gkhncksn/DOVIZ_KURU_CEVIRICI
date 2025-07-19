import requests
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import re
from tkinter import ttk
import datetime

class RealTimeCurrencyConverter():
    def __init__(self,url):
            self.data = requests.get(url).json()
            self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
  
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        # self.title = 'ONLINE DÖVİZ KURLARI'
        self.wm_title("ONLINE DÖVİZ KURLARI")
        self.currency_converter = converter


        #self.configure(background = 'blue')
        self.geometry("500x200")
        
        # Label
        self.intro_label = Label(self, text = 'ONLINE DÖVİZ KURLARI',  fg = 'blue', relief = "solid", 
                                 width = 40, justify = tk.CENTER, borderwidth = 0)
        self.intro_label.config(font = ('Trebuchet MS',15,'bold'))
        date_str = self.currency_converter.data['date']
        formatted_date = self.format_date(date_str)
        self.date_label = Label(self, text = f"1 Amerikan Doları = {self.currency_converter.convert('USD','TRY',1)} Türk Lirası \n1 Euro = {self.currency_converter.convert('EUR','TRY',1)} Türk Lirası \nTarih : {formatted_date}", 
                                 justify = tk.CENTER, fg = 'black', relief = "solid", borderwidth = 0)
        self.date_label.config(font = ('Trebuchet MS',12,'bold'))
        
        self.intro_label.place(x = 10 , y = 5)
        self.date_label.place(x = 100, y= 40)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self, width = 19, bd = 1, relief = tk.RIDGE, justify = tk.CENTER, validate='key', validatecommand=valid)
        self.amount_field.insert(0, "1")
        self.converted_amount_field_label = Label(self, text = '', fg = 'white', bg = 'red', 
                                                  relief = tk.RIDGE, justify = tk.CENTER, width = 16, borderwidth = 1)

        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("USD") # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("TRY") # default value

        font = ("Arial", 11, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,values=list(self.currency_converter.currencies.keys()), 
                                                   font = font, state = 'readonly', width = 12, justify = tk.CENTER)
        self.from_currency_dropdown.bind("<<ComboboxSelected>>", lambda event: self.perform())
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,values=list(self.currency_converter.currencies.keys()), 
                                                 font = font, state = 'readonly', width = 12, justify = tk.CENTER)

        self.from_currency_dropdown.place(x = 30, y= 120)
        self.amount_field.place(x = 30, y = 150)
        self.to_currency_dropdown.place(x = 340, y= 120)
        self.converted_amount_field_label.place(x = 340, y = 150)
        
        self.convert_button = Button(self, text = "ÇEVİR", command = self.perform, bg = "blue", fg = "black", 
                                     activebackground = "black", activeforeground = "white", width = 15, height = 2)
        self.convert_button.config(font=('Trebuchet MS', 10, 'bold'))
        self.convert_button.place(x = 180, y = 120)

    def perform(self):
        try:
            amount = float(self.amount_field.get())
        except ValueError:
            tk.messagebox.showerror("Hata", "Lütfen geçerli bir miktar girin")
            return

        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 2)
        self.converted_amount_field_label.config(text = str(converted_amount))

    def format_date(self, date_string):
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return date_object.strftime("%d.%m.%Y")
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    App(converter)
    mainloop()