import json


class Config:
    def __init__(self):
        with open('/Users/tom.rejmer/PycharmProjects/Keepa/data/config.json') as user_file:
            data = json.load(user_file)
        self.keepa_token = data["keepa_token"]
        self.iteration = data["iteration"]
        self.db_user_name = data["db"]["username"]
        self.db_password = data["db"]["password"]
        self.db_host = data["db"]["host"]
        self.db_name = data["db"]["db_name"]
        self.domain_id = data["domain_id"]
        self.qogita_email = data["qogita"]["email"]
        self.qogita_password = data["qogita"]["password"]
        self.webhook_url = data["webhook_url"]

    def get_token(self):
        return self.keepa_token

    def get_domain_id(self):
        return self.domain_id


