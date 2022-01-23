from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.country import Country


@app.route('/allcountries')
def display_all_countries():
    countries = Country.get_all()
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('all_countries.html', active_user=active_user, all_countries=countries)
    return render_template('all_countries.html', all_countries=countries)

@app.route('/continent/<string:continent>')
def display_continent(continent):
    print(continent)
    data = {
        'continent': ' '.join(continent.split('-'))
    }
    continent_countries = Country.get_one_continent(data)
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('one_continent.html', all_countries=continent_countries, active_user=active_user)
    return render_template('one_continent.html', all_countries=continent_countries)

@app.route('/country/<string:country_name>/<string:country_code>')
def one_country(country_name, country_code):
    data = {
        'code': country_code
    }
    country = Country.get_country_code(data)
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('one_country.html', active_user=active_user, country=country)
    return render_template('one_country.html', country)

@app.route('/report/<string:country_name>/<string:country_code>')
def display_report_country(country_name, country_code):
    data = {
        'code': country_code
    }
    country = Country.get_country_code(data)
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('edit_country.html', active_user=active_user, country=country)
    return render_template('edit_country.html', country)