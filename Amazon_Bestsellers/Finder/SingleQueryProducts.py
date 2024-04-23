import json
from time import sleep
import requests

from Utils.Config import Config
from Utils.Utils import Utils


class Keepa:
    def __init__(self, access_token, domainId):
        self.access_token = access_token
        self.domainId = domainId

    def get_product_data(self, product_code):
        product_code_list_string = ','.join(str(num) for num in product_code)
        if len(product_code[0]) > 11:
            url = f"https://api.keepa.com/product?key={self.access_token}&domain={self.domainId}&code={product_code_list_string}&&stats=60"
        else:
            # url = f"https://api.keepa.com/product?key={self.access_token}&domain={self.domainId}&asin={product_code_list_string}&stats=60"
            url = f"https://api.keepa.com/product?key={self.access_token}&domain={self.domainId}&asin={product_code_list_string}&stats=60&buybox=1"
        try:
            print("Wysyłam zapytanie")
            response = requests.get(url)
            data = json.loads(response.content)
            try:
                return data["products"]
            except:
                print(data)
                if self.is_limit_reached(data):
                    self.get_product_data(product_code)
                else:
                    print(f"Produkt jest nieprawidłowy: {product_code}")
                return []
        except:

            return []



    def is_limit_reached(self, data):
        if data["tokensLeft"] > 0:
            return False
        else:
            print("Za mało tokenów")
            sleep(60)
            return True

    def get_products(self, json_data):
        encoded_json = json.dumps(json_data)
        url = f"https://api.keepa.com/query?key={self.access_token}&domain={self.domainId}&selection={encoded_json}"
        response = requests.get(url)
        data = json.loads(response.content)
        with open("single.txt", "r") as file:
            existing_asin = set(line.strip() for line in file)
        existing_asin_set = set(existing_asin)
        data_asin_set = set(data["asinList"])
        existing_asin_set.update(data_asin_set)
        with open("single.txt", "w") as file:
            for asin in existing_asin_set:
                file.write(asin + "\n")

        return data

    def product_finder(self):
            json_data = {
    "monthlySold_gte": 49,
    "brand": [
        "rituals"
    ],
    "sort": [
        [
            "current_SALES",
            "asc"
        ]
    ],
    "productType": [
        0,
        1
    ],
    "perPage": 500,
    "page": 0
}

            data = self.get_products(json_data)
            print(f"Total: {data['totalResults']}")

            tokensRefill = (600 - data['tokensLeft']) / 20 * 60
            if tokensRefill>0:
                sleep(tokensRefill)




config = Config()
utils = Utils()
keepa = Keepa(config.get_token(), config.get_domain_id())
keepa.product_finder()