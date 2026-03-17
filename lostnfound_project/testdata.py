import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostnfound.settings')
django.setup()

from django.contrib.auth.models import User
from items.models import Item
from datetime import date

# Superuser se items banao
user = User.objects.filter(is_superuser=True).first()
if not user:
    print("Pehle superuser banao!")
else:
    test_items = [
        dict(title='Black iPhone 14', description='Black color iPhone 14 with cracked back cover. Lost near main road.',
             category='electronics', item_type='lost', location='road',
             location_detail='MG Road, near petrol pump', date_lost_found=date.today(),
             contact_phone='9876543210', contact_email=user.email),
        dict(title='Blue Backpack', description='Blue Nike backpack with books inside. Found at bus stand.',
             category='bags', item_type='found', location='bus_stand',
             location_detail='City Bus Stand Platform 3', date_lost_found=date.today(),
             contact_phone='9876543210', contact_email=user.email),
        dict(title='Aadhar Card', description='Aadhar card found near ATM. Owner please contact.',
             category='id_cards', item_type='found', location='bank',
             date_lost_found=date.today(), contact_email=user.email),
        dict(title='Car Keys with Red Keychain', description='Toyota car keys with red keychain lost in market area.',
             category='keys', item_type='lost', location='market',
             location_detail='Lal Darwaza Market', date_lost_found=date.today(),
             contact_phone='9123456789', contact_email=user.email),
        dict(title='Gold Watch', description='Gold colored wristwatch with leather strap. Lost at restaurant.',
             category='jewelry', item_type='lost', location='restaurant',
             date_lost_found=date.today(), contact_email=user.email),
        dict(title='Brown Wallet', description='Brown leather wallet with some cash and cards found at park.',
             category='wallet', item_type='found', location='park',
             location_detail='Central Park, near fountain', date_lost_found=date.today(),
             contact_phone='9988776655', contact_email=user.email),
    ]

    count = 0
    for data in test_items:
        item, created = Item.objects.get_or_create(
            title=data['title'],
            defaults={**data, 'posted_by': user}
        )
        if created:
            count += 1
            print(f'  Created: [{item.item_type.upper()}] {item.title}')
        else:
            print(f'  Exists:  [{item.item_type.upper()}] {item.title}')

    print(f'\nDone! {count} new items added.')
    print(f'Total items now: {Item.objects.count()}')
