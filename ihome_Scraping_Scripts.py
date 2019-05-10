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
mycursor.execute('CREATE DATABASE IF NOT EXISTS home')
mycursor.execute('USE home')
stmt = "SHOW TABLES LIKE 'home_Features'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if not result:
    mycursor.execute("CREATE TABLE home_Features (Location VARCHAR(255), Area INT, BED INT, Price BIGINT)") #Build_Age Was removed

###########################################################################################################

def show_DB():
    mycursor.execute("Select * From home_Features")
    myresult = mycursor.fetchall()
    print("Reporting the records of home_Features Database")
    print("--------------------------------------------")
    print("There are ",len(myresult)," records in the Database.")
    print("")
    c = 0
    print('{0:^40s}{1:^15s}{2:^15s}{3:>20s}'.format('نام منطقه', 'مساحت خانه', 'تعداد اتاق', 'قیمت خانه'))
    print('--------------------------------------------------------------------------------------------------------')
    for x in myresult:
        c+=1
        print(c,'{0:^35s}{1:^20d}{2:^20d}{3:^30d}'.format(x[0],x[1],x[2],x[3]))
###-------------------------------------------------------------------------------------------------------------------###

def Web_Scraping_ihome(No_Page):
    page_no = 0
    result = []
    while page_no < No_Page:
        page_no += 1
        # url = URL + str(page_no)
        url = 'https://www.ihome.ir/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/'+ str(page_no)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        Location = soup.find_all('div', attrs={'class': 'location'})
        Area = soup.find_all('i', attrs={'class': 'ihome-arrows'})
        Bed = soup.find_all('i', attrs={'class': 'ihome-bed'})
        Price = soup.find_all('div', attrs={'class': 'price'})
        Price = Price[1:]
        for i in range(len(Bed)):
            Lo = re.sub('\s+', ' ', Location[i].text).strip()
            # Processing the Area of Home
            Ar = re.sub('\s+', ' ', Area[i].next_sibling).strip()
            Ar = re.findall(r'^\d*', Ar)
            try:
                Ar = int(Ar[0])
            except ValueError:
                continue
            # Processing the number of rooms in Home
            B = re.sub('\s+', ' ', Bed[i].next_sibling).strip()
            try:
                B = int(B)
            except ValueError:
                continue
            # Processing the Price of Home
            Pr = re.sub('\s+', ' ', Price[i].text).strip()
            Pr = re.sub(',', '', Pr)
            try:
                Pr = int(re.findall(r'^\d*', Pr)[0])
            except ValueError:
                continue

            result.append((Lo, Ar, B, Pr))
    # Inserting Data to the DataBase ---------------------------------------------------------------------------
    for i in range(len(result)):
        sql = "INSERT INTO home_Features (Location, Area, BED, Price) VALUES (%s, %s, %s, %s)"
        val = [
            (result[i][0], result[i][1], result[i][2], result[i][3])
        ]
        mycursor.executemany(sql, val)
        mydb.commit()
