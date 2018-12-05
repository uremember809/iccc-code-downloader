# -*- coding: utf-8 -*-
"""
a script for saving ICC code to the local computer.

@author: matt
"""
    
def download_code(addr):
    
    import requests, sys, pyperclip 
    import dlcode, bs4, time


    #address = pyperclip.paste() if addr == '' else addr
    page = requests.get(address)
    bs = bs4.BeautifulSoup(page.text)
    chapter = bs.select('.toc a')


    for i in range(len(chapter)):
        dlcode.getcodefile('https://codes.iccsafe.org' + chapter[i].get('href'))
        time.sleep(5)

address = pyperclip.paste()
if __name__ == '__main__':
    download_code(address)



