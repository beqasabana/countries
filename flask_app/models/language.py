from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Language:
    def __init__(self, data):
        self.id = data['id']
        self.country_code = data['country_code']
        self.language = data['language']
        self.is_official = data['is_official']
        self.percentage = data['percentage']