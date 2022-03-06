from lib2to3.pgen2.tokenize import generate_tokens
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time
import codecs

from selenium.webdriver.chrome.options import Options
user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'
#from capsolution import CapSolution

#capsolution = CapSolution()


class AuctionBot():

    def __init__(self):
        self.urlFromCsv = []
        pass

    def create_browser(self):
        service_obj = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument(f'user-agent={user_agent_desktop}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        #return webdriver.Chrome(service=service_obj,options=options)
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def please_refine_your_search(self,browser):
        html=BeautifulSoup(browser.page_source,'lxml')
        print('please_refine_your_search')
        val = html.find("div", {"class": "not-searched"})
        if val is None:
             return False
        else:
            print('refine exit')
            return True
           

    def readData(self):    
        with open("Biomarkers.csv","r") as my_file:
            csv_reader = csv.reader(my_file)
            next(csv_reader)
            for url in csv_reader:
                self.urlFromCsv.append(url)

    def scrap_me(self, browser, url, filename, gene_name, row_number,start):
        print(filename)
        browser.get(url)
        if row_number == start:
            print("sleeping..")
            time.sleep(30)
        else:
            time.sleep(5)

       
        refine_exist = self.please_refine_your_search(browser)
        print(refine_exist)
        if(refine_exist):
            print('refine exist')
            f = codecs.open('gene.txt','a','utf-8')
            f.writelines('\n')
            f.writelines(gene_name)
        else:
            print('no refine exit')
            f = codecs.open(filename, "w", "utf−8")
            #obtain page source
            h = browser.page_source
            #write page source content to file
            f.writelines(h)
            print("file donwloaded done")


if __name__ == '__main__':

    # bot = AuctionBot()
    # bot.readData()
    # browser = bot.create_browser()
    # start=int(3720)
    f = codecs.open('gene.txt', "r", "utf−8")
    val=int(1)
    for va in f :
        print(val)
        val+=1
        print(va)
    # for row_number in list(range(start, 3720)): 
    #     print(row_number)
    #     url = bot.urlFromCsv[row_number][2]
    #     print(url)
    #    # url='https://www.citeab.com/antibodies/search?q=TNF'
    #     row = int(row_number)
    #     # if(row%50==0):
    #     #     time.sleep(180)
    #     gene_name = bot.urlFromCsv[row_number][1]
    #     filename = gene_name + '.html'.format()
    #     bot.scrap_me(browser, url, filename, gene_name, row_number,start)
