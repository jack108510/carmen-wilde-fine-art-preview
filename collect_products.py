"""Snapshot publicly listed Wix products for the static catalog. Run manually to refresh."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
import json
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from PIL import Image

ROOT=Path(__file__).parent
S=requests.Session()
BASE='https://www.carmenwildefineart.com/'
xml=ET.fromstring(S.get(BASE+'store-products-sitemap.xml',timeout=30).text)
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
entries=[]
for item in xml.findall('s:url',ns):
    url=item.findtext('s:loc',namespaces=ns)
    image=item.findtext('i:image/i:loc',namespaces=ns)
    entries.append((url,image))

def one(entry):
    url,img=entry
    slug=urlparse(url).path.rsplit('/',1)[-1]
    soup=BeautifulSoup(requests.get(url,timeout=35).text,'html.parser')
    scripts=soup.find_all('script',type='application/ld+json')
    product=next((json.loads(x.get_text()) for x in scripts if '"@type":"Product"' in x.get_text()),None)
    if not product: raise ValueError(f'No product schema: {url}')
    offer=product.get('offers',{})
    image_id=img.split('/media/')[1].split('/v1/')[0]
    image_url='https://static.wixstatic.com/media/'+image_id+'/v1/fit/w_1200,h_1200,q_85/file.jpg'
    raw=requests.get(image_url,timeout=50);raw.raise_for_status()
    pict=Image.open(BytesIO(raw.content)).convert('RGB');pict.thumbnail((1200,1200))
    out=ROOT/'assets'/'products'/f'{slug}.webp';out.parent.mkdir(parents=True,exist_ok=True)
    pict.save(out,'WEBP',quality=79,method=4)
    return {'slug':slug,'name':unescape(product['name']),'description':unescape(product.get('description','')).replace('&#010;',' ').replace('\n',' · '),'price':offer.get('price'),'currency':offer.get('priceCurrency','CAD'),'availability':offer.get('availability','').split('/')[-1],'image':'assets/products/'+slug+'.webp','legacy_url':url}

products=[]
with ThreadPoolExecutor(max_workers=7) as pool:
    futures={pool.submit(one,e):e for e in entries}
    for f in as_completed(futures):
        try:
            item=f.result(); products.append(item);print(item['slug'],item['price'],item['availability'],flush=True)
        except Exception as exc: print('FAILED',futures[f][0],str(exc),flush=True)
products.sort(key=lambda x:x['name'].casefold())
(ROOT/'products.json').write_text(json.dumps(products,indent=2,ensure_ascii=False)+'\n')
print('Collected',len(products),'of',len(entries))
