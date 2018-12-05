# -*- coding: utf-8 -*-
"""
Download a Single chapter of the code from ICC


"""
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import bs4, requests, re, os


def getrealsource(x):
            
    with closing(Firefox()) as browser:
        browser.get(x)
        time.sleep(random.randint(10,15))     #dynamic page which need a couple of seconds to load
        page_source = browser.page_source     #this is the real source code we can scrap
        
    return(page_source)


def getcodefile(x):                          #the function that scrape or download the chapter
          
    res = getrealsource(x)    
    s = bs4.BeautifulSoup(res)
    
    if s.select('iframe'):                   #Tag iframe will mean this chapter is in a pdf file
        
        pdfloc = re.compile(r'(?<=//).*')
        pdfname = re.compile(r'[^/]+$')
        unallowed = re.compile(r'[/\:*?<>]')
        pdf = re.compile(r'pdfViewer')
        
        iframes = s.select('iframe')                        #list of iframes
        
        for iframe in iframes:
            if 'pdfViewer' in str(iframe):
                
                address = iframe.get('src')                 #attribute src
                dllink = pdfloc.search(address)
                name = pdfname.findall(address)
                download = dllink.group()
                
                dl = requests.get('http://' + download)
                
                path = s.select('.book_heading')[0].getText()
                path = unallowed.sub('', path)
                filename = name[0]
                
                try:
                    os.makedirs(path)
                except:
                    print(f'{path} does already exist')
                    
                with open(os.path.join(path, filename), 'wb') as f:
                    f.write(dl.content)
                print(f'{filename} is saved!')
            else:
                pass
    else:
        
        if s.select('h1.pt-4'):
            
            space_finder_front = re.compile(r'(?<=\D)(?=\d+)')           # Some number fall between words without a space
            space_finder_back = re.compile(r'(?<=\d)(?=\D+)')            # Try to find them this way
            
            path = s.select('h1.pt-4')[0].getText().strip()
            
            if s.select('h1.chapter'):
                chapter = s.select('h1.chapter')[0].getText()
                chapter = space_finder_front.sub(' ', chapter)
                chapter = space_finder_back.sub(' ', chapter)
                page = s.select('section.chapter')
                
            elif s.select('h1.frontmatter_title'):                       # I don't know if they still have this kind of notation
                chapter = s.select('h1.frontmatter_title')[0].getText()  # I did not do further check. This is just an excercise for me.
                chapter = space_finder_front.sub(' ', chapter)
                chapter = space_finder_back.sub(' ', chapter)
                page = s.select('section.frontmattercontent')
   
            
            page = page[0](['p', 'h1', 'h2', 'dl', 'table'])             # capture p, h1, h2 (if any), dl (list) and table tags
            p = []
            for i in range(len(page)):
                try:
                    line = pd.read_html(str(page[i]))                    # try to read table with pandas if there are any(not the best way)
                except:
                    line = space_finder_front.sub(' ', page[i].getText())   #capture text
                    line = space_finder_back.sub(' ', line)                 #and a space to the number in between 2 words
                p.append(line)
            
            for i in range(len(p)):                                      #print the lines on the screen
                print(p[i])
                
            filename = chapter + '.txt'                                  #write to a txt file
            path = unallowed.sub('', path)

            if not os.path.exists(path):
                os.makedirs(path)   
                
            file = open(os.path.join(path, filename), 'wb')
            for i in range(0, len(p)):
                
                file.write((p[i] + '\r\n\r\n').encode())
            file.close()
            
            
        else:                                                        # I don't know if I need to test those any more.
            if s.select('.container-top strong'):
                name = re.search(r'\S.*', s.select('.container-top strong')[0].getText()).group()
                page = s.find_all(['p' ,'table'])
            elif s.select('.container-top h1'):
                name = re.search(r'\S.*', s.select('.container-top h1')[0].getText()).group()
                page = s.select('.container-top p')
            elif s.select('.*title'):
                name = re.search(r'\S.*', s.select('.*title')[0].getText()).group()
                page = s.select('.container-top p')
            else:
                title = re.search(r'\S+[^\|]*\|', s.select_one('title').get_text()).group()[:-2]
                page = s.select('.container-top p')
                name = title


            p = []
            for i in range(len(page)):
                if page[i].name == 'p':
                    p.append(page[i].getText())
                else:
                    pass
            
            for i in range(len(p)):
                print(p[i])
                
            
#            path = s.select('.book_heading')[0].getText()
#            path = unallowed.sub('', path)
            filename = name + '.txt'
            if not os.path.exists(path):
                os.makedirs(path)   
                
            file = open(os.path.join(path, filename), 'wb')
            for i in range(1, len(p)):
                
                file.write((p[i] + '\r\n\r\n').encode())
            file.close()

#getcodefile(x)

        