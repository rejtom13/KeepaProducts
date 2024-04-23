import json
from time import sleep

import requests


class Keepa:

    def __init__(self, access_token, domainId):
        self.access_token = access_token
        self.domainId = domainId
        self.tokensRefill = 0

    def get_product_data(self, product_code):
        product_code_list_string = ','.join(str(num) for num in product_code)
        if len(product_code[0]) > 11:
            url = f"https://api.keepa.com/product?key={self.access_token}&domain={self.domainId}&code={product_code_list_string}&stats=30&buybox=1"
        else:
            url = f"https://api.keepa.com/product?key={self.access_token}&domain={self.domainId}&asin={product_code_list_string}&stats=60&buybox=1&rating=1"
        print(url)
        try:
            print("Wysyłam zapytanie")
            response = requests.get(url)
            data = json.loads(response.content)
            self.tokensRefill = (600 - data['tokensLeft'])/20*60
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
    #
    # def product_finder(self):
    #     with open('Keepa/data/keepa_query.json') as user_file:
    #         json_string = user_file.read()
    #     encoded_json = urllib.parse.quote(json_string)
    #     url = f"https://api.keepa.com/query?key={self.access_token}&domain={self.domainId}&selection={encoded_json}"
    #     response = requests.get(url)
    #     data = json.loads(response.content)
    #     try:
    #         with open("Keepa/data/product_finder_results.txt", "w") as file:
    #             file.writelines("\n".join(data["asinList"]))
    #     except:
    #         print(data)
