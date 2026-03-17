content = open('templates/base.html').read()
print("Before:", content.count('Admin Panel'))

# Remove all admin related lines from navbar
import re
# Remove the entire staff block
content = re.sub(r'\s*{%\s*if user\.is_staff\s*%}.*?{%\s*endif\s*%}', '', content, flags=re.DOTALL)

print("After:", content.count('Admin Panel'))
open('templates/base.html', 'w').write(content)
print("Done!")
