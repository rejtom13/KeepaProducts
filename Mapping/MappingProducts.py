from Suppliers.Storage import Storage
from Suppliers.SupplierFile import SupplierFile
from Utils.Config import Config
from Utils.DbConnection import DbConnection
from Utils.Utils import Utils
from Suppliers.Storage import Storage
class MappingProducts:
    # def __init__(self, cursor):
    #     self.amazon_bestsellers_product_list = []
    #     self.storage_product_list = []
    #     self.mapped_products = []
    #     self.index = []
    #     self.get_amazon_bestsellers_products(cursor)
    #     self.get_storage_products(cursor)
    #     self.get_mapped_products(cursor)
    #     self.convert_mapped_products_list_to_tuple()

    def __init__(self, cursor, supplier=None):
        self.amazon_bestsellers_product_list = []
        self.storage_product_list = []
        self.mapped_products = []
        self.index = []
        self.get_amazon_bestsellers_products(cursor)
        self.get_storage_products(cursor, supplier)
        self.get_mapped_products(cursor)
        self.convert_mapped_products_list_to_tuple()

    def get_amazon_bestsellers_products(self, cursor):
        cursor.execute("Select asin, ean from amazon_bestsellers")
        self.amazon_bestsellers_product_list = [[str(asin), str(ean)] for asin, ean in cursor.fetchall()]

    def get_storage_products(self, cursor, supplier=None):
        if supplier is not None:
            cursor.execute(f"Select supplier, ean from storage where supplier ='{supplier}'")
            self.storage_product_list = [[str(supplier), str(ean)] for supplier, ean in cursor.fetchall()]
        else:
            cursor.execute("Select supplier, ean from storage")
            self.storage_product_list = [[str(supplier), str(ean)] for supplier, ean in cursor.fetchall()]



    def check_if_ean_is_available_in_storage(self, ean):
        try:
            self.index = [index for index, row in enumerate(self.storage_product_list) if row[1] == ean]
            return self.index
        except:
            self.index = -1
            return self.index

    def get_mapped_products(self, cursor):
        cursor.execute("Select supplier, ean, asin from mapping")
        self.mapped_products = [[str(supplier), str(ean), str(asin)] for supplier, ean, asin in cursor.fetchall()]

    def convert_mapped_products_list_to_tuple(self):
        return set(tuple(row) for row in self.mapped_products)

    def check_if_product_mapped(self, supplier, ean, asin):
        if [supplier, ean, asin] in self.mapped_products:
            return True
        else:
            return False

    def mapping_supplier(self, db):
        for i in range(len(self.amazon_bestsellers_product_list)):
            if len(self.check_if_ean_is_available_in_storage(self.amazon_bestsellers_product_list[i][1]))>0:
                for index in self.index:
                    if not self.check_if_product_mapped(self.storage_product_list[index][0],self.storage_product_list[index][1], self.amazon_bestsellers_product_list[i][0]):
                        self.prepare_add_query(self.storage_product_list[index][0],
                                            self.storage_product_list[index][1],
                                            self.amazon_bestsellers_product_list[i][0],
                                            db.cursor)
                        db.increase_counter()
                        db.commit_transaction_if_more_than_100()
                        print(f"Zmapowano product EAN: {self.amazon_bestsellers_product_list[i][1]}, ASIN: {self.amazon_bestsellers_product_list[i][0]}")
                    else:
                        print(f"Produkt zmapowany EAN: {self.amazon_bestsellers_product_list[i][1]}")
        db.commit_transaction()

    def prepare_add_query(self, supplier, ean, asin, cursor):
        self.data_product = {
            'supplier': supplier,
            'ean': ean,
            'asin': asin
        }

        self.query = (
            "INSERT INTO mapping (supplier,ean,asin)"
            "VALUES (%(supplier)s,%(ean)s, %(asin)s)")
        cursor.execute(self.query, self.data_product)




def main():
    config = Config()
    db = DbConnection(config.db_user_name, config.db_password, config.db_host, config.db_name)
    m = MappingProducts(db.cursor)
    for i in range(len(m.amazon_bestsellers_product_list)):
        if len(m.check_if_ean_is_available_in_storage(m.amazon_bestsellers_product_list[i][1]))>0:
            for index in m.index:
                if not m.check_if_product_mapped(m.storage_product_list[index][0],m.storage_product_list[index][1], m.amazon_bestsellers_product_list[i][0]):
                    m.prepare_add_query(m.storage_product_list[index][0],
                                        m.storage_product_list[index][1],
                                        m.amazon_bestsellers_product_list[i][0],
                                        db.cursor)
                    db.increase_counter()
                    db.commit_transaction_if_more_than_100()
                    print(f"Zmapowano product EAN: {m.amazon_bestsellers_product_list[i][1]}, ASIN: {m.amazon_bestsellers_product_list[i][0]}")
                else:
                    print(f"Produkt zmapowany EAN: {m.amazon_bestsellers_product_list[i][1]}")
        else:
            print(f"Brak produktu: {m.amazon_bestsellers_product_list[i][1]} w bazie")
    db.commit_transaction()

if __name__ == "__main__":
    main()

