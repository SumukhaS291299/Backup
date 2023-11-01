import datetime

from kivy.core.window import WindowBase
import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix import boxlayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.spinner import Spinner

WindowBase.keyboard_anim_args = {'d': 0.5, 't': 'in_out_quart'}
WindowBase.softinput_mode = 'below_target'


class CurrencyConverter(App):
    CountryCurrencyList = []
    CountrySymbolList = []

    def build(self):
        global CountryCurrencyList, CountrySymbolList
        self.window = boxlayout.BoxLayout(orientation='vertical')
        self.MainText = "Application Started..."
        self.CurrencyCodes = {}
        self.store = JsonStore('CurrencyCodes.json')
        self.welcome = Label(text="Currency Converter", font_size=60)
        self.window.add_widget(self.welcome)
        if self.store.exists("LastUpdated"):
            lastLoad = datetime.datetime.strptime(self.store.get("LastUpdated").get("time"), "%m/%d/%Y, %H:%M:%S")
            diff = datetime.datetime.now() - lastLoad
            if diff.seconds > 21600:
                self.StoreSymbols()
        else:
            self.StoreSymbols()
        self.LoadSymbols()
        self.InputCurrNumb = TextInput(text="1", font_size=20, multiline=False, size_hint=(.25, .35), height=150,
                                       pos_hint={'center_x': .5, 'center_y': .5})
        self.InputCurrNumb.bind(text=self.on_enter)
        self.window.add_widget(self.InputCurrNumb)
        self.InputCurrNumbValidation = Label(text="")
        self.window.add_widget(self.InputCurrNumbValidation)
        CountrySymbolList.sort()
        CountryCurrencyList.sort()
        self.CountrySymbolDropDown = Spinner(text="INR", values=CountrySymbolList, size_hint=(None, None),
                                             size=(100, 44),
                                             pos_hint={'center_x': .5, 'center_y': .5})
        self.window.add_widget(self.CountrySymbolDropDown)
        self.CountryCurrencyDropDown = Spinner(text="Indian Rupee", values=CountryCurrencyList,
                                               size_hint=(None, None),
                                               size=(250, 44),
                                               pos_hint={'center_x': .5, 'center_y': .5})
        self.window.add_widget(self.CountryCurrencyDropDown)
        self.CountrySymbolDropDown.bind(text=self.show_selected_value)
        self.CountryCurrencyDropDown.bind(text=self.show_selected_value)
        self.OutRate = Label(text="0 INR")
        self.window.add_widget(self.OutRate)
        self.GetCurrency = Button(text="Get Result")
        self.GetCurrency.bind(on_press=self.getRelativeCurrency)
        self.window.add_widget(self.GetCurrency)
        return self.window

    def getRelativeCurrency(self,instance):
        Numerical = float(self.InputCurrNumb.text)
        BaseCurrency = self.CountrySymbolDropDown.text
        if self.store.count() > 0:
            if self.store.exists("INR"):
                INRRATE = float(self.store.get("INR").get("Rate"))
                WantCurrenctRate = float(self.store.get(BaseCurrency).get("Rate"))
                UNITRate = INRRATE / WantCurrenctRate
                OUTRateValue = Numerical * UNITRate
                self.OutRate.text = str(OUTRateValue)

    def on_enter(self, instance, value):
        try:
            intValue = int(value)
            self.InputCurrNumbValidation.text = "Valid Currency Input"
            self.GetCurrency.disabled = False
        except:
            try:
                intValue = float(value)
                self.InputCurrNumbValidation.text = "Valid Currency Input"
                self.GetCurrency.disabled = False
            except:
                self.InputCurrNumbValidation.text = "Invalid Currency Input"
                self.GetCurrency.disabled = True


    def show_selected_value(self, spinner, text):
        try:
            if len(text) == 3:
                self.CountryCurrencyDropDown.text = self.store.get(text).get("Country")
            else:
                for code in self.store.keys():
                    if self.store.get(code).get("Country") == text:
                        self.CountrySymbolDropDown.text = code
                        break
        except:
            pass

    def StoreSymbols(self):
        print("This is running")
        global CountryCurrencyList, CountrySymbolList
        TempSymbolCountryMap = {}
        CountryCurrencyList = []
        CountrySymbolList = []
        response = requests.get("http://data.fixer.io/api/symbols?access_key=2f0778901994907d0c")
        JSON = response.json()
        if JSON.get("success") == True:
            for code in JSON.get("symbols").keys():
                Country = JSON.get("symbols").get(code)
                self.CurrencyCodes[Country] = code
                TempSymbolCountryMap[code] = Country
                self.store.put(code, Country=Country, symbols=code)
                CountrySymbolList.append(code)
                CountryCurrencyList.append(Country)
        responseBaseCurrency = requests.get(f"http://data.fixer.io/api/latest?access_key=2f0778901994907d0c")
        JSONBC = responseBaseCurrency.json()
        if JSONBC.get("success") == True:
            for rateCode in JSONBC.get("rates").keys():
                self.store.put(rateCode,Country=TempSymbolCountryMap.get(rateCode),Rate=JSONBC.get("rates").get(rateCode),symbols=rateCode)
            self.store.put("LastUpdated", time=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def LoadSymbols(self):
        global CountryCurrencyList, CountrySymbolList
        CountryCurrencyList = []
        CountrySymbolList = []
        CountrySymbols = 0
        if self.store.count() > 0:
            if self.store.exists("INR"):
                keys = self.store.keys()
                CountrySymbols = keys
                CountrySymbols.remove("LastUpdated")
            for code in CountrySymbols:
                CountrySymbolList.append(code)
                CountryCurrencyList.append(self.store.get(code).get("Country"))


if __name__ == "__main__":
    CurrencyConverter().run()
