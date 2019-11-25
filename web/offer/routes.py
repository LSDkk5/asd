from flask import Blueprint, render_template


offers = Blueprint('offers', __name__)

@offers.route('/api/offers', methods=['GET'])
def show_all_offers():
    pass 

@offers.route('/api/offers/add', methods=['GET'])
def add_offer_controller():
    pass

@offers.route('/api/offer/delete/<offer_id>', methods=['GET'])
def delete_offer_controller(offer_id):
    pass

@offers.route('/api/offer/<offer_id>', methods=['GET'])
def offer_detail(offer_id):
    pass

@offers.route('/api/offer/edit/<offer_id>', methods=['POST'])
def edit_offer_controller(offer_id):
    pass





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