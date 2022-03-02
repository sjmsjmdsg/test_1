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

def area(r):
    #if DEBUG:
    #   print("Computing area of %r" % r)
    return r

def code_execu:
    if request.method == 'POST':
        first_name = base64.decodestring(request.POST.get('first_name', ''))
        #BAD -- Allow user to define code to be run.
        exec("setname('%s')" % first_name)

if __name__ == '__main__':
    filterScriptTags('asdasd')
    area('a')
    code_execu