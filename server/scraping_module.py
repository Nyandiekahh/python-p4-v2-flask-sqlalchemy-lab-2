import requests
from bs4 import BeautifulSoup
from models import db, Customer, Item, Review

def scrape_data():
    url = 'https://www.instagram.com/'  # Replace with the URL you want to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example scraping logic
    customers_data = []
    items_data = []
    reviews_data = []

    # Scrape customer data (modify the selectors based on actual HTML structure)
    for customer_item in soup.select('.customer-class'):  # Replace with actual class or tag
        name = customer_item.select_one('.name-class').text
        customers_data.append({'name': name})
    
    # Scrape item data
    for item_item in soup.select('.item-class'):  # Replace with actual class or tag
        name = item_item.select_one('.name-class').text
        price = float(item_item.select_one('.price-class').text.strip('$'))  # Adjust based on actual format
        items_data.append({'name': name, 'price': price})

    # Scrape review data
    for review_item in soup.select('.review-class'):  # Replace with actual class or tag
        comment = review_item.select_one('.comment-class').text
        # Assuming customer_id and item_id are derived somehow, here we use placeholder values
        customer_id = 1
        item_id = 1
        reviews_data.append({'comment': comment, 'customer_id': customer_id, 'item_id': item_id})

    return {
        'customers': customers_data,
        'items': items_data,
        'reviews': reviews_data
    }

def save_data():
    data = scrape_data()

    with db.session.begin(subtransactions=True):
        # Clear existing data
        Customer.query.delete()
        Item.query.delete()
        Review.query.delete()

        # Add new data
        for customer in data['customers']:
            db.session.add(Customer(name=customer['name']))
        
        for item in data['items']:
            db.session.add(Item(name=item['name'], price=item['price']))

        for review in data['reviews']:
            customer = Customer.query.get(review['customer_id'])
            item = Item.query.get(review['item_id'])
            db.session.add(Review(comment=review['comment'], customer=customer, item=item))

        db.session.commit()
