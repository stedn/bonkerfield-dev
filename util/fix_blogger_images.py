from bs4 import BeautifulSoup
import glob
import fileinput
import sys
import re
import os
import urllib.request

files = glob.glob('*.html')
for f in files:
    img_src = None
    with open(f) as page:
        soup = BeautifulSoup(page, "html.parser")
        img = soup.find('img')
        if not img:
            break
        img_src = img['src']
        if 'blogspot' in img['src']:
            src_parts = img['src'].split('/')
            img_src = '/'.join(src_parts[:-2]+[src_parts[-1]])
    if img_src:
        for line in fileinput.input([f], inplace=True):
            if line.strip().startswith('image: '):
                line = 'image: '+img_src + '\n'
            sys.stdout.write(line)





files = glob.glob('*.html')
REMOVE_ATTRIBUTES = ['width','height', 'data-original-width', 'data-original-height']
for f in files:
    soup = None
    with open(f) as page:
        soup = BeautifulSoup(page, "html.parser")
        global_div = soup.find('div', {"dir": "ltr", "trbidi":"on"})
        if global_div:
            global_div.replaceWithChildren()
        [d.decompose() for d in soup.findAll('div', style=re.compile("display:none"))] 
        for div in soup.findAll('div', {"class": "separator"}):
            a = div.a
            if a:
                img = a.img
                if img:
                    img['title'] = div.text +' '+ div.a.text
                    val = 's1600'
                    if ('width' in img.attrs) and ('height' in img.attrs) and (img['width'] < img['height']):
                        val = 's800'
                    for attr in REMOVE_ATTRIBUTES:
                        if attr in img.attrs:
                            del img.attrs[attr]

                    if 'blogspot' in img['src']:
                        src_parts = img['src'].split('/')
                        img_src = '/'.join(src_parts[:-2]+[val]+[src_parts[-1]])
                        img['src'] = img_src
                    div.replaceWith(img)
    if soup:
        with open(f, "w") as f_output:
            f_output.write(str(soup)) 


files = glob.glob('*.html')
for f in files:
    soup = None
    with open(f) as page:
        true_folder = '/assets/images/'+f.split('-')[0]+'/'
        folder = '..'+true_folder
        if not os.path.exists(folder):
            os.mkdir(folder)
        soup = BeautifulSoup(page, "html.parser")
        for img in soup.findAll('img'):
            new_name=img['src'].split('/')[-1]
            try:
                urllib.request.urlretrieve(img['src'], folder+new_name)
                img['src']=true_folder+new_name
            except:
                img['src']='/assets/images/main/octopus.jpeg'
    if soup:
        with open(f, "w") as f_output:
            f_output.write(str(soup)) 