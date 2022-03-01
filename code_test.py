# Imported into code using

from finance import *
tax2 = 11
print(tax1)
print(tax2)


import re
def filterScriptTags(content):
    oldContent = ""
    while oldContent != content:
        oldContent = content
        content = re.sub(r'<script.*?>.*?</script>', '', content, flags= re.DOTALL | re.IGNORECASE)
    return content


if __name__ == '__main__':
    filterScriptTags('asdasd')