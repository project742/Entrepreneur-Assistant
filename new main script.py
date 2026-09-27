import mysql.connector as ms
from tabulate import tabulate
from time import sleep
from datetime import date
from random import randint
import smtplib
from sys import exit
x=ms.connect(host="localhost",user="root",passwd="root",database="arun")
cur=x.cursor()
def check_date():
    date = input("Enter Date (DD-MM-YYYY) : ")
    if len(date) == 10 and date[2] == "-" and date[-5] == "-":

        return True,date
    else:
        print("Invalid date format")
        return False,date
def check_email():# dont forget to check the max len of gmail
    global email
    email = input("Enter your email:")
    if len(email)<=39 and "@" in email and "." in email:
        return True,email
    else:
        print("Invalid email.")
        return False,email
def add_uid(letter,column,table,user_cur=None,admin=True):
    if admin:
        cur.execute("Select " + column + " from " + table)
        data = cur.fetchall()
        if len(data) == 0:
            return letter + "001"
        last_id = data[-1][0]
        n = int(last_id[1:]) + 1
        if n < 10:
            return letter + "00" + str(n)
        elif n < 100:
            return  letter + "0" + str(n)
        else:
            return letter + str(n)
    else:
        user_cur.execute("select " + column + " from " + table)
        data = user_cur.fetchall()
        if len(data) == 0:
            return letter + "001"
        last_id = data[-1][0]
        n = int(last_id[1:]) + 1
        if n < 10:
            return letter + "00" + str(n)
        elif n < 100:
            return  letter + "0" + str(n)
        else:
            return letter + str(n)
def send_notification(receiver_email,message):
    sender_email = "project562009@gmail.com"
    sender_password = "kauv scql mbtd rabk"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        print("Otp sent successfully")
        return otp
    except:
        print("Unable to send OTP. Please enter a valid email.")
        return
    print("If You didn't received the otp then enter some alphabets which menas that your email is invalid")
