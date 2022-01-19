from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.country import Country


@app.route('/all/countries')
def display_all_countries():
    countries = Country.get_all()
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('all_countries.html', active_user=active_user, countries=countries)
    return render_template('all_countries.html', countries=countries)