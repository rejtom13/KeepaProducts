class AmazonProductsList:
    def __init__(self, cursor):
        self.amazon_ean_in_db = self.get_amazon_ean_list(cursor);
        self.amazon_asin_in_db = self.get_amazon_asin_list(cursor);
        self.asin_blacklist = self.read_balck_list();

    def get_amazon_asin_list(self, cursor):
        cursor.execute('SELECT asin FROM amazon_bestsellers')
        asin_list =  [row[0] for row in cursor.fetchall()]
        return asin_list


    def read_asin_numbers(self):
        places = []
        with open('/Users/tom.rejmer/PycharmProjects/Storage/Amazon_Bestsellers/asin.txt', 'r') as file:
            for line in file:
                curr_place = line[:-1]
                places.append(curr_place)
        return places

    def get_amazon_ean_list(self, cursor):
        cursor.execute('SELECT ean FROM amazon_bestsellers')
        asin_list =  [row[0] for row in cursor.fetchall()]
        return asin_list

    def is_product_exist(self, ean):
        if ean in self.amazon_ean_in_db:
            return True
        else:
            return False

    def add_product_to_list(self, ena):
        if not self.is_product_exist(ena):
            self.amazon_ean_in_db.append(ena)

    def read_balck_list(self):
        with open('/Users/tom.rejmer/PycharmProjects/Storage/blacklist.txt', 'r') as plik:
            lista_id = [line.strip() for line in plik]
        return lista_id

    def add_product_to_black_list(self, ena):
        self.asin_blacklist.append(ena)
        with open('/Users/tom.rejmer/PycharmProjects/Storage/blacklist.txt', 'a') as file:
            file.write(ena+ "\n")