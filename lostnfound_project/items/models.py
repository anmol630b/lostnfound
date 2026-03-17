from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Item(models.Model):
    ITEM_TYPE_CHOICES = [('lost', 'Lost'), ('found', 'Found')]

    CATEGORY_CHOICES = [
        ('electronics',  'Electronics (Phone, Laptop, etc.)'),
        ('books',        'Books & Documents'),
        ('id_cards',     'ID / Identity Cards'),
        ('keys',         'Keys'),
        ('bags',         'Bags & Backpacks'),
        ('clothing',     'Clothing & Accessories'),
        ('jewelry',      'Jewelry & Watches'),
        ('wallet',       'Wallet & Money'),
        ('sports',       'Sports Equipment'),
        ('vehicles',     'Vehicle Parts / Accessories'),
        ('pets',         'Pets'),
        ('toys',         'Toys & Games'),
        ('other',        'Other'),
    ]

    STATUS_CHOICES = [
        ('active',   'Active'),
        ('resolved', 'Resolved'),
        ('claimed',  'Claimed'),
    ]

    LOCATION_CHOICES = [
        ('market',       'Market / Shopping Area'),
        ('bus_stand',    'Bus Stand / Railway Station'),
        ('park',         'Park / Garden'),
        ('hospital',     'Hospital / Clinic'),
        ('school',       'School / College'),
        ('office',       'Office / Workplace'),
        ('restaurant',   'Restaurant / Cafe'),
        ('road',         'Road / Street'),
        ('temple',       'Temple / Mosque / Church'),
        ('airport',      'Airport'),
        ('mall',         'Mall / Shopping Center'),
        ('bank',         'Bank / ATM'),
        ('gym',          'Gym / Sports Complex'),
        ('cinema',       'Cinema / Theatre'),
        ('metro',        'Metro / Auto / Cab'),
        ('home_area',    'Residential Area'),
        ('other',        'Other Location'),
    ]

    title            = models.CharField(max_length=200)
    description      = models.TextField()
    category         = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    item_type        = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    location         = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    location_detail  = models.CharField(max_length=200, blank=True, help_text="City, area, or specific place")
    date_lost_found  = models.DateField()
    date_posted      = models.DateTimeField(default=timezone.now)
    image            = models.ImageField(upload_to='items/', blank=True, null=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    posted_by        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    contact_email    = models.EmailField(blank=True)
    contact_phone    = models.CharField(max_length=15, blank=True, help_text="Phone/WhatsApp number")
    views_count      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'[{self.item_type.upper()}] {self.title}'

    def get_type_color(self):
        return 'danger' if self.item_type == 'lost' else 'success'

    def get_whatsapp_link(self):
        if self.contact_phone:
            phone = self.contact_phone.strip().replace(' ','').replace('+','').replace('-','')
            if not phone.startswith('91'):
                phone = '91' + phone
            msg = f'Hi! I saw your {self.item_type} item "{self.title}" on LostNFound. I want to help!'
            import urllib.parse
            return f'https://wa.me/{phone}?text={urllib.parse.quote(msg)}'
        return None

    def get_category_icon(self):
        icons = {
            'electronics': 'fa-mobile-alt',
            'books':       'fa-book',
            'id_cards':    'fa-id-card',
            'keys':        'fa-key',
            'bags':        'fa-shopping-bag',
            'clothing':    'fa-tshirt',
            'jewelry':     'fa-gem',
            'wallet':      'fa-wallet',
            'sports':      'fa-futbol',
            'vehicles':    'fa-car',
            'pets':        'fa-paw',
            'toys':        'fa-gamepad',
            'other':       'fa-box',
        }
        return icons.get(self.category, 'fa-box')


class ClaimRequest(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    item          = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    message       = models.TextField()
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    created_at    = models.DateTimeField(default=timezone.now)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']
        unique_together = ['item', 'claimant']

    def __str__(self):
        return f'Claim by {self.claimant.username} for {self.item.title}'
