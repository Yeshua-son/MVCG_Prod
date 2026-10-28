import json,sys
SITE = 'https://mvcg-prod.stwb.workers.dev'   # adresse publique du site, sans / final : à changer pour le domaine définitif
src=open('/home/claude/mvcg/index.src.html',encoding='utf8').read()
src=src.replace('__SITE__', SITE)
fonts=json.load(open('/home/claude/mvcg/fonts.json'))
for i,f in enumerate(fonts): src=src.replace(f'__FONT{i}__',f)
assert '__FONT' not in src
# IMG_EMBED : images intégrées en data URI
import re,base64,mimetypes
def emb(m):
    path='/home/claude/mvcg/site/'+m.group(1)
    mt={'jpg':'image/jpeg','jpeg':'image/jpeg','webp':'image/webp','png':'image/png'}[path.rsplit('.',1)[1]]
    return 'src="data:'+mt+';base64,'+base64.b64encode(open(path,'rb').read()).decode()+'"'
src=re.sub(r'src="(images/[^"]+)"',emb,src)
def emb_css(m):
    path='/home/claude/mvcg/site/'+m.group(1)
    mt={'jpg':'image/jpeg','webp':'image/webp','png':'image/png','svg':'image/svg+xml'}[path.rsplit('.',1)[1]]
    return 'url("data:'+mt+';base64,'+base64.b64encode(open(path,'rb').read()).decode()+'")'
src=re.sub(r'url\("(images/[^"]+)"\)',emb_css,src)
assert 'url("images/' not in src
assert 'src="images/' not in src
# artifact version (fragment) and standalone version
open('/home/claude/mvcg/site/index.html','w',encoding='utf8').write(src)
title_end=src.index('</title>')+8
head=src[:title_end]
standalone='<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+src.split('<a class="skip"')[0]+'</head>\n<body>\n<a class="skip"'+src.split('<a class="skip"',1)[1]+'\n</body>\n</html>\n'
import os; os.makedirs('/home/claude/mvcg/standalone',exist_ok=True)
open('/home/claude/mvcg/standalone/index.html','w',encoding='utf8').write(standalone)
print(len(src))
