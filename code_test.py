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
        # content = re.sub(r'<script.*?>.*?</script>', '', content, flags= re.DOTALL | re.IGNORECASE)
    return content


urlpatterns = [
    # Route to code_execution
    url(r'^code-ex1$', code_execution_bad, name='code-execution-bad'),
    url(r'^code-ex2$', code_execution_good, name='code-execution-good')
]

def code_execution(request):
    if request.method == 'POST':
        first_name = base64.decodestring(request.POST.get('first_name', ''))
        #BAD -- Allow user to define code to be run.
        exec("setname('%s')" % first_name)

if __name__ == '__main__':
    filterScriptTags('asdasd')