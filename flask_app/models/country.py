from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.city import City
from flask_app.models.language import Language


class Country:
    def __init__(self, data):
        self.code = data['code']
        self.name = data['name']
        self.continent = data['continent']
        self.region = data['region'] 
        self.surface_area = data['surface_area']
        self.indep_year = data['indep_year']
        self.population = data['population']
        self.life_expectancy = data['life_expectancy']
        self.gnp = data['gnp']
        self.gnp_old = data['gnp_old']
        self.local_name = data['local_name']
        self.government_form = data['government_form']
        self.head_of_state = data['head_of_state']
        self.capital = data['capital']
        self.code2 = data['code2']
        self.capital = None
        self.languages = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM countries LEFT JOIN country_languages ON code = country_code LEFT JOIN cities ON capital = cities.id;"
        countries = connectToMySQL('world').query_db(query)
        print(countries[0])
        cls_countries = []
        for country in countries:
            if len(cls_countries) == 0:
                cls_countries.append(Country(country))
                cls_countries[-1].languages.append(Language(country))
                city_data = {
                    'id': country['cities.id'],
                    'name': country['cities.name'],
                    'country_code': country['cities.country_code'],
                    'district': country['district'],
                    'population': country['cities.population']
                }
                cls_countries[-1].capital = City(city_data)
            elif cls_countries[-1].code != country['code']:
                cls_countries.append(Country(country))
                cls_countries[-1].languages.append(Language(country))
                city_data = {
                    'id': country['cities.id'],
                    'name': country['cities.name'],
                    'country_code': country['cities.country_code'],
                    'district': country['district'],
                    'population': country['cities.population']
                }
                cls_countries[-1].capital = City(city_data)
            else:
                cls_countries[-1].languages.append(Language(country))
        return cls_countries