####-----------------------------------------------------------------------------------------------------------------####
Ex = True
while(Ex):

    print('1- Search For HOME based on location.')
    print('2- Give Location, Area and Bed Number to Estimate the Home Price.')
    print('3- Create New Database')
    print('4- Show Database')
    print('5- Exit')
    option = int(input('Please Choose one option (1-5) :'))

    ####-----------------------------OPTION 1 IMPLEMENTATION---------------------------------####
    if option==1:
        print("Please Enter Your Location Name -- Sample(سعادت آباد):  ")
        location = input()
        CI = False
        while CI == False:
            try:
                P_Num = int(input("Please Enter The Number of Pages You Want to Search:  "))
                if type(P_Num)==int:
                    CI = True
            except ValueError:
                P_Num = int(input("Please Enter a number:  "))
                if type(P_Num) == int:
                    CI = True
                else:
                    print("Incorrect Input!")
                    exit(1)
        counter = 0
        page_no = 0
        result = []
        while page_no < P_Num:
            page_no += 1
            url = 'https://www.ihome.ir/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/'+ str(page_no)
            r =requests.get(url)
            soup = BeautifulSoup(r.text,'html.parser')
            print("Searching for {} in page {} of ihome.ir".format(location,page_no))
            Location = soup.find_all('div',attrs={'class':'location'})
            Area = soup.find_all('i',attrs={'class':'ihome-arrows'})
            # Build_Age = soup.find_all('i',attrs={'class':'ihome-building-age'})
            Bed = soup.find_all('i',attrs={"class":"ihome-bed"})
            # print(len(Bed))
            Price = soup.find_all('div',attrs={'class':'price'})
            Price = Price[1:]
            for i in range(len(Bed)):
                Lo = re.sub('\s+',' ',Location[i].text).strip()
                if location in Lo:
                    # Processing the Area of Home
                    Ar = re.sub('\s+', ' ', Area[i].next_sibling).strip()
                    Ar = re.findall(r'^\d*',Ar)
                    try:
                        Ar = int(Ar[0])
                    except ValueError:
                        continue
                    # Processing the number of rooms in Home
                    B = re.sub('\s+', ' ', Bed[i].next_sibling).strip()
                    try:
                        B = int(B)
                    except ValueError:
                        continue
                    # Processing the Price of Home
                    Pr = re.sub('\s+',' ',Price[i].text).strip()
                    Pr = re.sub(',','',Pr)
                    try:
                        Pr = int(re.findall(r'^\d*',Pr)[0])
                    except ValueError:
                        continue
                    # print(Ar)
                    # B_A = re.sub('\s+', ' ', Build_Age[i].next_sibling).strip()
                    # B_A = re.findall(r'^\d{1-2}',B_A)
                    # B_A = B_A[0]
                    # print(B_A)
                    result.append((Lo, Ar, B, Pr))
        # Inserting Data to the DataBase ---------------------------------------------------------------------------
        # for i in range(len(result)):
        #     sql = "INSERT INTO home_Features (Location, Area, BED, Price) VALUES (%s, %s, %s, %s)"
        #     val = [
        #         (result[i][0], result[i][1], result[i][2], result[i][3])
        #     ]
        #     mycursor.executemany(sql, val)
        #     mydb.commit()

        print('Do you want to show the result?(Yes/No)')
        ans = input()
        if ans == 'Yes' or ans == 'yes' or ans == 'y' or ans == 'Y':
            print("Reporting the records of home_Features Database")
            print("--------------------------------------------")
            print("There are ", len(result), " records in the Database.")
            print("")
            c = 0
            print('{0:^30s}{1:^20s}{2:^20s}{3:^20s}'.format('نام منطقه', 'مساحت خانه', 'تعداد اتاق', 'قیمت خانه'))
            print(
                '--------------------------------------------------------------------------------------------------------')
            for x in result:
                c += 1
                print(c,'{0:^25s}{1:^20d}{2:^20d}{3:^30d}'.format(x[0], x[1], x[2], x[3]))
    ####-----------------------------OPTION 2 IMPLEMENTATION---------------------------------####
    if option==2:
        import ML_Functions


    ####-----------------------------OPTION 3 IMPLEMENTATION---------------------------------####
    if option==3:
        # print('Please Enter your URL:')
        # u = input().strip()
        print('Please Enter the number of pages:')
        np = int(input())

        stmt = "SHOW TABLES LIKE 'home_Features'"
        mycursor.execute(stmt)
        result = mycursor.fetchone()
        if result:
            mycursor.execute("Drop TABLE home_Features")
            mycursor.execute("CREATE TABLE home_Features (Location VARCHAR(255), Area INT, BED INT, Price BIGINT)")  # Build_Age Was removed

        print("Gathering Data From ihome.ir ...")

        Web_Scraping_ihome(np)

        print('Do you want to show the result?(Yes/No)')
        ans = input()
        if ans == 'Yes' or ans == 'yes' or ans == 'y' or ans == 'Y':
            show_DB()
    #######_______________________________________________________________________#########
    if option==4:
        show_DB()
    if option==5:
        Ex = False





