from flask import Blueprint, render_template, request, flash
from .model import Outbreaks, Search
from flask_login import login_required, current_user
from . import db
from flask import redirect, url_for

# With the Flask app and db created
# from your_flask_app import db

# Define that this file is the blueprint of the application that has a bunch of roots inside of it
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')

        # Redirect to the results page with the search query
        return redirect(url_for('views.results', search_query=search_query))

    # Handle other cases as needed
    return redirect(url_for('views.home'))


@views.route('/results/<search_query>')
def results(search_query):
    # fetch relevant data from the database

    outbreaks = Outbreaks.query.filter(Outbreaks.Country.ilike(f'%{search_query}%')).all()

    # Create a new search entry in the database
    if current_user.is_authenticated:
        new_search = Search(user_id=current_user.id, country=search_query, year=0)  # Set year to 0 for now
        db.session.add(new_search)
        db.session.commit()

        # Retrieve user's search history
        search_history = current_user.get_search_history()

    return render_template('results.html', outbreaks=outbreaks)


@views.route('/visualization/<int:outbreak_id>')
def visualization(outbreak_id):
    # Fetch the outbreak based on the provided outbreak_id
    outbreak = Outbreaks.query.get_or_404(outbreak_id)

    # Extract years and occurrences for the selected country and disease
    years = [entry.Year for entry in
             Outbreaks.query.filter_by(Country=outbreak.Country, Disease=outbreak.Disease).order_by(Outbreaks.Year)]
    occurrences = [entry.DONs for entry in
                   Outbreaks.query.filter_by(Country=outbreak.Country, Disease=outbreak.Disease).order_by(
                       Outbreaks.Year)]

    return render_template('visualization.html', outbreak=outbreak, years=years, occurrences=occurrences)


# Add this route to views.py
@views.route('/search-history')
@login_required
def search_history():
    # Retrieve user's search history
    search_history = current_user.get_search_history()
    return render_template('search_history.html', search_history=search_history)

# @views.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         # If the form is submitted (POST request), retrieve values from the form
#         country = request.form.get('country')
#         year = request.form.get('year')
#
#         # Call the function to get disease outbreaks for the specified country and year
#         outbreaks = get_outbreaks_by_country_and_year(country, int(year))
#
#         # Render the results.html template with the obtained outbreaks
#         return render_template('results.html', outbreaks=outbreaks)
#
#     # If the method is not POST, render the search.html template
#     return render_template('search.html')
