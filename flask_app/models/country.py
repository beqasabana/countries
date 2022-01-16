from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


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