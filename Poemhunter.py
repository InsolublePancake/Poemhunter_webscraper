#!pip install --upgrade beautifulsoup4
#!pip install --upgrade html5lib
#!python -m pip install --upgrade pip

import urllib.request
from bs4 import BeautifulSoup
import re, os

def parse_url(root, page, folder):
    
    # Check for output folder, and create new folder if necessary
    if not os.path.exists(folder):
        print('Making Directory')
        os.mkdir(folder)
    else: pass
        
    url = root+page
    print(url)
    
    try:
        html=urllib.request.urlopen(url).read() # Reading Html Codes
        soup = BeautifulSoup(html,'html.parser')
        
        # Get body text of webpage
        body = str(soup.find(class_='KonaBody').p).encode('cp850','replace').decode('cp850')
        body = body.replace('<p>', '').replace('</p>', '').strip().replace('<br/>', '\n')
        
        # Actual title, for printing as heading
        title2 = soup.h1.text.replace(':', ' -').replace(' - Poem','')
        #title2 = title2.decode('utf-8')#.encode('cp850','replace').decode('cp850')
        
        # Title stripped of characters that can't go in a filename
        title = re.sub(r'[*/\?<>:"|]+', '', title2)
        theFile = '{}.txt'.format(title)
        #filepath = '\\'.join([folder, theFile])
        filepath = os.path.join(folder, theFile)
        print(filepath)

        try:
            with open(filepath, 'w') as f:
                title2 = title2.replace(' by', r'\n')
                f.write(title2)
                f.write('\n\n\n')
                f.write(body)
        except:
            print('Error encountered opening: ', filepath)
    
    except Exception as e:
        #print("[Error] ",e)
        print("Error occurred in extracting text from page.\n ", e)
    
    # Extract next link
    try:
        link = soup.find(class_="next")
        next_link = link.a['href']
        parse_url(root, next_link, folder)
        return
    except Exception as e:
        print("Error occurred extracting the next link\n", e, '\n', 'Program Terminating.')
        return
    
    return



soup = parse_url('https://www.poemhunter.com','/poem/desire-threadbare-desires/', 'N:\\user\\lumbric\\stuff\\George Gordon Byron')

print('\n\nEnd')