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


    @staticmethod
    def continent_sorter(country):
        if country.continent.lower() == 'europe':
            return 'europe'
        elif country.continent.lower() == 'asia':
            return 'asia'
        elif country.continent.lower() == 'africa':
            return 'africa'
        elif country.continent.lower() == 'north america':
            return 'north_america'
        elif country.continent.lower() == 'south america':
            return 'south_america'
        else:
            return 'oceania'

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM countries LEFT JOIN country_languages ON code = country_code LEFT JOIN cities ON capital = cities.id;"
        countries = connectToMySQL('world').query_db(query)
        cls_countries = {
            'europe': [],
            'asia': [],
            'africa': [],
            'north_america': [],
            'south_america': [],
            'oceania': []
        }
        last_country_added = None
        first_country = countries.pop(0)
        continent = Country.continent_sorter(Country(first_country))
        last_country_added = Country(first_country)
        cls_countries[continent].append(Country(first_country))
        cls_countries[continent][-1].languages.append(Language(first_country))
        city_data = {
            'id': first_country['cities.id'],
            'name': first_country['cities.name'],
            'country_code': first_country['cities.country_code'],
            'district': first_country['district'],
            'population': first_country['cities.population']
        }
        cls_countries[continent][-1].capital = City(city_data)
        for country in countries:
            if last_country_added.code != country['code']:
                continent = Country.continent_sorter(Country(country))
                last_country_added = Country(country)
                cls_countries[continent].append(Country(country))
                cls_countries[continent][-1].languages.append(Language(country))
                city_data = {
                    'id': country['cities.id'],
                    'name': country['cities.name'],
                    'country_code': country['cities.country_code'],
                    'district': country['district'],
                    'population': country['cities.population']
                }
                cls_countries[continent][-1].capital = City(city_data)
            else:
                continent = Country.continent_sorter(Country(country))
                last_country_added = Country(country)
                cls_countries[continent][-1].languages.append(Language(country))
        return cls_countries

    @classmethod
    def get_one_continent(cls, data):
        query = "SELECT * FROM countries LEFT JOIN country_languages ON code = country_code LEFT JOIN cities ON capital = cities.id WHERE continent = %(continent)s;"
        continent_countries_db = connectToMySQL('world').query_db(query, data)
        continent_countries_cls = []
        continent_countries_cls.append(Country(continent_countries_db[0]))
        continent_countries_cls[-1].languages.append(Language(continent_countries_db[0]))
        city_data = {
            'id': continent_countries_db[0]['cities.id'],
            'name': continent_countries_db[0]['cities.name'],
            'country_code': continent_countries_db[0]['cities.country_code'],
            'district': continent_countries_db[0]['district'],
            'population': continent_countries_db[0]['cities.population']
        }
        continent_countries_cls[-1].capital = City(city_data)
        continent_countries_db.pop(0)
        for country in continent_countries_db:
            if continent_countries_cls[-1].code != country['code']:
                continent_countries_cls.append(Country(country))
                continent_countries_cls[-1].languages.append(Language(country))
                city_data = {
                    'id': country['cities.id'],
                    'name': country['cities.name'],
                    'country_code': country['cities.country_code'],
                    'district': country['district'],
                    'population': country['cities.population']
                }
                continent_countries_cls[-1].capital = City(city_data)
            else:
                continent_countries_cls[-1].languages.append(Language(country))
        return continent_countries_cls

    @classmethod
    def get_country_code(cls, data):
        query = "SELECT * FROM countries LEFT JOIN country_languages ON code = country_code LEFT JOIN cities ON capital = cities.id WHERE code = %(code)s;"
        country = connectToMySQL('world').query_db(query, data)
        if not country:
            return country
        country_cls = Country(country[0])
        country_cls.languages.append(Language(country[0]))
        city_data = {
            'id': country[0]['cities.id'],
            'name': country[0]['cities.name'],
            'country_code': country[0]['cities.country_code'],
            'district': country[0]['district'],
            'population': country[0]['cities.population']
        }
        country_cls.capital = City(city_data)
        country.pop(0)
        if len(country) > 0:
            for inst in country:
                country_cls.languages.append(Language(inst))
        return country_cls

    @classmethod
    def get_country_name(cls, data):
        query = "SELECT * FROM countries LEFT JOIN country_languages ON code = country_code LEFT JOIN cities ON capital = cities.id WHERE countries.name = %(name)s;"
        country = connectToMySQL('world').query_db(query, data)
        if not country:
            return country
        country_cls = Country(country[0])
        country_cls.languages.append(Language(country[0]))
        city_data = {
            'id': country[0]['cities.id'],
            'name': country[0]['cities.name'],
            'country_code': country[0]['cities.country_code'],
            'district': country[0]['district'],
            'population': country[0]['cities.population']
        }
        country_cls.capital = City(city_data)
        country.pop(0)
        if len(country) > 0:
            for inst in country:
                country_cls.languages.append(Language(inst))
        return country_cls

    @classmethod
    def add_report(cls, data):
        query =''' 
        INSERT INTO reported_issues_country 
        (code, continent, region, surface_area, indep_year, population, life_expectancy, gnp, gnp_old, local_name, government_form, head_of_state, capital, code2) 
        VALUES (%(code)s, %(continent)s, %(region)s, %(surface_area)s, %(indep_year)s, %(population)s, %(life_expectancy)s, %(gnp)s, %(gnp_old)s, %(local_name)s, %(government_form)s, %(head_of_state)s, %(capital)s, %(code2)s);
        '''
        report_id = connectToMySQL('world').query_db(query, data)
        return