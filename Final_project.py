import re
import mysql.connector
import requests
from bs4 import BeautifulSoup

#Connecting to DataBase
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="@Hmadre87"
)
mycursor = mydb.cursor()
#Creating DataBase and Table if Not exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS Car_Advice")
mycursor.execute("use Car_Advice")
stmt = "SHOW TABLES LIKE 'Car_Attributes'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if not result:
    mycursor.execute("CREATE TABLE Car_Attributes (Name VARCHAR(255),Model VARCHAR(255),Prod_Year INT, Price VARCHAR(255), Mileage INT)")

#------------------------------------------------------------------------
# Fetching Price and Mileage of input car string from Bama.ir
print("Please Enter Your Intended Car Name or Model Name to search:")
car_name = input()
counter = 0
page_no = 0
result = []
while page_no < 500:
    page_no += 1
    url = 'https://bama.ir/car/all-brands/all-models/all-trims?page=' + str(page_no)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    name = soup.find_all('h2',attrs={'class':'persianOrder'})
    Model = soup.find_all('span',attrs={'style':'display:inline-block;'})
    Price = soup.find_all('p',attrs={'class':'cost'})
    Mileage = soup.find_all('p',attrs={'class':'price hidden-xs'})

    for i in range(len(name)):
        cn = re.sub('\s+',' ',name[i].text).strip()
        if car_name in cn:
            mo = re.sub('\s+',' ',Model[i].text).strip()
            Year = re.findall(r'^\d{4}',cn)
            Year = int(Year[0])
            pr = re.sub('\s+',' ',Price[i].text).strip()
            # convert pr to INT
            mi = re.sub('\s+',' ',Mileage[i].text).strip()
            mi = re.sub(r',','',mi)
            if ('صفر' in mi) or ('کارتکس' in mi):
                mi = 0
            elif '-' in mi:
                continue
            else:
                mi = re.findall(r'\d{1,6}',mi)
                mi = int(mi[0])

            result.append((cn,mo,Year,pr,mi))
            counter +=1
            print(counter, " car found...")
            # if counter==20:
            #     break

for i in range(len(result)):
    #Inserting Data to Database----------------------------------------------------#
    sql = "INSERT INTO Car_Attributes (Name, Model, Prod_Year, Price, Mileage) VALUES (%s, %s, %s, %s, %s)"
    val = [
        (result[i][0], result[i][1], result[i][2], result[i][3], result[i][4])
    ]
    mycursor.executemany(sql, val)
    mydb.commit()

def show_DB():
    mycursor.execute("Select * From Car_Attributes")
    myresult = mycursor.fetchall()
    print("Reporting the records of Car_Attributes Database")
    print("--------------------------------------------")
    print("There are ",len(myresult)," records in the Database.")
    print("")
    c = 0
    print('{0:60s}{1:40s}{2:20s}        {3:40s}{4:20s}'.format('نام خودرو', 'مدل خودرو','سال ساخت', 'قیمت خودرو', 'کارکرد'))
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for x in myresult:
        c+=1
        print(c,'-{0:60s}{1:40s}{2:20d}        {3:40s}{4:20d}'.format(x[0],x[1],x[2],x[3],x[4]))

print('Do you want to show you DataBase?(Yes/No)')
ans = input()
if ans == 'Yes' or ans == 'yes' or ans == 'y' or ans == 'Y':
    show_DB()


