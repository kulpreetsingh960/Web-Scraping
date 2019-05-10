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
mycursor.execute("CREATE DATABASE IF NOT EXISTS Car")
mycursor.execute("use Car")
stmt = "SHOW TABLES LIKE 'Car_Attr'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if not result:
    mycursor.execute("CREATE TABLE Car_Attr (Name VARCHAR(255), Price VARCHAR(255), Mileage VARCHAR(255))")
#------------------------------------------------------------------------
# Fetching Price and Mileage of input car string from Bama.ir
print("Please Enter Your Intended Car Name to search:")
car_name = input()
counter = 0
page_no = 0
result = []
while counter < 20:
    page_no += 1
    url = 'https://bama.ir/car/all-brands/all-models/all-trims?page=' + str(page_no)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    name = soup.find_all('h2',attrs={'class':'persianOrder'})
    Price = soup.find_all('p',attrs={'class':'cost'})
    Mileage = soup.find_all('p',attrs={'class':'price hidden-xs'})

    for i in range(len(name)):
        cn = re.sub('\s+',' ',name[i].text).strip()
        pr = re.sub('\s+',' ',Price[i].text).strip()
        mi = re.sub('\s+',' ',Mileage[i].text).strip()
        if car_name in cn:
            result.append((cn,pr,mi))
            counter +=1
            print(counter, " car found...")
            if counter==20:
                break

for i in range(len(result)):
    #Inserting Data to Database----------------------------------------------------#
    sql = "INSERT INTO Car_Attr (Name, Price, Mileage) VALUES (%s, %s, %s)"
    val = [
        (result[i][0], result[i][1], result[i][2])
    ]
    mycursor.executemany(sql, val)
    mydb.commit()

def show_DB():
    mycursor.execute("Select * From Car_Attr")
    myresult = mycursor.fetchall()
    print("Reporting the records of Car_Attr Database")
    print("--------------------------------------------")
    print("There are ",len(myresult)," records in the Database.")
    print("")
    c = 0
    print('{0:60s}{1:40s}{2:40s}'.format('نام خودرو', 'قیمت خودرو', 'کارکرد'))
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for x in myresult:
        c+=1
        print(c,'-{0:60s}{1:40s}{2:40s}'.format(x[0],x[1],x[2]))

print('Do you want to show you DataBase?(Yes/No)')
ans = input()
if ans == 'Yes' or ans == 'yes' or ans == 'y' or ans == 'Y':
    show_DB()


