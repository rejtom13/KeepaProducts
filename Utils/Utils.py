import requests
import json

class Utils:
    def __init__(self):
        self.exchange_rate = self.get_current_euro_rate()

    def read_asin_numbers(self):
        places = []
        with open('/Users/tom.rejmer/PycharmProjects/Storage/Amazon_products/asin.txt', 'r') as file:
            for line in file:
                curr_place = line[:-1]
                places.append(curr_place)
        return places

    def read_black_list(self):
        with open('/Users/tom.rejmer/PycharmProjects/Storage/blacklist.txt', 'r') as plik:
            places = [int(line.strip()) for line in plik]
        return places

    def get_unique_list(self, list1, list2, list3):
        unique_list = [element for element in list1 if element not in list2]
        unique_list = [element for element in unique_list if element not in list3]
        print(f"Do sprawdzenia pozostało {len(unique_list)}")
        return unique_list

    def get_unique_list_from_2(self, list1, list2):
        unique_list = [element for element in list1 if element not in list2]
        print(f"Do sprawdzenia pozostało {len(unique_list)}")
        return unique_list

    def update_asin_list(self, asin_list, i):
        with open('/Users/tom.rejmer/PycharmProjects/Storage/blacklist.txt', 'w') as filehandle:
            for listitem in asin_list[i:]:
                filehandle.write(f'{listitem}\n')

    def get_current_euro_rate(self):
        url = "https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json"
        response = requests.get(url)
        data = response.json()
        rate = data['rates'][0]['mid']
        return rate




    def send_discord_webhook(self, webhook_url, message):
        """
        Wysyła wiadomość na kanał Discord za pomocą webhooka.

        :param webhook_url: URL webhooka Discord
        :param message: Treść wiadomości do wysłania
        """
        payload = {
            'content': message
        }

        payload_json = json.dumps(payload)

        response = requests.post(webhook_url, data=payload_json, headers={'Content-Type': 'application/json'})
        if response.status_code < 299:
            print("Wiadomość została pomyślnie wysłana na kanał Discord.")
        else:
            print(f"Błąd podczas wysyłania wiadomości. Kod statusu: {response.status_code}")

