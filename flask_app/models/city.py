from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class City:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.country_code = data['country_code']
        self.district = data['district']
        self.population = data['population']

    @classmethod
    def get_city_id(cls, data):
        query = "SELECT * FROM cities WHERE name = %(name)s;"
        city = connectToMySQL('world').query_db(query, data)
        return city[0]['id']