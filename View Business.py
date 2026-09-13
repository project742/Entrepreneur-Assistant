import mysql.connector
from tabulate import tabulate
x = mysql.connector.connect(host="localhost",user="root",password="root",database="arun")
cur = x.cursor()

departments=[]
        cur.execute("Select distinct Dept from business_ideas")
        data=cur.fetchall()
        for i in data:
            for j in i:
                departments.append(j.lower())
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
        page = 1
        while True:
            print("\n"+"======================================== BUSINESS BOOK ==============================================\n")
            for j in range(10):
                if i + j < len(data):
                    print("\t\t\t\t\t",data[i + j][0],"-",data[i + j][1])
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
            Id=input("Enter the Business ID (as per mentioned in Business Book) :")
            
            cur.execute("Select * from business_ideas where B_ID = '%s'"%Id)
            data=cur.fetchall()
            
            print("Searching Business...")
            if len(data) != 1:
                print("Business Not Found,Enter a valid business ID")
                continue
    
            print("------" + data[1] + "------")
            print("Startup cost :" + data[4] + "Lakh-" + data[5] + "Lakh")
            print("Skills Required :" + data[3])
            print("Demand : " + data[-3])
            print("Risk : " + data[-2])
            print("License : " + data[-1])
            
    elif choice == "3":
        print("Enter the Startup budget in lakhs")
        print("For Example : 50000 as 0.5 lakhs)
        amount=input("Enter the Startup amount(in lakhs):")
        print("Searching Record...")
        cur.execute("""Select B_Name,Skills,Cost_LM,Cost_UP,Demand,Risk,License from 
        business_ideas where Cost_LM <='%s' """%(amount[:3],))
        data = cur.fetchall()
        print(tabulate(data,headers=["B_Name","Skills Required","Startup Cost(From)",
        "Startup Cost(To)","Skills","Demand","Risk","License"],tablefmt="psql"))
        
    elif choice == "4":
        print(departments)
        dept=input("Enter the department you want:")
        if dept.lower() in departments:
            cur.execute("""Select B_Name,Skills,Cost_LM,Cost_UP,Demand,Risk,License from
            business_ideas where dept = '%s'"""%(dept,))
            data=cur.fetchall()
            print(tabulate(data,headers=["B_Name","Skills Required","Startup Cost(From)",
            "Startup Cost(To)","Skills","Demand","Risk","License"],tablefmt="psql"))
        else:
            print("Invalid Department")
                
    elif choice == "5":
        print("Suggesting Business")
    elif choice == "6":
        break
    else:
        print("Invalid Input")







    

