# import json
# import requests
#
# def cc_converter(exchange_rates, curr_amount, curr_name):
#     for curr, rate in exchange_rates.items():
#         result = round(rate * curr_amount,2)
#         print(f'I will get {result} {curr} from the sale of {curr_amount} {curr_name}.')
#
# def get_exchange_rates(curr_code, curr_code_to):
#
#     if curr_code!=curr_code_to:
#         rates_get = requests.get(f'http://www.floatrates.com/daily/{curr_code}.json')
#         rates_json = rates_get.text
#         rates = json.loads(rates_json)
#         return rates[curr_code_to]
#     else:
#         return {'code': curr_code, 'rate': 1}
#
#
#
# # conicoins_amount = int(input('Please, enter the number of conicoins you have:'))
# # cc_amount = float(input())
# # cc_dol_rate = float(input("Please, enter the exchange rate:"))
# # exchange_rates_cc = dict(
# # RUB = 2.98,
# # ARS = 0.82,
# # HNL = 0.17,
# # AUD = 1.9622,
# # MAD = 0.208)
#
# # cc_rub_rate = 2.98,
# # cc_ars_rate = 0.82,
# # cc_hnl_rate = 0.17,
# # cc_aus_rate = 1.9622,
# # cc_mad_rate = 0.208)
#
#
#
# # cc_converter(exchange_rates_cc, cc_amount, 'conicoins')
# # dollars_amount = conicoins_amount * cc_dol_rate
# # print(f'The total amount of dollars: {dollars_amount}')
#
# exchange_rates_dict = {}
# currency_possesed_code = input()
# exchange_rate_data = get_exchange_rates(currency_possesed_code, 'usd')
# exchange_rates_dict[exchange_rate_data['code'].lower()] = exchange_rate_data['rate']
#
# exchange_rate_data = get_exchange_rates(currency_possesed_code, 'eur')
# exchange_rates_dict[exchange_rate_data['code'].lower()] = exchange_rate_data['rate']
#
#
# while 1:
#     curr_choice_code = input()
#     if curr_choice_code =='':
#         break
#     curr_possesed_amount = float(input())
#     print("Checking the cache...")
#     try:
#         exchange_rate = exchange_rates_dict[curr_choice_code]
#     except KeyError:
#         print('Sorry, but it is not in the cache!')
#         exchange_rate_data = get_exchange_rates(currency_possesed_code, curr_choice_code)
#         exchange_rate = exchange_rate_data['rate']
#         exchange_rates_dict[exchange_rate_data['code'].lower()] = exchange_rate
#     else:
#         print("Oh! It is in the cache!")
#
#     received = curr_possesed_amount * exchange_rate
#     print(f'You Received {received} {curr_choice_code}')

import json
import requests

class Converter():

    def __init__(self, base_currency):
        self.base_curr_code = base_currency
        self.exchange_rates_dict = {}
        self.stop = 0
        self.getExchangeRates('usd')
        self.getExchangeRates('eur')

    def getExchangeRates(self, exchange_curr_code):
        if self.base_curr_code!=exchange_curr_code:
            rates_get = requests.get(f'http://www.floatrates.com/daily/{self.base_curr_code}.json')
            rates_json = rates_get.text
            rates = json.loads(rates_json)
            rates = rates[exchange_curr_code]
            self.exchange_rates_dict[rates['code'].lower()] = rates['rate']
        else:
            self.exchange_rates_dict[self.base_curr_code] = 1

    def exchange(self):
        exchange_curr_code = input()
        if not exchange_curr_code:
            self.stop = 1
            return None
        base_curr_amount = float(input())
        print("Checking the cache...")
        try:
            exchange_rate = self.exchange_rates_dict[exchange_curr_code]
        except KeyError:
            print('Sorry, but it is not in the cache!')
            self.getExchangeRates(exchange_curr_code)
        else:
            print("Oh! It is in the cache!")

        received = base_curr_amount * self.exchange_rates_dict[exchange_curr_code]
        print(f'You Received {received} {exchange_curr_code}')



def main():
    base_currency = input()
    my_converter = Converter(base_currency)

    while 1:
        if my_converter.stop == 1:
            break

        my_converter.exchange()



if __name__ == "__main__":
    main()