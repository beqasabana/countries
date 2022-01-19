from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Language:
    def __init__(self, data):
        self.id = data['id']
        self.country_code = data['country_code']
        self.language = data['language']
        if data['is_official'] == 'T':
            self.is_official = True
        else:
            self.is_official = False
        self.percentage = data['percentage']