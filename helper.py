import csv
import difflib


def cut_email(str):
    val=''
    for i in str:
        if i!='@':
            val+=i
        else :
            return val   

def last_name (name):
    str=""
    for char in reversed(name):
        if(char==' '):
            break
        else:
            str+=char
    return str[::-1]        

def removeSpecialCharFromName(name):
    str=""
    for char in reversed(name):
        if(char>='a' and char<='z'):
            str+=char
    return str[::-1]      
           
def first_name(name):
    lst = name.split(' ')
    str =' '
    for i in range(len(lst)-1):
        str+=lst[i]
        str+=" "
    return str

def checkEmail(emails:list,name):
    name = removeSpecialCharFromName(name.lower())  
    #print(name,end=' ')
    for email in emails:
        shortEmail = cut_email(email.lower())
        length = len(shortEmail);
        control=length
        #print(length,shortEmail)
        while(length>2):
           # print(length)
            #print('================----------------==================')
            for j in range(len(name)-length+1):
                temp_name = name[j:length+j]
                #print(temp_name)
                for i in range(len(shortEmail)-length+1):
                    #print('okkk',email[i:length+i],temp_name,i)
                    if(temp_name == email[i:length+i]):
                        return email
                    control+=1;
            length-=1
            control = length    
       # print(name,email,shortEmail)
    return False        
         
def readData():   
    urlFromCsv=[] 
    with open("siteLink2.csv","r") as my_file:
        csv_reader = csv.reader(my_file)
        next(csv_reader)
        for url in csv_reader:
            urlFromCsv.append(url)
    return urlFromCsv        
        
def writeData(answer,block_site):
    with open('resul4.csv', 'w', newline="") as file:
        header=['Article Link','Email','First Name','Last Name','Full Name']
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerow(header) # 4. write the header
        csvwriter.writerows(answer)
    with open('errors4.csv', 'w', newline="") as file:
        header=['Article number','Article Link','Comment']
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerow(header) # 4. write the header
        csvwriter.writerows(block_site)


def readData1(): 
    urlFromCsv =[]
    
    with open("resul9.csv","r") as my_file:
        csv_reader = csv.reader(my_file)
        next(csv_reader)
        print('okk')
        for url in csv_reader:
            urlFromCsv.append(url[0])
           
    
    data=int(1)   
    with open("siteLink2.csv","r") as my_file:
        csv_reader = csv.reader(my_file)
        next(csv_reader)
        for urls in csv_reader:
            val =urls[0]
            if(urlFromCsv.index(val)):
                continue
            else:
                print(urls[0],data)
            data+=1     


          
# emmmail = 'emw'
readData1()

# mailList =['Torcato Martins','Francesco Meghini','Francesca Florio',' Yuu Kimata1','em M. Wilson']
# val = difflib.get_close_matches(emmmail,mailList,cutoff=0.3)
# print(val)





