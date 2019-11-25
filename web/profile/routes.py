from flask import Blueprint, render_template

profile = Blueprint('profile', __name__)

@profile.route('/api/users', methods=['GET'])
def show_all_profile():
    pass 

@profile.route('/api/profile', methods=['GET'])
def current_user_profile_controller():
    pass

@profile.route('/api/profile/<user_id>', methods=['GET'])
def profile_controller(id):
    pass

@profile.route('/api/profile/edit', methods=['POST'])
def edit_profile_controller():
    pass





@profile.route('/profile', methods=['POST', 'GET'])
def current_user_profile():
    return render_template('profile.html')

@profile.route('/profile/<user_id>', methods=['POST', 'GET'])
def user_profile(user_id):
    return render_template('user_profile.html')

@profile.route('/api/profile', methods=['POST', 'GET'])
def edit_profile():
    return render_template('edit_profile.html')