import mysql.connector
from tabulate import tabulate
x = mysql.connector.connect(host="localhost",user="root",password="root",database="arun")
cur = x.cursor()
#book
cur.execute("select B_ID, B_Name from business_ideas")
data = cur.fetchall()
i = 0
page=1
while True:
    print("\n"+"======================================== BUSINESS BOOK ==============================================\n")
    for j in range(10):
        if i + j < len(data):
            print("\t\t\t\t\t",data[i + j][0], "-", data[i + j][1])
    print("\n[P] Previous Page")
    print("[N] Next Page")
    print("[E] Exit")
    print("\t\t\t\t\t\t\t\t\t\t\tPage :",page)
    print("=====================================================================================================")
    choice = input("\n\nEnter choice: ")
    if choice.lower() == "n":
        if i + 10 < len(data):
            i += 10
            page += 1
        else:
            print("\nThis is the last page")
    elif choice.lower() == "p":
        if i >= 10:
            i -= 10
            page -= 1
        else:
            print("\nThis is the first page")
    elif choice.lower() == "e":
        break
    else:
        print("Inavlid Input")
cur.close()
x.close()


#searching business
"""cur.execute("select * from business_ideas")
data=cur.fetchall()
ids = []
ans = "y"
for i in data:
    ids.append(i[0])
    while ans.lower() == "y":
        Id=input("Enter the Business ID (as per mentioned in Business Book) :")
        if Id in ids:
            print("Searching Record...")
            cur.execute("select * from business_ideas where B_ID = '%s'"%Id)
            record = cur.fetchone()
            print(record[0] + "-" + record[1])
            print("Description : " + record[2])
            print("Risk : " + record[4])
            print("Demand : " + record[5])
        else:
            print("Business ID not found")
        ans=input("Press y to search more:")
"""   





    

