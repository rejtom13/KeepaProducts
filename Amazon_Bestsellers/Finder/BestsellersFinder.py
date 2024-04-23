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
        with open("/Users/tom.rejmer/PycharmProjects/Storage/Amazon_Bestsellers/asin.txt", "r") as file:
            existing_asin = set(line.strip() for line in file)
        existing_asin_set = set(existing_asin)
        data_asin_set = set(data["asinList"])
        existing_asin_set.update(data_asin_set)
        with open("/Users/tom.rejmer/PycharmProjects/Storage/Amazon_Bestsellers/asin.txt", "w") as file:
            for asin in existing_asin_set:
                file.write(asin + "\n")

        return data

    def product_finder(self):
        rules_list = [
            [12, 12.8, False],
            [12.8, 13, True],
            [13, 13.7, False],
            [13.7, 14, True],
            [14, 14.5, False],
            [14.5, 14.95, False],
            [14.95, 15, True],
            [15, 15.5, False],
            [15.5, 16, True],
            [16, 16.5, False],
            [16.5, 17, True],
            [17, 17.5, False],
            [17.5, 18, True],
            [18, 19, True],
            [19, 19.6, False],
            [19.6, 19.98, False],
            [19.98, 20, True],
            [20, 21, True],
            [21, 22, True],
            [22, 23, True],
            [23, 24, False],
            [24, 25, True],
            [25, 26, False],
            [26, 27, False],
            [27, 28, False],
            [28, 29, False],
            [29, 30, True],
            [30, 32, False],
            [32, 34, False],
            [34, 36, True],
            [36, 38, False],
            [38, 40, True],
            [40, 44, False],
            [44, 49, False],
            [49, 55, True],
            [55, 63, False],
            [63, 76, False],
            [76, 96, False],
            [96, 140, False],
            [140, 3000, True]

        ]
        rating = 44
        for elem in rules_list:
            if elem[2]:
                json_data = {
                                    "monthlySold_gte": 49,
                                    "current_RATING_lte": rating,
                                    "current_NEW_gte": elem[0]*100,
                                    "current_NEW_lte": (elem[1])*100,
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
                                    "perPage": 10000,
                                    "page": 0
                                }
                data = self.get_products(json_data)
                print(f"Min: {elem[0]}, Max: {elem[1]}, Rating min: {rating} Total: {data['totalResults']}")

                json_data = {
                                    "monthlySold_gte": 49,
                                    "current_RATING_gte": rating,
                                    "current_NEW_gte": elem[0]*100,
                                    "current_NEW_lte": (elem[1])*100,
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
                                    "perPage": 10000,
                                    "page": 0
                                }
                data = self.get_products(json_data)
                print(f"Min: {elem[0]}, Max: {elem[1]}, Rating max: {rating} Total: {data['totalResults']}")
            else:
                json_data = {
                                    "monthlySold_gte": 49,
                                    "current_NEW_gte": elem[0]*100,
                                    "current_NEW_lte": (elem[1])*100,
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
                                    "perPage": 10000,
                                    "page": 0
                                }
                data = self.get_products(json_data)
                print(f"Min: {elem[0]}, Max: {elem[1]}, Total: {data['totalResults']}")
            tokensRefill = (600 - data['tokensLeft']) / 20 * 60
            if tokensRefill>0:
                sleep(tokensRefill)




config = Config()
utils = Utils()
keepa = Keepa(config.get_token(), config.get_domain_id())
keepa.product_finder()