import re
import mysql.connector
import requests
from bs4 import BeautifulSoup
from sklearn import tree
from sklearn import preprocessing

def sql_conn(R):
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
    else:
        mycursor.execute("Drop TABLE home_Features")
        mycursor.execute(
            "CREATE TABLE home_Features (Location VARCHAR(255), Area INT, BED INT, Price BIGINT)")

    # Inserting Data to the DataBase ---------------------------------------------------------------------------

    for i in range(len(R)):
        sql = "INSERT INTO home_Features (Location, Area, BED, Price) VALUES (%s, %s, %s, %s)"
        val = [
            (R[i][0], R[i][1], R[i][2], R[i][3])
        ]
        mycursor.executemany(sql, val)
        mydb.commit()

#####------------------------------------------------------------------------------------------------------------------#####

def show_DB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="@Hmadre87"
    )
    mycursor = mydb.cursor()
    mycursor.execute('CREATE DATABASE IF NOT EXISTS home')
    mycursor.execute('USE home')
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

def CreateDB_ihome(No_Page):
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

    sql_conn(result)
#####--------------------------------------------------------------------------------------------------------------------#####

def home_search(location, num_page):
    page_no = 0
    result = []
    while page_no < num_page:
        page_no += 1
        url = 'https://www.ihome.ir/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/' + str(page_no)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        Location = soup.find_all('div', attrs={'class': 'location'})
        Area = soup.find_all('i', attrs={'class': 'ihome-arrows'})
        Bed = soup.find_all('i', attrs={"class": "ihome-bed"})
        Price = soup.find_all('div', attrs={'class': 'price'})
        Price = Price[1:]
        for i in range(len(Bed)):
            Lo = re.sub('\s+', ' ', Location[i].text).strip()
            Lo = re.sub('،','',Lo)
            if location in Lo:
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
            print(c, '{0:^25s}{1:^20d}{2:^20d}{3:^30d}'.format(x[0], x[1], x[2], x[3]))


def fetch_data(DB_Name,Table_Name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="@Hmadre87"
    )
    mycursor = mydb.cursor()
    stmt = "SHOW DATABASES LIKE '" + DB_Name +"'"
    mycursor.execute(stmt)
    r = mycursor.fetchone()
    if not r:
        print("There is no database named",DB_Name)
    else:
        st = 'USE ' + DB_Name
        mycursor.execute(st)
        stmt = "SHOW TABLES LIKE '"+ Table_Name +"'"
        mycursor.execute(stmt)
        t = mycursor.fetchone()
        if t:
            Sqlcommand = "Select * From " + Table_Name
            mycursor.execute(Sqlcommand)
            myresult = mycursor.fetchall()
            Fetched_Data = []
            for x in myresult:
                Fetched_Data.append(x)
        else:
            print("There is no Table named",Table_Name)
    return Fetched_Data


def Smart_Price_estimation(Loc, Ar, RN):
    Data = fetch_data('home','home_Features')
    if not Data:
        print("The Database does'nt have any records.\n Please run CREATE DATABASE option. ")
    ##----------------------------------------------------##
    #Preprocessing Data
    # create the Labelencoder object
    le = preprocessing.LabelEncoder()
    #convert the categorical columns into numeric
    s = []
    for x in range(len(Data)):
        s.append(Data[x][0])
    s_set = set(s)
    unique_s = list(s_set)
    for i in range(len(unique_s)):
        unique_s[i] = re.sub(r'، تهران','',unique_s[i])
    encoded_value = le.fit_transform(unique_s)
    ## END OF convert the categorical columns into numeric
    ## TRAIN THE MODEL
    Dic_Loc_Val = {}
    for i in range(len(unique_s)):
        Dic_Loc_Val[unique_s[i]] = encoded_value[i]
    x =[]
    y = []
    for each in Data:
        each = list(each)
        each[0]= re.sub(r'، تهران', '', each[0])
        if each[0] in Dic_Loc_Val.keys():
            each[0] = Dic_Loc_Val[each[0]]
        x.append(each[0:3])
        y.append(each[3])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x,y)

    if Loc in Dic_Loc_Val.keys():
        Loc_val = Dic_Loc_Val[Loc]
    else:
        print("The Location Name Is Not Available.")
        exit(1)

    new_data = [[Loc_val,Ar,RN]]
    answer = clf.predict(new_data)
    print('The Approximate Price For Intended Home is:',answer[0])
    return answer[0]