def user_menu(uname):
    cur.execute("Create database if not exists "+uname)
    user_x = ms.connect(host="localhost",user="root",passwd="root",database=uname)
    user_cur = user_x.cursor()            
    while True:
        print("Press 1 ----> View Business")
        print("Press 2 ----> My Business")
        print("Press 3 ----> Back")
        choice = input("Enter the choice:")
        if choice == "1":
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
                        data=cur.fetchone()
                        if data is None:
                            print("Business Not Found,Enter a valid business ID")
                            continue
                        print(tabulate([["Business Name", data[1]],["Startup Cost",
                        str(data[3]) + " - " + str(data[4]) + " Lakhs"],
                        ["Skills Required", data[5]],["Demand", data[-2]],["Risk", data[-1]],
                        ["License", data[-3]]], headers=["DETAIL", "INFORMATION"], tablefmt="grid"))
                elif choice == "3":
                    amount=input("Enter the Startup amount:")
                    if amount.isdigit():
                        cur.execute("Select B_NAME,COST_LM,SKILLS,LICENSE,DEMAND,RISK from business_ideas where COST_LM <= %s"%(amount,))
                        data = cur.fetchall()
                        if len(data) > 0:
                            print(tabulate(data,headers=["B_Name","Startup Cost","Skills Required","License","Demand","Risk"],tablefmt="grid"))
                        else:
                            print("Sorry,We Have No Business for Your investment")
                    else:
                        print("Amount must contain only numbers")
                elif choice == "4":
                    departments = list()
                    cur.execute("Select  distinct DEPT from business_ideas")
                    for i in cur.fetchall():
                        for j in i:
                            departments +=[j.lower()]
                    print(departments)
                    dept=input("Enter the department you want:")
                    if dept.lower() in departments:
                        cur.execute("""Select B_Name,Skills,Cost_LM,Demand,Risk,License from
                        business_ideas where dept = '%s'"""%(dept,))
                        data=cur.fetchall()
                        print(tabulate(data,headers=["B_Name","Skills Required","Startup Cost",
                        "Skills","Demand","Risk","License"],tablefmt="grid"))
                    else:
                        print("Invalid Department")
                elif choice == "5":
                    while True:
                        print("Suggesting Business")
                        print("\n========================================")
                        print("          SUGGEST BUSINESS")
                        print("========================================")
                        # Q1 - INVESTMENT
                        while True:
                            print("\n1. How much are you willing to invest?")
                            print("1. ₹20,000 - ₹50,000")
                            print("2. ₹50,000 - ₹75,000")
                            print("3. ₹75,000 - ₹1 Lakh")
                            print("4. ₹1 Lakh - ₹2 Lakhs")
                            print("5. Above ₹2 Lakhs")
                            print("Leave it Blank to go to previous menu")
                            choice = input("Enter your choice: ")
                            if choice == "1":
                                min_investment = 20000
                                max_investment = 50000
                            elif choice == "2":
                                min_investment = 50000
                                max_investment = 75000
                            elif choice == "3":
                                min_investment = 75000
                                max_investment = 100000
                            elif choice == "4":
                                min_investment = 100000
                                max_investment = 200000
                            elif choice == "5":
                                min_investment = 200000
                                max_investment = 100000000
                            elif len(choice) == 0:
                                pass
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
                            break
                        # Q2 - TIME
                        while True:
                            print("\n2. How much time can you spend on the business?")
                            print("1. Part Time")
                            print("2. Full Time")
                            choice = input("Enter your choice: ")
                            if choice == "1":
                                time_req = "Part Time"
                            elif choice == "2":
                                time_req = "Full Time"
                            elif len(choice) == 0:
                                break
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
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
                                dept = "Healthcare"
                            elif choice == "9":
                                dept = "Tourism"
                            elif choice == "10":
                                dept = "Fitness"
                            elif len(choice) == 0:
                                break
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
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
                            elif len(choice) == 0:
                                break
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
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
                            elif len(choice) == 0:
                                break
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
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
                            elif len(choice) == 0:
                                break
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
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
                            elif len(choice) == 0:
                                break
                            elif len(choice) == 0:
                                break
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
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
                            elif len(choice) == 0:
                                break
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
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
                            elif len(choice) == 0:
                                break
                            else:
                                print("Invalid choice.")
                                continue
                            break
                        if len(choice) == 0:
                            break
                        cur.execute("""Select B_ID,B_NAME,DEPT,COST_LM,COST_UP,DEMAND,RISK,LICENSE,TIME_REQ,SKILLS,
                        CUSTOMERS,LOCATION,TEAM_SIZE,MODEL from business_ideas natural join business_details """)
                        businesses = cur.fetchall()
                        results = list()
                        for b in businesses:
                            score = 0
                            # INVESTMENT
                            if b[4] >= min_investment and b[3] <= max_investment:
                                score += 1
                            # TIME
                            if b[8] == time_req:
                                score += 1
                            # DEPARTMENT
                            if b[2] == dept:
                                score += 1
                            # SKILLS
                            if skill.lower() in b[9].lower():
                                score += 1
                            # CUSTOMERS
                            if b[10] == customer or customer == "Anyone":
                                score += 1
                            # LOCATION
                            if b[11] == location or location == "Any Location":
                                score += 1
                            # RISK
                            if b[6] == risk:
                                score += 1
                            # TEAM
                            if b[12] == team:
                                score += 1
                            # BUSINESS MODEL
                            if b[13] == model or model == "No Preference":
                                score += 1
                            percentage = (score/9) * 100
                            results.append((percentage, b))
                        results.sort(reverse=True)
                        print("\n========================================")
                        print("       YOUR BUSINESS SUGGESTIONS")
                        print("========================================")
                        if len(results) == 0:
                            print("No businesses available.")
                            break
                        count = 0
                        table = []
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
                            table.append([count,b[1],emoji + " " + str(int(percentage)) + "%",b[2],"₹" + str(b[3]) +
                            " - ₹" + str(b[4]),b[5],b[6],b[9],b[10],b[11],b[12],b[13]])
                            if count == 10:
                                break
                        print("\n========================================")
                        print("       YOUR BUSINESS SUGGESTIONS")
                        print("========================================")
                        print(tabulate(table,headers=["No.", "Business", "Match Score", "Department","Investment",
                        "Demand", "Risk", "Skills","Customers", "Location", "Team Size", "Model"],tablefmt="grid"))
                        print("\n========================================")
                        print("Suggestions are based on your answers.")
                        print("========================================")
                        break
                elif choice == "6":
                    break
                else:
                    print("Invalid Input")
        elif choice == "2":
            # Tables for business details
            user_cur.execute("""Create table if not exists workers(W_ID varchar(10),W_NAME varchar(30),
            POST varchar(30),JOIN_DATE date,EMAIL varchar(40))""")
            user_cur.execute("""Create table if not exists attendance(w_id varchar(10),Date varchar(2),
            Month varchar(15
            ),Year Varchar(4),Status varchar(10))""")
            user_cur.execute("""Create table if not exists post(P_ID varchar(10),Post varchar(30),Salary varchar(10))""")
            user_cur.execute("""Create table if not exists sal_attendance(w_id varchar(10),Year varchar(4),
            Month varchar(15),Present_Days varchar(2))""")
            user_cur.execute("Create table if not exists paid_leaves(days varchar(2))") 
            while True:
                print("\n==========================================")
                print("          MY BUSINESS MANAGEMENT")
                print("==========================================")
                print("Press 1 ----> Workers Management")
                print("Press 2 ----> Attendance")
                print("Press 3 ----> Salary Allotting")
                print("Press 4 ----> Sales Management")
                print("Press 5 ----> Sales Report")
                print("Press 6 ----> Product Management")
                print("Press 7 ----> Back")
                choice = input("\nEnter your choice : ")
                if choice == "1":
                    print("\n==========================================")
                    print("          WORKERS MANAGEMENT")
                    print("==========================================")
                    while True:
                        print("\nPress 1 ----> View Worker")
                        print("Press 2 ----> Add Worker")
                        print("Press 3 ----> Update Worker")
                        print("Press 4 ----> Delete Worker")
                        print("Press 5 ----> Back")
                        choice = input("\nEnter your choice : ")
                        if choice == "1":
                            user_cur.execute("Select * from workers")
                            records = user_cur.fetchall()
                            if len(records) > 0:
                                print("\n================ WORKERS =================")
                                print(tabulate(records,headers=["W_ID", "W_NAME", "POST", "JOIN_DATE", "EMAIL"],
                                tablefmt="grid"))
                            else:
                                print("\nNo workers found.")
                        elif choice == "2":
                            print("\n----------- ADD WORKER -----------")
                            wid = add_uid("W","W_ID","Workers",user_cur,False)
                            name = input("Enter Worker Name : ")
                            post = input("Enter Post : ")
                            join_date = input("Enter Joining Date (YYYY-MM-DD) : ")
                            if len(join_date) == 10 and join_date[4] == "-" and join_date[7] == "-":
                                pass
                            else:
                                print("Invalid date format. Enter as YYYY-MM-DD.")
                                continue
                            ok,email=check_email()
                            if ok:
                                otp = randint(100000, 999999)
                                message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                                send_notification(email,message)
                            else:
                                break
                            print("Enter the  received OTP in your new email account for email verification")
                            print("If you havent got any OTP then your email is invalid type something to get out of this...")
                            entered_otp = input("Enter the OTP: ")
                            if str(otp) == entered_otp:
                                print("OTP Verified Successfully")
                            else:
                                print("Incorrect OTP")
                                print("Failed To Add The Worker")
                                continue
                            user_cur.execute("Insert into workers VALUES ('%s','%s','%s','%s','%s')"%
                            (wid, name, post, join_date, email))
                            user_x.commit()
                            print("\nWorker added successfully.")
                        # UPDATE WORKER
                        elif choice == "3":
                            print("\n----------- UPDATE WORKER -----------")
                            wid = input("Enter Worker ID to update : ")
                            user_cur.execute("Select * from workers where W_ID = '%s'"%(wid,))
                            if user_cur.fetchone() is not None:
                                while True:
                                    print("\n1. Update Name")
                                    print("2. Update Post")
                                    print("3. Update Joining Date")
                                    print("4. Update Email")
                                    print("5. Back")
                                    update_choice = input("\nEnter your choice : ")
                                    if update_choice == "1":
                                        name = input("Enter new Worker Name : ")
                                        user_cur.execute("Update workers set W_NAME = '%s' where W_ID = '%s'"%
                                        (name, wid))
                                        user_x.commit()
                                        print("\nWorker name updated successfully.")
                                    elif update_choice == "2":
                                        post = input("Enter new Post : ")
                                        user_cur.execute("Update workers set POST = '%s' where W_ID = '%s'"%
                                        (post, wid))
                                        user_x.commit()
                                        print("\nWorker post updated successfully.")
                                    elif update_choice == "3":
                                        join_date = input("Enter new Joining Date (YYYY-MM-DD) : ")
                                        if len(join_date) == 10 and join_date[4] == "-" and join_date[7] == "-":
                                            pass
                                        else:
                                            print("Invalid date format. Enter as YYYY-MM-DD.")
                                            continue
                                        user_cur.execute("Update workers set JOIN_DATE = '%s' where W_ID = '%s'"%
                                        (join_date, wid))
                                        user_x.commit()
                                        print("\nJoining date updated successfully.")
                                    elif update_choice == "4":
                                        ok,email=check_email()
                                        if ok:
                                            otp = randint(100000, 999999)
                                            message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                                            send_notification(email,message)
                                        else:
                                            break
                                        print("Enter the  received OTP in your new email account for email verification")
                                        print("If you havent got any OTP then your email is invalid type something to get out of this...")
                                        entered_otp = input("Enter the OTP: ")
                                        if str(otp) == entered_otp:
                                            print("OTP Verified Successfully")
                                        else:
                                            print("Incorrect OTP")
                                            print("Failed To Add The Worker")
                                            continue
                                        user_cur.execute("Update workers set EMAIL='%s' where W_ID = '%s'"%
                                        (email, wid))
                                        user_x.commit()
                                        print("\nEmail updated successfully.")
                                    elif update_choice == "5":
                                        break
                                    else:
                                        print("\nInvalid Input.")
                            else:
                                print("\nWorker ID not found.")
                        # DELETE WORKER
                        elif choice == "4":
                            print("\n----------- DELETE WORKER -----------")
                            wid = input("Enter Worker ID to delete : ")
                            user_cur.execute("Select W_ID from workers where W_ID = '%s'"%(wid,))
                            if user_cur.fetchone() is None:
                                print("\nWorker ID not found.")
                                continue
                            sure=input("Are you sure to delete (Y/N) :").lower()
                            if sure == "y":
                                user_cur.execute("Delete from workers where w_ID='%s'"%(wid,))
                                user_x.commit()
                                print("User deleted successfully")
                                user_cur.execute("Select w_id from workers")
                                data = user_cur.fetchall()
                                n = int(wid[1:])
                                for row in data:
                                    old_id = row[0]
                                    number = int(old_id[1:])
                                    if number > n:
                                        number = number - 1
                                        if number < 10:
                                            new_id = "W00" + str(number)
                                        elif number < 100:
                                            new_id = "W0" + str(number)
                                        else:
                                            new_id = "W" + str(number)
                                        user_cur.execute("Update workers set W_ID = '%s' where W_ID ='%s'"%
                                        (new_id, old_id))
                                user_x.commit()
                            else:
                                print("Deletion cancelled")
                        # BACK
                        elif choice == "5":
                            break
                        else:
                            print("\nInvalid Input.")
                elif choice == "2":
                    months={"01":"January","02":"February","03":"March","04":"April","05":"May","06":"June","07":"July",
                            "08":"August","09":"September","10":"October","11":"November","12":"December"}
                    print("\n==========================================")
                    print("              ATTENDANCE")
                    print("==========================================")
                    wid = input("Enter Worker ID : ")
                    user_cur.execute("select w_id from workers where w_id = '%s'"%(wid,))
                    worker = user_cur.fetchone()
                    if worker is None:
                        print("Worker not found.")
                        continue
                    while True:
                        print("\nPress 1 ----> View ")
                        print("Press 2 ----> Mark ")
                        print("Press 3 ----> Delete")
                        print("Press 4 ----> Back")
                        choice = input("\nEnter your choice : ")
                        # View attendance
                        if choice == "1":
                            user_cur.execute("""select * from attendance where w_id ='%s'""" % (wid,))
                            record = user_cur.fetchall()
                            if len(record) == 0 :
                                print("No attendance found for", wid)
                            else:
                                print(tabulate(record,headers=["Worker ID","Date","Month","Year","Status"],
                                tablefmt="grid"))
                        # Mark Attendance
                        elif choice == "2":
                            ok,entered_date = check_date()
                            if ok:
                                user_cur.execute("""Select w_id,date from attendance where w_id='%s'and date='%s'
                                and month='%s' and year='%s'"""%(wid,entered_date[:2],months[entered_date[3:5]],
                                entered_date[6:]))
                                data = user_cur.fetchall()
                                if len(data) != 0 :
                                    print("\nAttendance for",wid,"on",entered_date,"already exist")
                                    continue
                                print("1 ----> Present")
                                print("2 ----> Absent")
                                choice = input("Enter the status:").lower()
                                if choice == "1":
                                    status = "present"
                                    user_cur.execute("""Select * from sal_attendance where w_id='%s' and year='%s'
                                    and month='%s'"""%(wid,entered_date[6:],months[entered_date[3:5]]))
                                    data=user_cur.fetchall()
                                    if len(data) == 0:
                                        present_days="1"
                                        user_cur.execute("""Insert into sal_attendance values('%s','%s','%s','%s')
                                        """%(wid,entered_date[6:],months[entered_date[3:5]],present_days))
                                    else:
                                        present_days=data[0][-1]
                                        present_days=str(int(present_days) + 1)
                                        user_cur.execute("""Update sal_attendance set present_days='%s' where
                                        w_id='%s' and year='%s' and month='%s'"""%(present_days,wid,entered_date[6:],
                                        months[entered_date[3:5]]))
                                    user_x.commit()
                                elif choice == "2":
                                    status = "absent"
                                else:
                                    print("Invalid choice")
                                    continue
                                user_cur.execute("Insert into attendance values('%s','%s','%s','%s','%s')"%
                                (wid,entered_date[:2],months[entered_date[3:5]],entered_date[6:],status))
                                user_x.commit()
                                print("Attendance Marked Successfully")
                            else:
                                continue
                        elif choice == "3": # Delete Attendance
                            while True:
                                print("Press 1 ----> To Delete by Month")
                                print("Press 2 ----> To Delete by Year")
                                print("Press 3 ----> Back")
                                choice = input("Enter the choice:")
                                if choice  == "1":
                                    print(months)
                                    month=input("Enter the month's key:")
                                    if month not in months:
                                        print("Invalid month key")
                                        continue
                                    user_cur.execute("Select * from attendance where month='%s'"%(months[month]))
                                    data=user_cur.fetchall()
                                    if len(data) == 0:
                                        print("No records are found in the month of",months[month])
                                        continue
                                    sure=input("Are you sure(Yes/No):").lower()
                                    if sure == "yes":
                                        user_cur.execute("Delete from attendance  where month='%s'"%
                                        (months[month]))
                                        user_cur.execute("Delete from sal_attendance where month='%s'"%
                                        (months[month]))
                                        user_x.commit()
                                        print("Attendance Deleted Successfully")
                                    else:
                                        print("Deletion Cancelled")
                                elif choice == "2":
                                    year=input("Enter the year:")
                                    if not year.isdigit():
                                        print("Year must contains digits")
                                        continue
                                    user_cur.execute("Select * from attendance where year='%s'"%(year))
                                    data=user_cur.fetchall()
                                    if len(data) == 0:
                                        print("No records are found in the year of",year)
                                        continue
                                    sure=input("Are you sure(Yes/No):").lower()
                                    if sure == "yes":
                                        user_cur.execute("Delete from attendance  where year='%s'"%
                                        (year))
                                        user_cur.execute("Delete from sal_attendance  where year='%s'"%
                                        (year))
                                        user_x.commit()
                                        print("Attendance Deleted Successfully")
                                    else:
                                        print("Deletion Cancelled")
                                elif choice =="3":
                                    break
                                else:
                                    print("Invalid Input")
                        elif choice == "4": # back
                            break
                        else:
                            print("Invalid Input")
                elif choice == "3":
                    print("\n==========================================")
                    print("           SALARY ALLOTTING")
                    print("==========================================")
                    while True:
                        print("Press 1 ----> Manage Salary details (as per post)")
                        print("Press 2 ----> To check the paid leaves")
                        print("Press 3 ----> Generate salary")
                        print("Press 4 ----> Back")
                        choice = input("\nEnter your choice : ")
                        if choice == "1":
                            while True:
                                print("Press 1 ----> View All Post")
                                print("Press 2 ----> Add Post")
                                print("Press 3 ----> Update Post")
                                print("Press 4 ----> Delete Post")
                                print("Press 5 ----> Back")
                                choice = input("Enter the choice:")
                                if choice == "1":
                                    user_cur.execute("Select * from Post")
                                    posts = user_cur.fetchall()
                                    if len(posts) == 0:
                                        print("No Post Found")
                                        continue
                                    print(tabulate(posts,headers=["Post ID","Post","Salary"],tablefmt="grid"))
                                elif choice == "2":
                                    post = input("Enter the Post:")
                                    salary = input("Enter the Salary:")
                                    if  not salary.isdigit():
                                        print("Salary must contains numbers")
                                        continue
                                    user_cur.execute("Insert into Post values('%s','%s','%s')"%
                                    (add_uid("P","P_ID","Post",user_cur,False),post,salary))
                                    print("Post Added Successfully")
                                elif choice == "3":
                                    pid=input("Enter the Post ID:")
                                    user_cur.execute("Select P_ID from Post where P_ID='%s'"%(pid))
                                    posts = user_cur.fetchall()
                                    if len(posts) == 0:
                                        print("Invalid Post ID")
                                        continue
                                    print("Press 1 ----> To update Post")
                                    print("Press 2 ----> To update Salary")
                                    choice = input("Enter the choice:")
                                    if choice =="1":
                                        post = input("Enter the Post:")
                                        user_cur.execute("Update Post set Post ='%s' where P_Id ='%s'"%(post,pid))
                                    elif choice == "2":
                                        salary = input("Enter the Salary:")
                                        if  not salary.isdigit():
                                            print("Salary must contains numbers")
                                            continue
                                        user_cur.execute("Update Post set Salary ='%s' where P_Id ='%s'"%(salary,pid))
                                    else:
                                        print("Invalid choice")
                                        continue
                                    user_x.commit()
                                    print("Post Details Updated Successfully")
                                elif choice == "4":
                                    pid = input("Enter the Post ID:")
                                    user_cur.execute("Select P_ID from Post where P_ID='%s'"%(pid))
                                    posts = user_cur.fetchall()
                                    if len(posts) == 0:
                                        print("Invalid Post ID")
                                        continue
                                    sure = input("Are You sure to Delete(Yes/No):")
                                    if sure.lower() == "yes":
                                        user_cur.execute("Delete from Post where P_ID = '%s'"%(pid))
                                        user_x.commit()
                                        print("Post Deleted Successfully")
                                    else:
                                        print("Deletion Cancelled")
                                elif choice == "5":
                                    break
                                else:
                                    print("Invalid Choice")
                        elif choice == "2": # Paid Leaves
                            print("Current Setting")
                            user_cur.execute("Select * from Paid_leaves")
                            days=user_cur.fetchall()
                            print(tabulate(days,headers=["No Of Unpaid Days"],tablefmt="grid"))
                            print("Leave it empty to just view it")
                            print("Give the input if you need to update")
                            paid_leaves=input("Enter the no of Paid Leaves(for a month):")
                            if not paid_leaves.isdigit():
                                print("No of days should be a number")
                                continue
                            if len(paid_leaves) not in (1,2):
                                print("It must contains 1 or 2 digits only")
                                continue
                            user_cur.execute("Update paid_leaves set days='%s'"%(paid_leaves,))
                            user_x.commit()
                            print("Paid Leaves updated successfully")
                        elif choice == "3":
                            pass
                        elif choice == "4":
                            break
                        else:
                            print("Invalid Input")
                elif choice == "4":
                    print("\n==========================================")
                    print("           SALES MANAGEMENT")
                    print("==========================================")
                    while True:
                        print("1. Add Sale")
                        print("2. Update Sale")
                        print("3. Delete Sale")
                        print("4. View Sales")
                        print("5. Back")
                        choice = input("\nEnter your choice : ")
                        if choice == "1":
                            pass
                        elif choice == "2":
                            pass
                        elif choice == "3":
                            pass
                        elif choice == "4":
                            pass
                        elif choice == "5":
                            break
                        else:
                            print("Invalid Input")
                elif choice == "5":
                    print("\n==========================================")
                    print("              SALES REPORT")
                    print("==========================================")
                    while True:
                        print("1. Daily Sales Report")
                        print("2. Monthly Sales Report")
                        print("3. Product-wise Sales Report")
                        print("4. Total Sales")
                        print("5. Low Stock Alert Settings")
                        print("6. Back")
                        choice = input("\nEnter your choice : ")
                        if choice == "1":
                            pass
                        elif choice == "2":
                            pass
                        elif choice == "3":
                            pass
                        elif choice == "4":
                            pass
                        elif choice == "5":
                            pass
                        elif choice == "6":
                            break
                        else:
                            print("Invalid Input")
                elif choice == "6":
                    print("\n==========================================")
                    print("          PRODUCT MANAGEMENT")
                    print("==========================================")
                    while True:
                        print("1. Add Product")
                        print("2. Update Product")
                        print("3. Delete Product")
                        print("4. View Products")
                        print("5. Search Product")
                        print("6. Back")
                        choice = input("\nEnter your choice : ")
                        if choice == "1":
                            pass
                        elif choice == "2":
                            pass
                        elif choice == "3":
                            pass
                        elif choice == "4":
                            pass
                        elif choice == "5":
                            pass
                        elif choice == "6":
                            break
                        else:
                            print("Invalid Input")
                elif choice == "7":
                    break
                else:
                    print("Invalid Input")
        elif choice == "3":
            break
        else:
            print("Invalid Choice")
