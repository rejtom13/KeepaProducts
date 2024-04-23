from sqlite3 import InterfaceError
from time import sleep, time

from Amazon_Bestsellers.Analyzer.Components.AmazonProductsList import AmazonProductsList
from Amazon_Bestsellers.Analyzer.Components.Keepa import Keepa
from Amazon_Bestsellers.Analyzer.Components.Product import Product
from Mapping.MappingProducts import MappingProducts
from Utils.Config import Config
from Utils.DbConnection import DbConnection
from Utils.Utils import Utils


def main():
    config = Config()
    utils = Utils()
    db = DbConnection(config.db_user_name, config.db_password, config.db_host, config.db_name)
    keepa = Keepa(config.get_token(), config.get_domain_id())
    a = AmazonProductsList(db.cursor)
    m = MappingProducts(db.cursor)
    asin_list = a.read_asin_numbers()
    print(len(asin_list))
    asin_list = utils.get_unique_list_from_2(asin_list,a.asin_blacklist)
    asin_list = utils.get_unique_list_from_2(asin_list, a.amazon_asin_in_db)
    for i in range(0, len(asin_list), config.iteration):
        start_time = time()
        product_asin = asin_list[i:i+config.iteration]
        print(f"Sprawdzam produkt: {product_asin}")
        data = keepa.get_product_data(product_asin)
        for i in range(len(data)):
            if data[i]["eanList"] is not None:
                for ean in data[i]["eanList"]:
                    p = Product(ean, data[i])
                    p.update_data_in_db(db.cursor, a.is_product_exist(ean))
                    a.add_product_to_list(ean)
                    db.increase_counter()
                    if len(m.check_if_ean_is_available_in_storage(ean)) > 0:
                        for index in m.index:
                            if not m.check_if_product_mapped(m.storage_product_list[index][0],
                                                             m.storage_product_list[index][1],
                                                             p.asin):
                                m.prepare_add_query(m.storage_product_list[index][0],
                                                    m.storage_product_list[index][1],
                                                    p.asin,
                                                    db.cursor)
                                print(
                                    f"Zmapowano product EAN: {p.ean}, ASIN: {p.asin}")
                            else:
                                print(f"Produkt zmapowany EAN: {p.ean}")
                db.commit_transaction_if_more_than_100()
            else:
                try:
                    a.add_product_to_black_list(data[i]["asin"])
                    print(f"Brak listy EAN dla produktu: {data[i]['asin']}")
                except:
                    continue

        diff_time = time()-start_time
        print(f"Proces sprawdzenia produktów trwał: {round(diff_time,2)}")
        if keepa.tokensRefill-diff_time>0:
            sleep(keepa.tokensRefill-diff_time)
    db.commit_transaction()
    db.close_connection()
    utils.send_discord_webhook(config.webhook_url, "Zakończono sprawdzanie bestsellerów")


if __name__ == "__main__":
    try:
        main()
    except:
        print("Wystąpił jakiś błąd")
        main()