# Fix items/admin.py - remove list_editable conflicts
content = open('items/admin.py').read()
content = content.replace("    list_editable = ['status']\n    list_per_page = 20\n    date_hierarchy = 'date_posted'\n    ordering      = ['-date_posted']\n    inlines       = [ClaimInline]", "    list_per_page = 20\n    date_hierarchy = 'date_posted'\n    ordering      = ['-date_posted']\n    inlines       = [ClaimInline]")
content = content.replace("    list_editable   = ['status']\n    list_per_page = 25", "    list_per_page = 25")
open('items/admin.py', 'w').write(content)
print('items/admin.py fixed!')

# Fix accounts/admin.py - remove list_editable conflict
content = open('accounts/admin.py').read()
content = content.replace("    list_editable = ['is_verified']\n    readonly_fields", "    readonly_fields")
open('accounts/admin.py', 'w').write(content)
print('accounts/admin.py fixed!')
