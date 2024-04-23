import time
from datetime import datetime


class Product:

    def __init__(self, ean, data):
        self.ean = ean
        self.domainId = data["domainId"]
        self.asin = ""
        self.mpn = ""
        self.name = "" #git
        self.brand = "" #git
        self.category = "" #git
        self.categoryId = 0
        self.numberOfItems = 0 #git
        self.fbaFee = 0.00
        self.referralFeePercent = 0#git
        self.salesRank = 0#git
        self.amazonPrice = 0.00#git
        self.salesRankParameter = 0.00 #nie wiem na razie
        self.amazonAvailabilityPercent = 0.0 #git
        self.countNew = 0#git
        self.newPrice = 0.00
        self.fbmPrice = 0.00
        self.fbaPrice = 0.00
        self.buyBoxPrice = 0.00
        self.avgBuyBoxPrice = 0.00
        self.reviewsNumber = 0
        self.reviewsIncrease = 0
        self.maxCostVelAmazon = 0.00
        self.maxCostVelNew = 0.00
        self.maxCostVelBuybox = 0.00
        self.avgPrice = 0.00
        self.salesRankDrop30 = 0
        self.salesRankDrop90 = 0
        self.salesRankDrop180 = 0
        self.variations = 0
        self.monthlySold = 0
        self.image = ""
        self.lastUpdateDate = None
        self.set_name(data)
        self.set_mpn(data)
        self.set_asin(data)
        self.set_brand(data)
        self.set_fbaFees(data)
        self.set_categoryId(data)
        self.set_category(data)
        self.set_lastUpdateDate()
        self.set_numberOfItems(data)
        self.set_fbaFee(data)
        self.set_referralFeePercent(data)
        self.set_salesRank(data)
        self.set_amazonPrice(data)
        self.set_amazonAvailabilityPercent(data)
        self.set_countNew(data)
        self.set_newPrice(data)
        self.set_fbmPrice(data)
        self.set_fbaPrice(data)
        self.set_buyBoxPrice(data)
        self.set_avg_buyBox_price(data)
        self.set_reviewsNumber(data)
        self.set_reviewsIncrease(data)
        self.set_maxCostVelNew()
        self.set_maxCostVelAmazon()
        self.set_maxCostVelBuybox()
        self.set_average_price(data)
        self.set_salesDrop30(data)
        self.set_salesDrop90(data)
        self.set_salesDrop180(data)
        self.set_variations(data)
        self.set_monthlySold(data)
        self.set_image(data)

    def get_name(self):
        return self.name


    def set_name(self, data):
        try:
            self.name = data["title"]
        except:
            self.name = None

    def set_asin(self, data):
        try:
            self.asin = data["asin"]
        except:
            self.asin = 0

    def set_mpn(self, data):
        try:
            self.mpn = data["partNumber"]
        except:
            self.mpn = None

    def set_brand(self, data):
        try:
            self.brand = data["brand"]
        except:
            self.brand = None

    def set_fbaFees(self, data):
        try:
            self.fbaFees = data["fbaFees"]
        except:
            self.fbaFees = None

    def set_category(self, data):
        try:
            self.category = data["categoryTree"][0]["name"]
        except:
            self.category = None

    def set_categoryId(self, data):
        try:
            self.categoryId = data["categoryTree"][0]["catId"]
        except:
            self.categoryId = None

    def set_numberOfItems(self, data):
        try:
            self.numberOfItems = data["numberOfItems"]
        except:
            self.numberOfItems = -2

    def set_fbaFee(self, data):
        try:
            self.fbaFee = data["fbaFees"]["pickAndPackFee"]/100
        except:
            self.fbaFee = -2

    def set_referralFeePercent(self, data):
        try:
            self.referralFeePercent = data["referralFeePercent"]
        except:
            self.referralFeePercent = -2

    def set_salesRank(self, data):
        try:
            self.salesRank = data["csv"][3][-1]
        except:
            self.salesRank = -2

    def set_monthlySold(self, data):
        try:
            self.monthlySold = data["monthlySold"]
        except:
            self.monthlySold = 0


    def set_amazonPrice(self, data):
        try:
            self.amazonPrice = data["csv"][0][-1]/100
        except:
            self.amazonPrice = -2

    def set_amazonAvailabilityPercent(self, data):
        try:
            self.amazonAvailabilityPercent = 100-data["csv"][0].count(-1)/(len(data["csv"][0])/2)*100
        except:
            self.amazonAvailabilityPercent = -2

    def set_countNew(self, data):
        try:
            self.countNew = data["stats"]["totalOfferCount"]
        except:
            self.countNew = -2

    def set_newPrice(self, data):
        try:
            self.newPrice = data["csv"][1][-1]/100
        except:
            self.newPrice = -2

    def set_fbmPrice(self, data):
        try:
            self.fbmPrice = data["csv"][7][-1]/100
        except:
            self.fbmPrice = -2

    def set_fbaPrice(self, data):
        try:
            self.fbaPrice = data["csv"][10][-1]/100
        except:
            self.fbaPrice = -2

    def set_buyBoxPrice(self, data):
        try:
            self.buyBoxPrice = float(data["stats"]["buyBoxPrice"])/100 + float(data["stats"]["buyBoxShipping"])/100
        except:
            self.buyBoxPrice = self.newPrice

    def calculate_buybox_average(self, data):
        result = []
        current_set = []
        for item in data:
            current_set.append(item)
            if len(current_set) == 3:
                time, price, shipcost = current_set
                current_unix_time = int(datetime.utcnow().timestamp())
                if price > 0 and price < 368110 and (current_unix_time / 60 - 21564000 - 24 * 60 * 30) < time:
                    result.append(price + shipcost)
                current_set = []
        if result:
            average = round(sum(result) / len(result) / 100,2)

        else:
            average = -1
        return average

    def set_avg_buyBox_price(self, data):
        try:
            self.avgBuyBoxPrice = self.calculate_buybox_average(data["csv"][18])
        except:
            self.avgBuyBoxPrice = -1

    def set_reviewsNumber(self, data):
        try:
            self.reviewsNumber = data["csv"][17][-1]
        except:
            self.reviewsNumber = -2

    def set_reviewsIncrease(self, data):
        try:
            data_csv = data["csv"][17]
            current_unix_time = int(datetime.utcnow().timestamp())
            time_limit = current_unix_time / 60 - 21564000 - 24 * 60 * 30
            index = len(data_csv)-2
            while data_csv[index] > time_limit and index>0:
                index = index - 2
            self.reviewsIncrease = self.reviewsNumber-data_csv[index-1]
        except:
            self.reviewsIncrease = -1

    def set_maxCostVelNew(self):
        try:
            if self.newPrice>0:
                self.maxCostVelNew = round((self.newPrice*(1-self.referralFeePercent/100-19/119-0.0252)-self.fbaFee),2)
        except:
            self.maxCostVelNew = -2


    def set_maxCostVelBuybox(self):
            try:
                if self.buyBoxPrice > 0:
                    self.maxCostVelBuybox = round(
                        (self.buyBoxPrice * (1 - self.referralFeePercent / 100 - 19 / 119 - 0.0252) - self.fbaFee), 2)
            except:
                self.maxCostVelNew = self.maxCostVelNew

    def set_maxCostVelAmazon(self):
        try:
            if self.amazonPrice>0:
                self.maxCostVelAmazon = round((self.amazonPrice*(1-self.referralFeePercent/100-19/119-0.0252)-self.fbaFee),2)
        except:
            self.maxCostVelAmazon = -2

    def set_average_price(self, data):
        try:
            price_list = data["csv"][1]
            prices_sum, count = 0, 0
            for i in range(1, len(price_list), 2):
                if price_list[i]>0:
                    count +=1
                    prices_sum += price_list[i]
            self.avgPrice = round(prices_sum/count/100,2)
        except:
            self.avgPrice = -1

    def set_salesDrop30(self, data):
        try:
            self.salesRankDrop30 = data["stats"]["salesRankDrops30"]
        except:
            self.salesRankDrop30 = -1

    def set_salesDrop90(self, data):
        try:
            self.salesRankDrop90 = data["stats"]["salesRankDrops90"]
        except:
            self.salesRankDrop90 = -1


    def set_salesDrop180(self, data):
        try:
            self.salesRankDrop180 = data["stats"]["salesRankDrops180"]
        except:
            self.salesRankDrop180 = -1


    def set_variations(self, data):
        try:
            if data["variationCSV"] is not None:
                self.variations = len((data["variationCSV"]).strip('"').split(","))
            else:
                self.variations = 0
        except:
            self.variations = -1

    def set_image(self, data):
        try:
            csv_temp = (data['imagesCSV']).split(',')[0]
            self.image = f"https://images-na.ssl-images-amazon.com/images/I/{csv_temp}"
        except:
            self.image = ""

    def set_lastUpdateDate(self):
        self.lastUpdateDate = datetime.fromtimestamp(time.time())

    def get_lastUpdateDate(self):
        return self.lastUpdateDate

    def get_Qogito_list(self, cursor):
        cursor.execute('SELECT ean FROM zalando_products')
        ean_list =  [row[0] for row in cursor.fetchall()]
        return ean_list

    def prepare_add_query(self):
        self.data_product = {
            'ean': self.ean,
            'domainId': self.domainId,
            'mpn': self.mpn,
            'asin': self.asin,
            'name': self.name,
            'brand': self.brand,
            'categoryId': self.categoryId,
            'category': self.category,
            'numberOfItems': self.numberOfItems,
            'fbaFee': self.fbaFee,
            'referralFeePercent': self.referralFeePercent,
            'salesRank': self.salesRank,
            'amazonPrice': self.amazonPrice,
            'amazonAvailabilityPercent': self.amazonAvailabilityPercent,
            'totalOfferCount': self.countNew,
            'newPrice': self.newPrice,
            'fbmPrice': self.fbmPrice,
            'fbaPrice': self.fbaPrice,
            'buyBoxPrice': self.buyBoxPrice,
            'avgBuyBoxPrice': self.avgBuyBoxPrice,
            'reviewsNumber': self.reviewsNumber,
            'reviewsIncrease': self.reviewsIncrease,
            'maxCostVelBuybox': self.maxCostVelBuybox,
            'maxCostVelNew': self.maxCostVelNew,
            'maxCostVelAmazon': self.maxCostVelAmazon,
            'avgPrice': self.avgPrice,
            'SRDrop30': self.salesRankDrop30,
            'variations': self.variations,
            'image': self.image,
            'monthlySold': self.monthlySold,
            'lastUpdateDate': self.get_lastUpdateDate()
        }

        # self.query =  ("INSERT INTO ean_products "
        self.query =  ("INSERT INTO amazon_bestsellers "
                       "(ean, domainId, mpn, asin, name, brand, categoryId, category,numberOfItems, fbaFee,referralFeePercent, salesRank, monthlySold,"
                       "amazonPrice, amazonAvailabilityPercent, totalOfferCount, newPrice, fbmPrice"
                       ",fbaPrice, buyBoxPrice,avgBuyBoxPrice, reviewsNumber,reviewsIncrease,maxCostVelBuybox, maxCostVelAmazon, maxCostVelNew,avgPrice, "
                       "SRDrop30, variations, image, lastUpdateDate)"
                        "VALUES "
                       "(%(ean)s, %(domainId)s, %(mpn)s,%(asin)s, %(name)s, %(brand)s, %(categoryId)s, %(category)s,%(numberOfItems)s,"
                        "%(fbaFee)s, %(referralFeePercent)s, %(salesRank)s, %(monthlySold)s, %(amazonPrice)s, "
                        "%(amazonAvailabilityPercent)s, %(totalOfferCount)s, %(newPrice)s, %(fbmPrice)s, %(fbaPrice)s, "
                       "%(buyBoxPrice)s, %(avgBuyBoxPrice)s, %(reviewsNumber)s,%(reviewsIncrease)s, %(maxCostVelBuybox)s, %(maxCostVelAmazon)s,%(maxCostVelNew)s,%(avgPrice)s,"
                       "%(SRDrop30)s,%(variations)s,%(image)s,%(lastUpdateDate)s)")

    def prepare_update_query(self):
        self.data_product = {
            'ean': self.ean,
            'mpn': self.mpn,
            'name': self.name,
            'fbaFee': self.fbaFee,
            'referralFeePercent': self.referralFeePercent,
            'salesRank': self.salesRank,
            'monthlySold': self.monthlySold,
            'amazonPrice': self.amazonPrice,
            'amazonAvailabilityPercent': self.amazonAvailabilityPercent,
            'totalOfferCount': self.countNew,
            'newPrice': self.newPrice,
            'fbmPrice': self.fbmPrice,
            'fbaPrice': self.fbaPrice,
            'buyBoxPrice': self.buyBoxPrice,
            'avgBuyBoxPrice': self.avgBuyBoxPrice,
            'reviewsNumber': self.reviewsNumber,
            'reviewsIncrease': self.reviewsIncrease,
            'maxCostVelBuybox': self.maxCostVelBuybox,
            'maxCostVelNew': self.maxCostVelNew,
            'maxCostVelAmazon': self.maxCostVelAmazon,
            'avgPrice': self.avgPrice,
            'SRDrop30': self.salesRankDrop30,
            'variations': self.variations,
            'image': self.image,
            'lastUpdateDate': self.get_lastUpdateDate()

        }
        self.query = ("UPDATE amazon_bestsellers SET name = %(name)s, mpn = %(mpn)s, fbaFee = %(fbaFee)s, referralFeePercent = %(referralFeePercent)s, "
                      "salesRank = %(salesRank)s,monthlySold = %(monthlySold)s, "
                      "amazonPrice = %(amazonPrice)s, amazonAvailabilityPercent = %(amazonAvailabilityPercent)s, "
                      "totalOfferCount = %(totalOfferCount)s, newPrice = %(newPrice)s,fbmPrice = %(fbmPrice)s,"
                      "buyBoxPrice = %(buyBoxPrice)s,avgBuyBoxPrice = %(avgBuyBoxPrice)s,reviewsNumber = %(reviewsNumber)s,reviewsIncrease = %(reviewsIncrease)s,"
                      "maxCostVelAmazon = %(maxCostVelAmazon)s,maxCostVelNew = %(maxCostVelNew)s,maxCostVelBuybox = %(maxCostVelBuybox)s,"
                      "avgPrice = %(avgPrice)s,SRDrop30 = %(SRDrop30)s, variations = %(variations)s,image = %(image)s,lastUpdateDate = %(lastUpdateDate)s "
                      "WHERE ean = %(ean)s")


    def update_data_in_db(self, cursor, boolean):
        if boolean:
            print(f"Aktualizuję w bazie produkt EAN: {self.ean} ASIN: {self.asin}")
            self.prepare_update_query()
        else:
            print(f"Dodaję do bazy produkt EAN: {self.ean} ASIN: {self.asin}")
            self.prepare_add_query()
        cursor.execute(self.query, self.data_product)




