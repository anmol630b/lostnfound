content = open('items/admin.py').read()

# Fix - title column ko proper naam do
old = "    list_display = [\n        'item_image_thumb', 'title', 'type_badge', 'get_category_display',\n        'get_location_display', 'status_badge', 'posted_by_link',\n        'claims_count', 'views_count', 'date_posted'\n    ]"

new = "    list_display = [\n        'item_image_thumb', 'title', 'type_badge', 'cat_display',\n        'loc_display', 'status_badge', 'posted_by_link',\n        'claims_count', 'views_count', 'date_posted'\n    ]"

content = content.replace(old, new)

# Fix method names
content = content.replace(
    "    def category_display(self, obj):\n        return obj.get_category_display()\n    category_display.short_description = 'Category'",
    "    def cat_display(self, obj):\n        return obj.get_category_display()\n    cat_display.short_description = 'Category'"
)
content = content.replace(
    "    def location_display(self, obj):",
    "    def loc_display(self, obj):"
)
content = content.replace(
    "    location_display.short_description = 'Location'",
    "    loc_display.short_description = 'Location'"
)

open('items/admin.py', 'w').write(content)
print('Fixed!')
