# Builds index.inline.html: index.html with app.css, app.js and i18n.js inlined (for publishing while developing; no cache problems).
import re
h=open('index.html').read()
def sub(pat,fn):
    global h
    h,n=re.subn(pat,fn,h);assert n==1,(pat,n)
sub(r'<link rel="stylesheet" href="app\.css[^"]*">',lambda m:'<style>'+open('app.css').read()+'</style>')
sub(r'<script src="app\.js[^"]*"></script>',lambda m:'<script>'+open('app.js').read().replace('</script','<\\/script')+'</script>')
sub(r'<script src="i18n\.js[^"]*"></script>',lambda m:'<script>'+open('i18n.js').read().replace('</script','<\\/script')+'</script>')
open('index.inline.html','w').write(h)
print(len(h))
