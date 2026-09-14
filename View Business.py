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
        print("\n========================================")
        print("          SUGGEST BUSINESS")
        print("========================================")
        # Q1 - INVESTMENT
        while True:
            print("\n1. How much are you willing to invest?")
            print("1. Below 1 Lakh")
            print("2. 1 - 5 Lakhs")
            print("3. 5 - 10 Lakhs")
            print("4. 10 - 25 Lakhs")
            print("5. Above 25 Lakhs")
                
            choice = input("Enter your choice: ")

            if choice == "1":
                investment = 1
            elif choice == "2":
                investment = 5
            elif choice == "3":
                investment = 10
            elif choice == "4":
                investment = 25
            elif choice == "5":
                investment = 100
            else:
                print("Invalid choice.")
                continue
            break

        # Q2 - TIME
        while True:
            print("\n2. How much time can you spend on the business?")
            print("1. Part Time")
            print("4. Full Time")

            choice = input("Enter your choice: ")

            if choice == "1":
                time_req = "Part Time"
            elif choice == "2":
                time_req = "Full Time"
            else:
                print("Invalid choice.")
                continue
            break

        # Q3 - INTEREST
        while True:
            print("\n3. Which area interests you the most?")
            print("1. Food")
            print("2. Technology")
            print("3. Construction")
            print("4. Agriculture")
            print("5. Fashion")
            print("6. Entertainment")
            print("7. Education")
            print("8. Healthcare")
            print("9. Tourism")
            print("10. Fitness")

            choice = input("Enter your choice: ")

            if choice == "1":
                dept = "Food"
            elif choice == "2":
                dept = "Technology"
            elif choice == "3":
                dept = "Construction"
            elif choice == "4":
                dept = "Agriculture"
            elif choice == "5":
                dept = "Fashion"
            elif choice == "6":
                dept = "Entertainment"
            elif choice == "7":
                dept = "Education"
            elif choice == "8":
                dept = "Environment"
            elif choice == "9":
                dept = "Tourism"
            elif choice == "10":
                dept = "Fitness"
            else:
                print("Invalid choice.")
                continue
            break

        # Q4 - SKILLS
        while True:
            print("\n4. What are you good at?")
            print("1. Cooking")
            print("2. Computer")
            print("3. Manufacturing")
            print("4. Marketing")
            print("5. Management")
            print("6. Creative Work")
            print("7. Agriculture")
            print("8. No Specific Skill")

            choice = input("Enter your choice: ")

            if choice == "1":
                skill = "Cooking"
            elif choice == "2":
                skill = "Computer"
            elif choice == "3":
                skill = "Manufacturing"
            elif choice == "4":
                skill = "Marketing"
            elif choice == "5":
                skill = "Management"
            elif choice == "6":
                skill = "Creative"
            elif choice == "7":
                skill = "Agriculture"
            elif choice == "8":
                skill = "No Specific Skill"
            else:
                print("Invalid choice.")
                continue
            break

        # Q5 - CUSTOMERS
        while True:
            print("\n5. What type of customers would you prefer?")
            print("1. Local Customers")
            print("2. Students")
            print("3. Families")
            print("4. Businesses")
            print("5. Online Customers")
            print("6. Anyone")

            choice = input("Enter your choice: ")

            if choice == "1":
                customer = "Local Customers"
            elif choice == "2":
                customer = "Students"
            elif choice == "3":
                customer = "Families"
            elif choice == "4":
                customer = "Businesses"
            elif choice == "5":
                customer = "Online Customers"
            elif choice == "6":
                customer = "Anyone"
            else:
                print("Invalid choice.")
                continue
            break

        # Q6 - LOCATION
        while True:
            print("\n6. Where do you want to operate?")
            print("1. Home")
            print("2. Shop")
            print("3. Factory")
            print("4. Online")
            print("5. Any Location")

            choice = input("Enter your choice: ")

            if choice == "1":
                location = "Home"
            elif choice == "2":
                location = "Shop"
            elif choice == "3":
                location = "Factory"
            elif choice == "4":
                location = "Online"
            elif choice == "5":
                location = "Any Location"
            else:
                print("Invalid choice.")
                continue
            break

        # Q7 - RISK
        while True:
            print("\n7. How comfortable are you with risk?")
            print("1. Low")
            print("2. Medium")
            print("3. High")

            choice = input("Enter your choice: ")

            if choice == "1":
                risk = "Low"
            elif choice == "2":
                risk = "Medium"
            elif choice == "3":
                risk = "High"
            else:
                print("Invalid choice.")
                continue
            break

        # Q8 - TEAM
        while True:
            print("\n8. Do you want to work alone or with others?")
            print("1. Alone")
            print("2. 1-2 People")
            print("3. Small Team")
            print("4. Large Team")

            choice = input("Enter your choice: ")

            if choice == "1":
                team = "Alone"
            elif choice == "2":
                team = "1-2 People"
            elif choice == "3":
                team = "Small Team"
            elif choice == "4":
                team = "Large Team"
            else:
                print("Invalid choice.")
                continue
            break

        # Q9 - BUSINESS MODEL
        while True:
            print("\n9. What type of business do you prefer?")
            print("1. Selling Products")
            print("2. Providing Services")
            print("3. Making Products")
            print("4. Operating Online")
            print("5. No Preference")

            choice = input("Enter your choice: ")

            if choice == "1":
                model = "Selling Products"
            elif choice == "2":
                model = "Providing Services"
            elif choice == "3":
                model = "Making Products"
            elif choice == "4":
                model = "Operating Online"
            elif choice == "5":
                model = "No Preference"
            else:
                print("Invalid choice.")
                continue
            break

        # GET BUSINESS DETAILS
        cur.execute("""Select B_ID,B_NAME,DEPT,COST_LM,COST_UP,DEMAND,RISK,LICENSE,TIME_REQ,SKILLS,
        CUSTOMERS,LOCATION,TEAM_SIZE,MODEL from business_ideas natural join business_details """)
        businesses = cur.fetchall()
        results = []

        # CHECK EACH BUSINESS
        for b in businesses:
            score = 0

            if b[3] <= investment <= b[4]:
                score += 1

            if b[8] == time_req:
                score += 1

            if b[2] == dept:
                 score += 1

            if skill.lower() in b[9].lower():
                score += 1

            if b[10] == customer or customer == "Anyone":
                score += 1

            if b[11] == location or location == "Any Location":
                score += 1

            if b[6] == risk:
                score += 1

            if b[12] == team:
                score += 1

            if b[13] == model or model == "Any":
                score += 1

            percentage = (score / 9) * 100
            results.append((percentage, b))

        # SORT RESULTS
        results.sort(reverse=True)

        # DISPLAY TOP 3
        print("\n========================================")
        print("       YOUR BUSINESS SUGGESTIONS")
        print("========================================")

        if len(results) == 0:
            print("No businesses available.")
            continue

        count = 0
        for percentage, b in results:
            count += 1

            if percentage >= 80:
                emoji = "😄"
            elif percentage >= 60:
                emoji = "🙂"
            elif percentage >= 40:
                emoji = "😐"
            else:
                emoji = "🙁"

            print("\n", count, ".", b[1])
            print("Match Score :", emoji, round(percentage), "%")
            print("Department  :", b[2])
            print("Investment  :", b[3], "-", b[4], "Lakhs")
            print("Demand      :", b[5])
            print("Risk        :", b[6])
            print("Skills      :", b[9])
            print("Customers   :", b[10])
            print("Location    :", b[11])
            print("Team Size   :", b[12])
            print("Model       :", b[13])

            if count == 10:
                break

        print("\n========================================")
        print("Suggestions are based on your answers.")
        print("========================================")
            elif choice == "6":
                break
            else:
                print("Invalid Input")







    

