from bs4 import BeautifulSoup
import difflib
import requests
import time
import csv
from helper import cut_email,last_name,first_name,checkEmail
user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

#variable
urlFromCsv=[]
block_site=[]
row_number=int(1700)
answer=[]

#for read data from csv file
def readData():    
    with open("siteLink2.csv","r") as my_file:
        csv_reader = csv.reader(my_file)
        next(csv_reader)
        for url in csv_reader:
            urlFromCsv.append(url)
    #print(urlFromCsv) 

def retriveData(url_number):
    try:
        headers = { 'User-Agent': user_agent_desktop}
        content = None
        print(urlFromCsv[url_number][0])
        html_content = requests.get(urlFromCsv[url_number][0],headers=headers).text
        soup = BeautifulSoup(html_content, "lxml")
      
    except:
        print('data can not retrive from the url')
        print(url_number,urlFromCsv[url_number][0])
        return url_number
    #for get the email
    try:
        temp_email=[]
        map_email ={}
        author_info = soup.find_all(attrs={"class": "oemail"})
       
        #if not get any email
        if(len(author_info)==0):
            print('block site')
            answer.append([urlFromCsv[url_number][0],'null','null','null','null'])
            return url_number+1
      
        for email in author_info:
            #print(email.text)
            if(map_email.get(email.text)):
                continue
            else:
                val=email.text[::-1]
                temp_email.append(val)
                map_email[email.text]=1
           

    except:
        
        # block_site.append(url_number,urlFromCsv[url_number],"no email")
        print('can not retrive email') 
        return url_number   

    try:
        #get the author name
        flag= True  
        author_name =soup.find(attrs={"class":"fm-author"})
        author_names = author_name.find_all('a') 
       
           
        for name in author_names:
            val = name.text            
            mail=checkEmail(temp_email,val)
            #print(mail,val)
            if(mail):
                answer.append([urlFromCsv[url_number][0],mail,first_name(val).strip(),last_name(val).strip(),val])
                flag=False 
                break
        if(flag):
            answer.append([urlFromCsv[url_number][0],temp_email[0],first_name(author_names[0].text).strip(),last_name(author_names[0].text).strip(),author_names[0].text])
            block_site.append([url_number,urlFromCsv[url_number][0],"algo error"])
        return url_number+1       
    except:
       answer.append([urlFromCsv[url_number][0],'null','null','null','null'])
       return url_number+1
def writeData():
    print(len(block_site))
  
   
    with open('resul9.csv', 'a', newline="",encoding="utf-8") as file:
        header=['Article Link','Email','First Name','Last Name','Full Name']
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerow(header) # 4. write the header
        csvwriter.writerows(answer)
    with open('errors8.csv', 'a', newline="",encoding="utf-8") as file:
        header=['Article number','Article Link','Comment']
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerow(header) # 4. write the header
        csvwriter.writerows(block_site)


if __name__ == '__main__':
    readData()
    row_number=7000
    while row_number!=len(urlFromCsv):
       row_number= retriveData(row_number)
       print(row_number)
       #time.sleep(1)
    writeData()   

    
    



