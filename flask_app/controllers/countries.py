from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.country import Country
from flask_app.models.city import City


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
    return render_template('one_country.html', country=country)

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
    return render_template('edit_country.html', country=country)

@app.route('/report/country', methods=['POST'])
def report_country():
    data = {
        'code': request.form['code']
    }
    country = Country.get_country_code(data)
    city_name = {
        'name': request.form['capital']
    }
    report_data = {
        'code': request.form['code'],
        'name': request.form['name'],
        'continent': request.form['continent'],
        'region': request.form['region'],
        'surface_area': request.form['surface_area'],
        'indep_year': request.form['indep_year'],
        'population': request.form['population'],
        'life_expectancy': request.form['life_expectancy'],
        'gnp': request.form['gnp'],
        'gnp_old': request.form['gnp_old'],
        'local_name': request.form['local_name'],
        'government_form': request.form['government_form'],
        'head_of_state': request.form['head_of_state'],
        'capital': City.get_city_id(city_name),
        'code2': request.form['code2']
    }
    for key in report_data:
        if report_data[key] == 'None':
            report_data[key] = None
    report_id = Country.add_report(report_data)
    return redirect('/country/' + country.name + '/' + country.code)

@app.route('/search', methods=['POST'])
def search():
    continents = ('europe', 'asia', 'africa', 'north america', 'south america', 'oceania', 'antarctica')
    if request.form['search_term'].lower() in continents:
        data = {
            'continent': request.form['search_term']
        }
        return redirect(f"/continent/{request.form['search_term'].lower()}")
    data = {
            'name': request.form['search_term']
        }
    country = Country.get_country_name(data)
    if not country:
        return redirect('/')
    return redirect(f"/country/{country.name}/{country.code}")