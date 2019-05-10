import re
import mysql.connector
from sklearn import tree
from sklearn import preprocessing

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

Data = fetch_data('home','home_Features')
if not Data:
    print("The Database does'nt have any records.\n Please run CREATE New DATABASE option. ")
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
print("Please Enter Your Intended Location:(example: سعادت آباد)")
Loc = input()

if Loc in Dic_Loc_Val.keys():
    Loc_val = Dic_Loc_Val[Loc]
else:
    print("The Location Name Is Not Available.")
    exit(1)
print("Please Enter Your Intended Home Area:(example:150)")
Ar = int(input())
print("Please Enter Your Intended Room Number:(example:3)")
RN = int(input())
new_data = [[Loc_val,Ar,RN]]
answer = clf.predict(new_data)
print('The Approximate Price For Intended Home is: \t',answer[0],'\n')




