from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
@home.route('/home', methods=['GET'])
@home.route('/index', methods=['GET'])
def home_page():
    return render_template('home.html')

@home.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html')

@home.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@home.route('/afterregister', methods=['GET'])
def first_login():
    return render_template('afterRegister.html')

@home.route('/cookies', methods=['GET'])
def cookies():
    return render_template('cookies.html')

@home.route('/cooperation', methods=['GET'])
def cooperation():
    return render_template('cooperation.html')

@home.route('/rules', methods=['GET'])
def rules():
    return render_template('rules.html')

@home.route('/forinvestors', methods=['GET'])
def for_investors():
    return render_template('forInvestors.html')

@home.route('/formedias', methods=['GET'])
def for_medias():
    return render_template('forMedias.html')

@home.route('/offers', methods=['GET'])
def offers():
    return render_template('offers.html')