print("="*92 + "\n\t\t\t\tENTREPRENEUR ASSISTANT\n" + "="*92) 
while True:
    print("1 ---> Admin login")
    print("2 ---> User login")
    choice=input("Enter Your Option: ")

    if choice == "1":
        admin_attempts = 1
        while True:
            print("\nAdmin Login")
            print(admin_attempts,"of 3 attempts")
            admin_name = input("Enter admin ID: ")
            admin_password = input("Enter password: ")

            if admin_name == "arun" and admin_password == "1234":
                print("Admin login successful!")
                break

            admin_attempts += 1

            if admin_attempts == 4:
                print("\nToo many unsuccessful login attempts.")
                print("Account has been locked due to security issues.")
                cur.execute("Select email from admin_details")
                email=cur.fetchall()[0]
                otp = randint(100000, 999999)
                message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                send_notification(email,message)
                print("OTP has been sent to your email.")
                entered_otp = input("Enter OTP: ")

                if entered_otp == str(otp):
                    print("OTP verified successfully.")
                    break
                else:
                    print("Incorrect OTP.")
                    print("Exiting Program...")
                    exit()

            else:
                print("Invalid admin ID or password.")
                print("Please try again.")
                    
        print("Welcome Admin")
        print("Admin Dashboard")
        while True:
            print("Press 1 ----> Manage Business Ideas")
            print("Press 2 ----> Manage Users")
            print("Press 3 ----> Change Your Email")
            print("Press 4 ----> Back")
            choice=input("Enter the option:")
            
            if choice == "1":
                print("Time to manage the business")
                continue
            elif choice == "2":
                while True:
                    print("Managing Users")
                    print("Time to manage the users")
                    print("Press 1 -----> View User Details")
                    print("Press 2 -----> Add a User")
                    print("Press 3 -----> Update User")
                    print("Press 4 -----> Delete a  User")
                    print("Press 5 -----> Back")
                    choice=input("Enter the choice:")
                    
                    if choice == "1": # Viewing User
                        print("Viewing users")
                        cur.execute("Select * from user_ids")
                        data=cur.fetchall()
                        if len(data)>0:
                            print("Showing User Id Details...")
                            print(tabulate(data, headers=["User ID","User Name",
                            "Password","Attempts","Email"],tablefmt="grid"))
                            continue
                        else:
                            print("No Users Found")
                            continue
                    elif choice == "2":  # Adding User
                        uid = add_uid("U","u_id","user_ids")
                        cur.execute("Select User_name from user_ids where U_ID='%s'"%(uid,))
                        user_name=input("Enter the User Name:")
                        password=input("Enter the password:")
                        ok,email=check_email()
                        if ok:
                            otp = randint(100000, 999999)
                            message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                            send_notification(email,message)
                            print("To verify the email is exist or not")
                            print("If you did't receive the OTP then your email doen't exist,just press any alphabet to get out of this")
                            entered_otp = input("Enter the OTP:")
                            if str(otp) == entered_otp:
                                print("OTP verified successfully")
                                cur.execute("""Insert into user_ids values
                                ('%s','%s','%s','%s','%s')"""%
                                (uid,user_name,password,"Unlocked",email))
                                x.commit()
                                print("User added successfully")
                            else:
                                print("Incorrect OTP")
                        else:
                            break
                    elif choice == "3":
                        uid=input("Enter the User ID to update:")
                        while True:# Updating User
                            print("Press 1 ----> To update User Name")
                            print("Press 2 ----> To update Password")
                            print("Press 3 ----> To update the Status")
                            print("Press 4 ----> To update Email")
                            print("Press 5 ----> Back")
                            cur.execute("Select User_name from user_ids where U_ID='%s'"%(uid,))
                            if cur.fetchone() is  None:
                                print("User ID Not Found,Enter already existing User ID")
                                break
                            choice=input("Enter your choice from above (1,2,3,4):")
                            if choice == "1":
                                uname=input("Enter the user name:")
                                cur.execute("update user_ids set User_name = '%s' where u_id='%s'"
                                %(uname,uid))
                                print("User name updated successfully")
                            elif choice == "2":
                                password=input("Enter the password:")
                                cur.execute("""update user_ids set password = '%s'
                                where u_id='%s'"""%(password,uid))
                                print("Password updated successfully")
                            elif choice == "3":
                                status = {1:"Locked",2:"Unlocked"}
                                print(status)
                                option = input("Enter the Status (1 or 2):")
                                if option == "1":
                                    cur.execute("Update user_ids set status = '%s' where u_id='%s'"
                                    %(status[1],uid))
                                elif option == "2":
                                    cur.execute("Update user_ids set status = '%s' where u_id='%s'"
                                    %(status[2],uid))
                                else:
                                    print("Invalid Input")
                                    continue
                                x.commit()
                                print("Status updated succesfully")
                            elif choice == "4":
                                ok,email= check_email()
                                if ok: 
                                    otp = randint(100000, 999999)
                                    message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                                    send_notification(email,message)
                                    entered_otp = input("Enter the OTP:")
                                    if str(otp) == entered_otp:
                                        print("OTP verified successfully")
                                        cur.execute("""update user_ids set email = '%s'
                                        where u_id='%s'"""%(email,uid))
                                        print("Email updated successfully")
                                    else:
                                        print("Incorrect OTP")
                                continue
                            elif choice == "5":
                                break
                            else:
                                print("Invalid input")
                                break
                            continue
                    elif choice == "4": # Deleting User
                        uid=input("Enter the User ID:")
                        cur.execute("Select User_name from user_ids where U_ID='%s'"%(uid,))
                        if cur.fetchone() is  None:
                            print("User ID not found, Enter the already existing User ID")
                            continue
                        sure=input("Are you sure to delete (Y/N) :").lower()
                        if sure == "y":
                            cur.execute("Delete from user_ids where U_ID='%s'"%(uid,))
                            x.commit()
                            print("User deleted successfully")
                            cur.execute("Select u_id from User_ids")
                            data = cur.fetchall()
                            n = int(uid[1:])
                            for row in data:
                                old_id = row[0]
                                number = int(old_id[1:])
                                if number > n:
                                    number = number - 1
                                    if number < 10:
                                        new_id = "B00" + str(number)
                                    elif number < 100:
                                        new_id = "B0" + str(number)
                                    else:
                                        new_id = "B" + str(number)
                                    cur.execute("""Update User_ids set U_ID = '%s' where U_ID ='%s'"""%(new_id, old_id))
                            x.commit()
                            break
                        else:
                            print("Deletion cancelled")
                            break
                    elif choice == "5": #Back
                        break
                    else:
                        print("Invalid choice,Enter valid choice")
            elif choice == "3":
                cur.execute("Select email from admin_details")
                current_email = cur.fetchall()[0][0]
                print("Current Email :",current_email)
                while True:
                    ok,email=check_email()
                    if ok:
                        otp = randint(100000, 999999)
                        message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                        send_notification(email,message)
                    else:
                        break
                    print("Enter the  received OTP in your new email account for email verification")
                    print("If you havent got any OTP then your email is invalid type something to get out of this...")
                    entered_otp = input("Enter the OTP: ")
                    if str(otp) == entered_otp:
                        print("OTP Verified Successfully")
                        cur.execute("Update admin_details set email = '%s'"%email)
                        x.commit()
                        print("Email Updated Successffully")
                        break
                    else:
                        print("Incorrect OTP")
                        break
            elif choice == "4":
                    break
            else:
                print("Invalid input")
    elif choice == "2":
        print("User Login")
        while True:
            print("Press 1 ----> Create New Account")
            print("Press 2 ----> Signup")
            print("Press 3 ----> Back")
            choice = input("Enter the choice:")
            if choice == "1":
                uid = add_uid("U","u_id","user_ids")
                username = input("Enter the Username:")
                cur.execute("Select * from user_ids where user_name = '%s'"%(username,))
                if len(cur.fetchall()) > 0:
                    print("Username already Taken,Try another name")
                    continue
                password = input("Enter the Password:")
                ok,email=check_email()
                if ok:
                    otp = randint(100000, 999999)
                    message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                    send_notification(email,message)
                    entered_otp = input("Enter the OTP: ")
                    if entered_otp == str(otp):
                        print("OTP Verified Successfully")
                        cur.execute("""Insert into user_ids  (u_id,user_name,password,status,email) values
                        ('%s','%s','%s','%s','%s')"""%(uid,username,password,"Unlocked",email))
                        x.commit()
                        print("Account Created Successfully")
                        user_menu(username)
                    else:
                        print("Incorrect OTP")
                else:
                    pass
            elif choice == "2":
                attempts = 0
                username = input("Enter the username:")
                cur.execute("Select * from user_ids where user_name = '%s'"%(username,))
                data = cur.fetchall()
                if len(data) == 0:
                    print("Invalid Username")
                    continue
                account_status = data[0][-2]
                if account_status.lower() == "locked":
                    print("Account locked,Can't Access the Account.Contact Admin for further Details.")
                    continue
                while True:
                    attempts += 1
                    print("Attempt: " + str(attempts) + " of 3")
                    password = input("Enter the password:")

                    if data[0][2] == password: 
                        print("Account Found")
                        print("Welcome " + str(data[0][1]))
                        user_menu(username) # Function for user entire menu
                        break
                    else:
                        print("Invalid Password")
                        if attempts == 3:
                            print("Too many attempts..") #send notification to admin to change the no of attempts in the table"
                            print("\n-----------Security Alert-------------------")
                            print("Account Locked")
                            print("Contact Admin for the access of your account")
                            print("--------------------------------------------\n")
                            message = "Subject: Your Account Has Been Locked Due To Unauthorised Login"
                            send_notification(data[0][-1],message)
                            cur.execute("Update  user_ids set status = '%s' where user_name='%s'"%
                            ("Locked",username))
                            x.commit()
                            break
            elif choice == "3":
               break
            else:
                print("Invalid Input")
    else:
        print("Invalid input,try again")
"""
def loading_bar():
    print("Loading...")
    for i in range(5):
        print("███",end="")
        #print("⬤",end="")
        time.sleep(0.3)
def text_box(txt):
    n = len(txt)
    top = "╔" + " - " * n + "╗"
    mid = "║ " + txt +       " ║"
    bottom = "╚" + " - " * n + "╝"
    print(top)
    print(mid)
    print(bottom)
"""
# if u are changing a value of a variable inside a func then u need to declare it inside the func
#or u should give it as global inside the func
#but u dont need to do this for not changing the value
