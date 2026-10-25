#!/usr/bin/env python3
"""python3 bump.py 21.7.9 : writes the version into app.js (APP_VERSION), version.json and the ?v= of the three files in index.html,
so a new version always makes the browser fetch app.css / app.js / i18n.js again (no mix of an old file with a new page)."""
import re,sys
v=sys.argv[1];assert re.fullmatch(r'\d+\.\d+\.\d+',v)
def sub(path,pat,rep,count=1):
    s=open(path).read();n,c=re.subn(pat,rep,s);assert c>=count,(path,pat,c);open(path,'w').write(n)
sub('app.js',r"const APP_VERSION='[^']*'","const APP_VERSION='"+v+"'")
sub('index.html',r'(app\.css|app\.js|i18n\.js)\?v=[0-9.]+',r'\1?v='+v,3)
open('version.json','w').write('{"version":"'+v+'"}')
print('version',v)
import subprocess;subprocess.run([sys.executable,'langpages.py'],check=True)      # the language pages (de/ ru/ ...) copy index.html, so they are rebuilt with every version
