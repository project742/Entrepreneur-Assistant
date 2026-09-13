import mysql.connector
from tabulate import tabulate
x = mysql.connector.connect(host="localhost",user="root",password="root",database="arun")
cur = x.cursor()
while True:
    print("Press 1 ----> Business Book")
    print("Press 2 ----> Searching Business")
    print("Press 3 ----> Browse by Investment")
    print("Press 4 ----> Browse by Department")
    print("Press 5 ----> Suggest Business")
    print("Press 6 ----> Back")
    choice = input("Enter the choice:")
    if choice == "1":
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
                print("Invalid Input")

    elif choice == "2":
        cur.execute("select * from business_ideas")
        data=cur.fetchall()
        ids = []
        for i in data:
            ids.append(i[0])
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
    elif choice == "3":
        cur.execute("select * from business_ideas")
        data=cur.fetchall()
        ids = []
        for i in data:
            ids.append(i[0])
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
                
    elif choice == "4":
        departments=[]
        cur.execute("select distinct Dept from business_ideas")
        data=cur.fetchall()
        for i in data:
            for j in i:
                departments.append(j.lower())
        print(departments)
        dept=input("Enter the department you want:")
        if dept.lower() in departments:
            cur.execute("select * from business_ideas natural join business_ideas1 where dept = '%s' "%dept)
            data=cur.fetchall()
            print(tabulate(data,headers=["B_ID","B_Name",
            "Department","Cost LM","Cost UP","Skills","License","Demand","Risk"],tablefmt="psql"))
        else:
            print("Invalid Department")
                
    elif choice == "5":
        print("Suggesting Business")
    elif choice == "6":
        break
    else:
        print("Invalid Input")







    

