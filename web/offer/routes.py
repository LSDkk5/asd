from flask import Blueprint, render_template


offers = Blueprint('offers', __name__)

@offers.route('/offer/list', methods=['POST', 'GET'])
def offer_lists():
    return render_template('offers.html')

@offers.route('/offer/add', methods=['POST', 'GET'])
def add_offer():
    return render_template('add-offer.html')

@offers.route('/offer/del/<offer_id>', methods=['POST', 'GET'])
def del_offer(offer_id):
    return render_template('del-offer.html')

@offers.route('/offer/edit/<offer_id>', methods=['POST', 'GET'])
def edit_offer(offer_id):
    return render_template('edit-offer.html')

@offers.route('/offer/details/<offer_id>', methods=['POST', 'GET'])
def offer_details(offer_id):
    return render_template('offer-details.html')