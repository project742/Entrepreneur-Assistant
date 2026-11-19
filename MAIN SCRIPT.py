import mysql.connector as ms
from tabulate import tabulate
import time 
from datetime import datetime
from random import randint
import smtplib
import sys
x=ms.connect(host="localhost",user="root",passwd="root",database="arun")
cur=x.cursor()
# Tables for admin 
cur.execute("""create table if not exists user_ids (u_id varchar(10),user_name varchar(40),password varchar(40),status varchar(10),
            email varchar(39))""")
cur.execute("create table if not exists admin_details (email varchar(39))")
cur.execute("Select * from admin_details")
data = cur.fetchall()
if len(data) == 0:
    cur.execute("Insert into admin_details values('idnetflix135@gmail.com')")
    x.commit()
#cur.execute("""create table if not exists business_ideas (b_id varchar(10),b_name varchar(40),dept varchar(30),cost_lm int,
            #skills varchar(100),license varchar(100),demand varchar(10),risk varchar(10))""")
# Tables for user
options={"1":"HIGH","2":"MEDIUM","3":"LOW"}
months={"01":"January","02":"February","03":"March","04":"April","05":"May","06":"June","07":"July",
        "08":"August","09":"September","10":"October","11":"November","12":"December"}
max_days={"January":31,"February":28,"March":31,"April":30,"May":31,"June":30,"July":31,"August":31,"September":30,
        "October":31,"November":30,"December":31}
def loading_bar(text,delay,space):
    print("\n")
    print("                                                   ⚙ PLEASE WAIT...")
    print(" "*space + text + "\n")
    print("                                              [",end="")
    for i in range(24): 
        print("█",end="")
        time.sleep(delay)
    print("] 100%")
    print("\n                                                     ✓ READY!\n")
def update_uid(handle2,handle1,table_name,col_name,letter,uid):
    handle2.execute("Select "+col_name+" from "+table_name)
    data = handle2.fetchall()
    n = int(uid[1:])
    for row in data:
        old_id = row[0]
        number = int(old_id[1:])
        if number > n:
            number = number - 1
            if number < 10:
                new_id = letter+"00" + str(number)
            elif number < 100:
                new_id = letter+"0" + str(number)
            else:
                new_id = letter + str(number)
            handle2.execute(("Update "+table_name+" set "+col_name+" = '%s' where "+col_name+" = '%s'")%(new_id,old_id))
    handle1.commit()
def check_date():
    date = input("Enter Date (DD-MM-YYYY) : ")
    if len(date) == 10 and date[2] == "-" and date[-5] == "-":
        return True,date
    else:
        print("⚠ Invalid date format")
        return False,date
def check_email(email):
    if email[-10:] == "@gmail.com":
        return True
    else:
        print("⚠ Invalid email. Please try again.")
    return False
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
def send_notification(receiver_email,message,need_message=True):
    sender_email = "project562009@gmail.com"
    sender_password = ""
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email,message)
        server.quit()
        if need_message:
            print("Message sent successfully")
    except Exception as e:
        sys.stderr.write("\nError:"+str(e)+"\n\n")
        if need_message:
            print("Unable to send the message.")
def user_menu(uname):
    loading_bar("Accessing User Portal",0.03,49)
    print("\n👋 WELCOME",uname,"\n")
    cur.execute("Create database if not exists " + uname)
    user_x = ms.connect(host="localhost",user="root",passwd="root",database=uname)
    user_cur = user_x.cursor()
    # Tables for My Business 
    user_cur.execute("""Create table if not exists Workers(W_ID varchar(10),W_NAME varchar(30),
    POST varchar(30),JOIN_DATE varchar(15)
    ,EMAIL varchar(40))""")
    user_cur.execute("""Create table if not exists Attendance(w_id varchar(10),Date varchar(2),
    Month varchar(15),Year Varchar(10),Status varchar(10))""")
    user_cur.execute("""Create table if not exists Post(P_ID varchar(10),Post varchar(30),Salary varchar(10))""")
    user_cur.execute("""Create table if not exists Sal_attendance(w_id varchar(10),Year varchar(10),
    Month varchar(15),Present_Days varchar(2))""")
    user_cur.execute("Create table if not exists Paid_leaves(Days varchar(2))")
    user_cur.execute("""Create table if not exists Given_Salary(W_ID varchar(10),Month varchar(15),Year varchar(10),
    Total_Salary varchar(10))""")
    user_cur.execute("""Create table if not exists Products(P_ID varchar(10),P_Name varchar(40),price int,stock int)""")
    user_cur.execute("""Create table if not exists Sales(S_ID varchar(10),P_ID varchar(10),Quantity int,Price int,
    Total_Amount int,Sale_Date varchar(13))""")
    while True:
        print("\n+------------------------------------------+")
        print("|               👤 USER PORTAL             |")
        print("+------------------------------------------+")
        print("  Press 1 ----> 📚 View Business")
        print("  Press 2 ----> 🏢 My Business")
        print("  Press 3 ----> ↩ Back")
        choice = input("➤ Please select an option to continue: ")
        if choice == "1":
            cur.execute("Select * from business_ideas")
            data = cur.fetchall()
            if len(data) == 0:
                print("\n  🔒 Business Suggestion Unavailable      ")
                print("  ➤ You cannot access this option now.    ")
                print("  ➤ Please try another option!            ")
                continue
            loading_bar("🔍 Loading Business Explorer",0.03,45)
            while True:
                print("\n+------------------------------------------+")
                print("|          💼 BUSINESS EXPLORER            |")
                print("+------------------------------------------+")
                print("  Press 1 ----> 📚 Business Book          ")
                print("  Press 2 ----> 🔎 Search Business        ")
                print("  Press 3 ----> 💰 Browse by Investment   ")
                print("  Press 4 ----> 🏢 Browse by Department   ")
                print("  Press 5 ----> ✨ Suggest Business       ")
                print("  Press 6 ----> ↩️ Back                  ")
                choice = input("➤ Please select an option to continue: ")
                if choice == "1":
                    cur.execute("Select B_ID,B_Name from business_ideas")
                    business = cur.fetchall()
                    i = 0
                    page = 1
                    while True:
                        if len(business) == 0:
                            print("\n                  ⚠️ Sorry! No business ideas available.\n")
                            break
                        else:
                            print("\n"+"======================================== BUSINESS BOOK ==============================================\n")
                            for j in range(10):
                                if i + j < len(business):
                                    print("\t\t\t\t\t",business[i + j][0],"-",business[i + j][1])
                            print("\n[P] Previous Page")
                            print("[N] Next Page")
                            print("[E] Exit")
                            print("\t\t\t\t\t\t\t\t\t\t\tPage :",page)
                            print("=====================================================================================================")
                            choice = input("\n\n  ➤ Enter your choice: ").lower()
                            if choice == "n":
                                if i + 10 < len(business):
                                    i += 10
                                    page += 1
                                else:
                                    print("\n  ⚠️ You have reached the last page!")
                            elif choice == "p":
                                if i >= 10:
                                    i -= 10
                                    page -= 1
                                else:
                                    print("\n  ⚠️ You are already on the first page!")
                            elif choice == "e":
                                print("\n  📚 Exiting Business Book...")
                                break
                            else:
                                print("\n  ✗ Invalid input! Please enter from P,N,E.")
                elif choice == "2":
                    print("\n+------------------------------------------+")
                    print("|            🔎 SEARCH BUSINESS            |")
                    print("+------------------------------------------+")
                    Id = input("\n➤ Enter the Business ID: ")
                    loading_bar("Searching business...",0.015,49)
                    cur.execute("select * from business_ideas where B_ID = %s",(Id,))
                    data = cur.fetchone()
                    if data is None:
                        print("\n❌ Business not found! Please enter a valid Business ID.")
                        continue
                    print("\n✅ Business Found!\n")
                    print(tabulate([["Business Name",data[1]],["Startup Cost",str(data[3])],["Skills Required",data[4]],
                    ["License",data[-3]],["Demand Level",data[-2]],["Risk Level",data[-1]]],headers=["DETAIL","INFORMATION"],
                    tablefmt="grid"))
                elif choice == "3":
                    print("\n+------------------------------------------+")
                    print("|         💰 BROWSE BY INVESTMENT          |")
                    print("+------------------------------------------+")
                    amount = input("\n➤ Enter your investment amount: ₹")
                    loading_bar("Searching business...",0.015,49)
                    if amount.isdigit():
                        cur.execute("Select B_NAME,COST_LM,SKILLS,LICENSE,DEMAND,RISK from business_ideas where COST_LM <= %s"%
                        (int(amount),))
                        data = cur.fetchall()
                        if len(data) > 0:
                            print("\n✅ Businesses matching your investment:\n")
                            print(tabulate(data,headers=["BUSINESS NAME","STARTUP COST","SKILLS REQUIRED","LICENSE","DEMAND",
                            "RISK"],tablefmt="grid"))
                        else:
                            print("\n⚠️  No businesses found for your investment.")
                    else:
                        print("\n❌ Invalid amount! Please enter numbers only.")
                elif choice == "4":
                    print("\n+------------------------------------------+")
                    print("|         🏢 BROWSE BY DEPARTMENT          |")
                    print("+------------------------------------------+")
                    departments = list()
                    cur.execute("Select distinct DEPT from business_ideas")
                    data = cur.fetchall()
                    if len(data) == 0:
                        print("\n  ⚠️  No Business Available!")
                        continue
                    for i in data:
                        for j in i:
                            departments += [j.lower()]
                    print("\n📂 AVAILABLE DEPARTMENTS")
                    print("-" * 42)
                    for dept_name in departments:
                        print("  🔹",dept_name.title())
                    dept = input("\n➤ Enter the department: ")
                    loading_bar("Searching business...",0.015,49)
                    if dept.lower() in departments:
                        cur.execute("Select B_NAME,Cost_LM,Skills,License,Demand,Risk from business_ideas where dept = '%s'"%
                        (dept,))
                        data = cur.fetchall()
                        print("\n✅ Businesses in",dept.title(),"Department\n")
                        print(tabulate(data,headers=["BUSINESS NAME","STARTUP COST","SKILLS REQUIRED","LICENSE","DEMAND","RISK"],
                        tablefmt="grid"))
                    else:
                        print("\n❌ Invalid department! Please choose from the list.")
                elif choice == "5":
                    print("\n+-----------------------------------------------+")
                    print("|         ✨ BUSINESS RECOMMENDATION SYSTEM     |")
                    print("+-----------------------------------------------+")
                    print("\n  Answer the following questions to find suitable businesses.")
                    # Q1 - INVESTMENT
                    print("\n+------------------------------------------+")
                    print("|             💰 INVESTMENT                |")
                    print("+------------------------------------------+")
                    print("  1. ₹20,000 - ₹50,000")
                    print("  2. ₹50,000 - ₹75,000")
                    print("  3. ₹75,000 - ₹1 Lakh")
                    print("  4. ₹1 Lakh - ₹2 Lakhs")
                    print("  5. Above ₹2 Lakhs")
                    choice = input("\n➤ Select your investment range: ")
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
                    else:
                        print("❌ Invalid choice! Select a number from 1 to 5.")
                        continue
                    # Q2 - DEPARTMENT
                    print("\n+------------------------------------------+")
                    print("|             🎯 YOUR INTEREST             |")
                    print("+------------------------------------------+")
                    cur.execute("Select distinct DEPT from business_ideas")
                    data = cur.fetchall()
                    departments = dict()
                    for i in range(len(data)):
                        departments[i + 1] = data[i][0]
                    print("\t\tKey-Department\n")
                    for i,j in departments.items():
                        print("\t\t" + str(i) + ". " + j)
                    dept_key = input("\n➤ Select your preferred department's key: ")
                    if dept_key.isdigit() and int(dept_key) in departments:
                        dept = departments[int(dept_key)]
                    else:
                        print("❌ Invalid key! Select a valid department's key.")
                        continue
                    # Q3 - SKILLS
                    print("\n+------------------------------------------+")
                    print("|             🛠️ YOUR SKILL              |")
                    print("+------------------------------------------+")
                    cur.execute("Select distinct Skills from business_ideas")
                    data = cur.fetchall()
                    skills = dict()
                    for i in range(len(data)):
                        skills[i + 1] = data[i][0]
                    print("\t\tKey-Skill\n")
                    for i, j in skills.items():
                        print("\t\t" + str(i) + ". " + j)
                    skill_key = input("\n➤ Select your preferred skill's key: ")
                    if skill_key.isdigit() and int(skill_key) in skills:
                        skill = skills[int(skill_key)]
                    else:
                        print("❌ Invalid key! Select a valid skill's key.")
                        continue
                    # Q4 - RISK
                    print("\n+------------------------------------------+")
                    print("|               ⚖️ RISK LEVEL              |")
                    print("+------------------------------------------+")
                    for i, j in options.items():
                        print("\t\t" + str(i) + ". " + j)
                    choice = input("\n➤ Select your risk preference: ")
                    if choice in options:
                        risk = options[choice]
                    else:
                        print("❌ Invalid choice! Select a number from 1 to 3.")
                        continue
                    # ANALYSE
                    print("\n⏳ Finding businesses that match your preferences...")
                    cur.execute("Select B_ID,B_NAME,DEPT,COST_LM,SKILLS,LICENSE,DEMAND,RISK from business_ideas")
                    businesses = cur.fetchall()
                    results = list()
                    for b in businesses:
                        score = 0
                        if min_investment <= b[3] <= max_investment:
                            score += 1
                        if b[2].lower() == dept.lower():
                            score += 1
                        if b[4].lower() == skill.lower():
                            score += 1
                        if b[7] == risk:
                            score += 1
                        percentage = (score/4) * 100
                        if percentage > 0:
                            results.append((percentage,b))
                    for i in range(len(results)):
                       for j in range(i + 1,len(results)):
                           if results[i][0] < results[j][0]:
                               temp = results[i]
                               results[i] = results[j]
                               results[j] = temp
                    loading_bar("Analysing data...",0.015,52)
                    print("\n+" + "-"*94 + "+")
                    print("|" + "                            ✨ YOUR BUSINESS SUGGESTIONS\t\t\t\t       " + "|")
                    print("+" + "-"*94 + "+")
                    if len(results) == 0:
                        print("\n⚠️  No businesses available at the moment.")
                        continue
                    count = 0
                    table = []
                    for percentage,b in results:
                        count += 1
                        if percentage >= 80:
                            emoji = "😄"
                        elif percentage >= 60:
                            emoji = "🙂"
                        elif percentage >= 40:
                            emoji = "😐"
                        else:
                            emoji = "🙁"
                        table.append([count,b[1],emoji + " " + str(int(percentage)) + "%","₹" + str(b[3]),b[4],b[5],b[6],b[7]])
                        if count == 10:
                            break
                    print(tabulate(table,headers=["Sno","Business","Match Score","Startup Cost","Skills","License","Demand","Risk"]
                    ,tablefmt="grid"))
                    print("\n✅ Suggestions are based on your answers.")
                elif choice == "6":
                    print("\n↩️  Returning to the previous menu...")
                    break
                else:
                    print("\n⚠ Invalid choice.")
                    print("  Please select an option from 1 to 6.")
        elif choice == "2":
            while True:
                print("\n+------------------------------------------+")
                print("|        🏢 MY BUSINESS MANAGEMENT         |")
                print("+------------------------------------------+")
                print("|  Press 1 ----> 👥 Workers Management     |")
                print("|  Press 2 ----> 📅 Attendance             |")
                print("|  Press 3 ----> 💰 Manage Salary          |")
                print("|  Press 4 ----> 📦 Product Management     |")
                print("|  Press 5 ----> 🛒 Sales Management       |")
                print("|  Press 6 ----> 📊 Sales Report           |")
                print("|  Press 7 ----> ↩ Back                   |")
                print("+------------------------------------------+")
                choice = input("\n➤ Enter your choice : ")
                if choice == "1":
                    while True:
                        print("\n+------------------------------------------+")
                        print("|          👥 WORKERS MANAGEMENT           |")
                        print("+------------------------------------------+")
                        print("|  Press 1 ----> View Worker               |")
                        print("|  Press 2 ----> Add Worker                |")
                        print("|  Press 3 ----> Update Worker             |")
                        print("|  Press 4 ----> Delete Worker             |")
                        print("|  Press 5 ----> Back                      |")
                        print("+------------------------------------------+")
                        choice = input("\n➤ Enter your choice : ")
                        if choice == "1":
                            user_cur.execute("Select * from workers")
                            records = user_cur.fetchall()
                            if len(records) > 0:
                                print("\n+------------------------------------------+")
                                print("|             👥 WORKER DIRECTORY          |")
                                print("+------------------------------------------+\n")
                                print(tabulate(records,headers=["W_ID","   Worker Name","     Post","Join_Date","     Email"],tablefmt="grid"))
                            else:
                                print("\n⚠️  No workers found!\n")
                        elif choice == "2":
                            print("\n+------------------------------------------+")
                            print("|               ➕ ADD WORKER              |")
                            print("+------------------------------------------+")
                            wid = add_uid("W","W_ID","Workers",user_cur,False)
                            name = input("➤ Enter Worker Name : ")
                            if name == "" or name.isspace():
                                print("⚠ Worker Name is required. Please try again.")
                                continue
                            post = input("➤ Enter Post : ")
                            if post == "" or post.isspace():
                                print("⚠ Worker Post is required. Please try again.")
                                continue
                            join_date = input("➤ Enter Joining Date (YYYY-MM-DD)(or leave it empty if you don't want to add join date) : ")
                            if join_date == "" :
                                join_date = "NULL"
                            elif len(join_date) == 10 and join_date[4] == "-" and join_date[-3] == "-":
                                pass
                            else:
                                print("\n⚠️  Invalid date format! Use YYYY-MM-DD.")
                                continue
                            email = input("➤ Enter Worker Email(or leave it empty if you don't want to add email) : ")
                            if  email != "" :
                                ok = check_email(email)
                                if ok:
                                    otp = randint(100000,999999)
                                    message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                                    send_notification(email,message)
                                else:
                                    continue
                                print("\n➤ Enter the OTP received in your email.")
                                print("⚠️  If you did not receive it, enter an incorrect OTP to cancel.")
                                entered_otp = input("➤ Enter the OTP : ")
                                if str(otp) == entered_otp:
                                    print("\n✓ Email verified successfully!")
                                else:
                                    print("\n✗ Incorrect OTP!")
                                    print("⚠️  Failed to add worker.")
                                    continue
                            else:
                                email = "NULL"
                            user_cur.execute("Insert into workers VALUES ('%s','%s','%s','%s','%s')"% 
                            (wid,name,post,join_date,email))
                            user_x.commit()
                            print("\n✓ Worker added successfully!")
                        elif choice == "3":
                            print("\n+------------------------------------------+")
                            print("|              ✏️ UPDATE WORKER            |")
                            print("+------------------------------------------+")
                            wid = input("➤ Enter Worker ID to update : ")
                            user_cur.execute("Select * from workers where W_ID = '%s'" % (wid,))
                            record = user_cur.fetchone()
                            if record is not None:
                                print("\n  ➤ Press Enter to keep the existing value.")
                                print("\n+-----------------------------------------------+")
                                name = input("  ➤ Worker Name : ")
                                if name == "":
                                    name = record[1]
                                post = input("  ➤ Worker Post : ")
                                if post == "":
                                    post = record[2]
                                join_date = input("  ➤ Joining Date : ")
                                if join_date == "" :
                                    join_date = record[-2]
                                elif len(join_date) == 10 and join_date[4] == "-" and join_date[-3] == "-":
                                    pass
                                else:
                                    print("\n⚠️  Invalid date format! Use YYYY-MM-DD.")
                                    continue
                                email = input("  ➤ Email : ")
                                if email == "":
                                    email = record[-1]
                                else:
                                    ok = check_email(email)
                                    if ok:
                                        otp = randint(100000,999999)
                                        message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                                        send_notification(email,message)
                                    else:
                                        continue
                                    print("\n➤ Enter the OTP received in your email.")
                                    print("⚠️  If you did not receive it, enter an random letter to cancel.")
                                    entered_otp = input("➤ Enter the OTP : ")
                                    if str(otp) == entered_otp:
                                        print("\n✓ Email verified successfully!")
                                    else:
                                        print("\n✗ Incorrect OTP!")
                                        print("⚠️  Failed to update worker.")
                                        continue
                                user_cur.execute("""Update workers set W_NAME = '%s',POST = '%s',JOIN_DATE = '%s',EMAIL = '%s'where
                                W_ID = '%s'"""%(name,post,join_date,email,wid))
                                user_x.commit()
                                print("\n+-----------------------------------------------+")
                                print("|       ✓ WORKER DETAILS UPDATED SUCCESSFULLY   |")
                                print("+-----------------------------------------------+")
                            else:
                                print("\n✗ Worker ID not found!")
                        elif choice == "4":
                            print("\n+--------------------------------------------+")
                            print("|              🗑️ DELETE WORKER            |")
                            print("+--------------------------------------------+")
                            wid = input("➤ Enter Worker ID to delete : ")
                            user_cur.execute("Select W_ID from workers where W_ID = '%s'" % (wid,))
                            if user_cur.fetchone() is None:
                                print("\n✗ Worker ID not found!")
                                continue
                            sure = input("\n⚠️  Are you sure you want to delete? (Y/N) : ").lower()
                            if sure == "y":
                                user_cur.execute("Delete from workers where W_ID='%s'" % (wid,))
                                user_cur.execute("Delete from attendance where W_ID='%s'" % (wid,))
                                user_cur.execute("Delete from sal_attendance where W_ID='%s'" % (wid,))
                                user_x.commit()
                                print("\n+-----------------------------------------------+")
                                print("|       ✓ WORKER DELETED SUCCESSFULLY           |")
                                print("+-----------------------------------------------+")
                                update_uid(user_cur,user_x,"Workers","W_ID","W",wid)
                            else:
                                print("\n↩ Deletion cancelled.")
                        elif choice == "5":
                            print("\n↩ Returning to Business Management...")
                            break
                        else:
                            print("\n⚠️  Invalid choice! Please enter a number from 1 to 5.")
                elif choice == "2":
                    print("\n+------------------------------------------+")
                    print("|             📅 ATTENDANCE                |")
                    print("+------------------------------------------+")
                    wid = input("\n➤ Enter Worker ID : ")
                    user_cur.execute("Select w_id from workers where w_id = '%s'"%(wid,))
                    worker = user_cur.fetchone()
                    if worker is None:
                        print("\n✗ Worker not found, Invalid worker Id")
                        continue
                    while True:
                        print("\n+--------------------------------------+")
                        print("|          📅 ATTENDANCE MENU          |")
                        print("+--------------------------------------+")
                        print("|  Press 1 ----> View Attendance       |")
                        print("|  Press 2 ----> Mark Attendance       |")
                        print("|  Press 3 ----> Delete Attendance     |")
                        print("|  Press 4 ----> Back                  |")
                        print("+--------------------------------------+")
                        choice = input("\n➤ Enter your choice : ")
                        if choice == "1":
                            print("\n",months)
                            month = input("\n➤ Enter the month's key : ")
                            if month not in months:
                                print("\n⚠ Invalid month key. Please try again.")
                                continue
                            year = input("➤ Enter the year : ")
                            if  not year.isdigit():
                                print("\n⚠ Invalid year. Year must contain only digits.")
                                continue
                            user_cur.execute("Select * from attendance where w_id ='%s' and month = '%s' and year = '%s'" %
                            (wid,months[month],year))
                            record = user_cur.fetchall()
                            if len(record) == 0:
                                print("\n+------------------------------------------+")
                                print("|         ⚠ NO ATTENDANCE FOUND           |")
                                print("+------------------------------------------+")
                            else:
                                print("\n+------------------------------------------+")
                                print("|          📋 ATTENDANCE RECORDS           |")
                                print("+------------------------------------------+")
                                print(tabulate(record,headers=["Worker ID","Day","Month","Year","Status"],tablefmt="grid"))
                        #(DD-MM-YYYY)
                        elif choice == "2":
                            ok,entered_date = check_date()
                            if ok:
                                user_cur.execute("""Select w_id,date from attendance where w_id='%s'and date='%s' and month='%s'
                                and year='%s'"""% (wid,entered_date[:2],months[entered_date[3:5]],entered_date[6:]))
                                data = user_cur.fetchall()
                                if len(data) != 0:
                                    print("⚠ Attendance already exists for",wid,"on",entered_date)
                                    continue
                                print("\n+------------------------------------------+")
                                print("|           ✚ MARK ATTENDANCE             |")
                                print("+------------------------------------------+")
                                print("|  Press 1 ----> Present                   |")
                                print("|  Press 2 ----> Absent                    |")
                                print("+------------------------------------------+")
                                choice = input("\n➤ Enter the status : ")
                                if choice == "1":
                                    status = "Present"
                                    user_cur.execute("""Select * from sal_attendance where w_id='%s' and year='%s' and
                                    month='%s'"""% (wid,entered_date[6:],months[entered_date[3:5]]))
                                    data = user_cur.fetchall()
                                    if len(data) == 0:
                                        present_days = "1"
                                        user_cur.execute("""Insert into sal_attendance values('%s','%s','%s','%s')""" %
                                        (wid,entered_date[6:],months[entered_date[3:5]],present_days))
                                    else:
                                        present_days = data[0][-1]
                                        present_days = str(int(present_days) + 1)
                                        user_cur.execute("""Update sal_attendance set present_days='%s'where w_id='%s' and
                                        year='%s'and month='%s'"""% (present_days,wid,entered_date[6:],months[entered_date[3:5]]))
                                    user_x.commit()
                                elif choice == "2":
                                    status = "Absent"
                                else:
                                    print("\n⚠ Invalid choice. Please try again.")
                                    continue
                                user_cur.execute("Insert into attendance values('%s','%s','%s','%s','%s')"%
                                (wid,entered_date[:2],months[entered_date[3:5]],entered_date[6:],status))
                                user_x.commit()
                                print("\n+------------------------------------------+")
                                print("|       ✓ ATTENDANCE MARKED SUCCESSFULLY   |")
                                print("+------------------------------------------+")
                                print("  ➤ Worker ID :",wid)
                                print("  ➤ Date      :",entered_date)
                                print("  ➤ Status    :",status.upper())
                            else:
                                continue
                        elif choice == "3":
                            while True:
                                print("\n+------------------------------------------+")
                                print("|          🗑 DELETE ATTENDANCE            |")
                                print("+------------------------------------------+")
                                print("|  Press 1 ----> Delete by Month           |")
                                print("|  Press 2 ----> Delete by Year            |")
                                print("|  Press 3 ----> Back                      |")
                                print("+------------------------------------------+")
                                choice = input("\n➤ Enter your choice : ")
                                if choice == "1":
                                    print("\n+------------------------------------------+")
                                    print("|               📅 MONTHS                  |")
                                    print("+------------------------------------------+")
                                    print("\n",months)
                                    month = input("\n➤ Enter the month's key : ")
                                    if month not in months:
                                        print("\n⚠ Invalid month key. Please try again.")
                                        continue
                                    year = input("➤ Enter the year : ")
                                    if  not year.isdigit():
                                        print("\n⚠ Invalid year. Year must contain only digits.")
                                        continue
                                    user_cur.execute("Select * from attendance where w_id = '%s' and month='%s' and year = '%s'" %
                                    (wid,months[month],year))
                                    data = user_cur.fetchall()
                                    if len(data) == 0:
                                        print("\n⚠ No attendance records found for ",wid,"on",months[month],"-",year)
                                        continue
                                    sure = input("\n➤ Are you sure you want to delete? (Yes/No) : ").lower()
                                    if sure == "yes":
                                        user_cur.execute("Delete from attendance where w_id = '%s' and month='%s' and year = '%s'" %
                                        (wid,months[month],year))
                                        user_cur.execute("""Delete from sal_attendance where w_id = '%s' and month='%s' and year =
                                        '%s'""" %(wid,months[month],year))
                                        user_x.commit()
                                        print("\n+------------------------------------------+")
                                        print("|      ✓ ATTENDANCE DELETED SUCCESSFULLY   |")
                                        print("+------------------------------------------+")
                                    else:
                                        print("\n↩ Deletion Cancelled.")
                                elif choice == "2":
                                    year = input("\n➤ Enter the year : ")
                                    if not year.isdigit():
                                        print("\n⚠Invalid year. Year must contain digits only.")
                                        continue
                                    user_cur.execute("Select * from attendance where w_id = '%s' and year='%s'" % (wid,year))
                                    data = user_cur.fetchall()
                                    if len(data) == 0:
                                        print("\n⚠ No attendance records found for",wid,"in",year)
                                        continue
                                    sure = input("\n➤ Are you sure you want to delete? (Yes/No) : ").lower()
                                    if sure == "yes":
                                        user_cur.execute("Delete from attendance where w_id = '%s' and year='%s'" % (wid,year))
                                        user_cur.execute("Delete from sal_attendance where w_id = '%s' and year='%s'"  % (wid,year))
                                        user_x.commit()
                                        print("\n+------------------------------------------+")
                                        print("|      ✓ ATTENDANCE DELETED SUCCESSFULLY   |")
                                        print("+------------------------------------------+")
                                    else:
                                        print("\n↩ Deletion Cancelled.")
                                elif choice == "3":
                                    print("\n↩ Returning to the previous menu...")
                                    break
                                else:
                                    print("\n⚠ Invalid choice.")
                                    print("   Please select an option from 1 to 3.")
                        elif choice == "4":
                            print("\n↩ Returning to the previous menu...")
                            break
                        else:
                            print("\n⚠ Invalid choice.")
                            print("   Please select an option from 1 to 4.")
                elif choice == "3":
                    print("\n+------------------------------------------+")
                    print("|              💰 MANAGE SALARY            |")
                    print("+------------------------------------------+")
                    while True:
                        print("\n+-------------------------------------------+")
                        print("|             💵 SALARY OPTIONS             |")
                        print("+-------------------------------------------+")
                        print("|  Press 1 ----> Manage Salary Details      |")
                        print("|  Press 2 ----> Check Paid Leaves          |")
                        print("|  Press 3 ----> Generate Salary            |")
                        print("|  Press 4 ----> View Paid Salary           |")
                        print("|  Press 5 ----> Delete Salary History      |")
                        print("|  Press 6 ----> Back                       |")
                        print("+-------------------------------------------+")
                        choice = input("\n➤ Enter your choice : ")
                        if choice == "1":
                            while True:
                                print("\n+-------------------------------------------+")
                                print("|          🛠️ MANAGE POST SALARY          |")
                                print("+-------------------------------------------+")
                                print("|  Press 1 ----> View All Posts             |")
                                print("|  Press 2 ----> Add New Post               |")
                                print("|  Press 3 ----> Update Post Details        |")
                                print("|  Press 4 ----> Delete Post                |")
                                print("|  Press 5 ----> Back                       |")
                                print("+-------------------------------------------+")
                                choice = input("\n➤ Enter your choice : ")
                                if choice == "1": #P_ID varchar(10),Post varchar(30),Salary varchar(10)
                                    user_cur.execute("Select * from Post")
                                    posts = user_cur.fetchall()
                                    if len(posts) == 0:
                                        print("\n+-------------------------------------------+")
                                        print("|             ⚠ NO POSTS FOUND             |")
                                        print("+-------------------------------------------+")
                                        continue
                                    print("\n+------------------------------------------+")
                                    print("|              📋 POST DIRECTORY           |")
                                    print("+------------------------------------------+")
                                    print(tabulate(posts,headers=["Post ID","Post","Salary"],tablefmt="grid"))
                                elif choice == "2":
                                    print("\n+------------------------------------------+")
                                    print("|               ➕ ADD POST                |")
                                    print("+------------------------------------------+")
                                    post = input("\n➤ Enter the Post : ")
                                    if post.isspace() or len(post) == 0:
                                        print("\n⚠ Invalid post.")
                                        print("   Post can't be empty or with only spaces !")
                                        continue
                                    salary = input("➤ Enter the Salary : ")
                                    if not salary.isdigit():
                                        print("\n⚠ Invalid salary.")
                                        print("  Salary must contain numbers only.")
                                        continue
                                    user_cur.execute("Insert into Post values('%s','%s','%s')" %
                                    (add_uid("P","P_ID","Post",user_cur,False),post.title(),salary))
                                    user_x.commit()
                                    print("\n+------------------------------------------+")
                                    print("|           ✓ POST ADDED SUCCESSFULLY      |")
                                    print("+------------------------------------------+")
                                elif choice == "3":
                                    pid = input("\n➤ Enter the Post ID : ")
                                    user_cur.execute("Select * from Post where P_ID='%s'" % (pid,))
                                    posts = user_cur.fetchone()
                                    if posts is None:
                                        print("\n+------------------------------------------+")
                                        print("|             ✗ INVALID POST ID            |")
                                        print("+------------------------------------------+")
                                        print(" Post ID doesn't exist !")
                                        continue
                                    print("\n+-------------------------------------------+")
                                    print("|            ✏️ UPDATE POST DETAILS         |")
                                    print("+-------------------------------------------+")
                                    print("\n  ➤ Press Enter to keep the existing value.")
                                    print("\n+-----------------------------------------------+")
                                    post = input("\n➤ Enter the Post : ")
                                    if len(post) == 0:
                                        post = posts[1]
                                    elif post.isspace() :
                                        print("\n⚠ Invalid post.")
                                        print("   Post can't be with only spaces !")
                                        continue
                                    salary = input("➤ Enter the Salary : ")
                                    if len(salary) == 0:
                                        salary = posts[2]
                                    elif not salary.isdigit():
                                        print("\n⚠ Invalid salary.")
                                        print("  Salary must contain numbers only.")
                                        continue
                                    user_cur.execute("Update Post set Post = '%s',Salary ='%s' where P_Id ='%s'" %
                                    (post.title(),salary,pid))
                                    user_x.commit()
                                    print("\n+------------------------------------------+")
                                    print("|        ✓ POST DETAILS UPDATED            |")
                                    print("+------------------------------------------+")
                                elif choice == "4":
                                    pid = input("\n➤ Enter the Post ID : ")
                                    user_cur.execute("Select P_ID from Post where P_ID='%s'" % (pid,))
                                    posts = user_cur.fetchall()
                                    if len(posts) == 0:
                                        print("\n+------------------------------------------+")
                                        print("|             ✗ INVALID POST ID            |")
                                        print("+------------------------------------------+")
                                        print(" Post ID doesn't exist !")
                                        continue
                                    sure = input("\n➤ Are You sure to Delete (Yes/No) : ")
                                    if sure.lower() == "yes":
                                        user_cur.execute("Delete from Post where P_ID = '%s'" % (pid,))
                                        update_uid(user_cur,user_x,"Post","P_ID","P",pid)
                                        user_x.commit()
                                        print("\n+--------------------------------------------+")
                                        print("|           ✓ POST DELETED SUCCESSFULLY      |")
                                        print("+--------------------------------------------+")
                                    else:
                                        print("\n↩ Deletion Cancelled.")
                                elif choice == "5":
                                    break
                                else:
                                   print("\n⚠ Invalid choice.")
                                   print("   Please select an option from 1 to 5.")
                        elif choice == "2":  # Paid Leaves
                            print("\n+------------------------------------------+")
                            print("|             📅 PAID LEAVE SETTINGS       |")
                            print("+------------------------------------------+")
                            user_cur.execute("Select * from Paid_leaves")
                            days = user_cur.fetchall()
                            if len(days) == 0:
                                print("\n⚠ No paid leave details available.")
                                print("Provide the no of paid leaves to access the salary for employees")
                                a=1
                            else:
                                print("\nCurrent Setting :")
                                print(tabulate(days,headers=["No Of Paid Leaves"],tablefmt="grid"))
                                print("\n➤ Leave it empty to just view it.")
                                a=2
                            print("➤ Give the input if you need to update.")
                            paid_leaves = input("\n➤ Enter the No of Paid Leaves (for a month) : ")
                            if paid_leaves == "":
                                continue
                            if not paid_leaves.isdigit():
                                print("\n⚠ No of days should be a number.")
                                continue
                            if len(paid_leaves) not in (1,2):
                                print("\n⚠ It must contain 1 or 2 digits only.")
                                continue
                            if a==1:
                                user_cur.execute("Insert into paid_leaves values ('%s')" % (paid_leaves,))
                            else:
                                user_cur.execute("Update paid_leaves set days='%s'" % (paid_leaves,))
                            user_x.commit()
                            print("\n+--------------------------------------------+")
                            print("|       ✓ PAID LEAVES UPDATED SUCCESSFULLY   |")
                            print("+--------------------------------------------+")
                        elif choice == "3":  # Generate Salary
                            print("\n+------------------------------------------+")
                            print("|             💰 GENERATE SALARY           |")
                            print("+------------------------------------------+")
                            wid = input("\nEnter the Employee ID : ")
                            user_cur.execute("Select * from Attendance where w_id='%s'" % (wid,))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n+------------------------------------------+")
                                print("|          ✗ INVALID WORKER ID             |")
                                print("+------------------------------------------+")
                                continue
                            year = input("➤ Enter the Year : ")
                            if not year.isdigit():
                                print("\n⚠ Invalid input. Year must contain numbers.")
                                continue
                            print("\n Months :")
                            print(months)
                            month_key = input("\n➤ Enter the Month's Key : ")
                            if month_key not in months:
                                print("\n⚠ Invalid Month Key.")
                                continue
                            month = months[month_key]
                            user_cur.execute("""Select count(*) from attendance where Status='Present' and month='%s'
                            and year='%s' and w_id='%s'""" % (month,year,wid))
                            present_days = user_cur.fetchall()[0][0]
                            user_cur.execute("""Select count(*) from attendance where Status='Absent' and
                            month='%s'and year='%s' and w_id='%s'""" % (month,year,wid))
                            absent_days = user_cur.fetchall()[0][0]
                            Max_days = max_days[month]
                            if month == "February" and int(year) % 4 == 0:
                                Max_days = 29
                            total_days = present_days + absent_days
                            if total_days != Max_days:
                                print("\n+---------------------------------------------+")
                                print("|          ⚠ INCOMPLETE ATTENDANCE           |")
                                print("+---------------------------------------------+")
                                print("|  Full attendance has not been recorded.     |")
                                print("|  Unable to generate salary                  |")
                                print("+---------------------------------------------+")
                                continue
                            user_cur.execute("Select W_Name,Post,Email from workers where w_id='%s'" % (wid,))
                            name,post,email = user_cur.fetchall()[0]
                            user_cur.execute("Select Salary from post where post='%s'" % (post,))
                            sal = user_cur.fetchall()
                            if len(sal) == 0:
                                print("\n+------------------------------------------+")
                                print("|          ⚠ SALARY NOT SPECIFIED         |")
                                print("+------------------------------------------+")
                                print("|  No Salary is specified for this post.   |")
                                print("+------------------------------------------+")
                                continue
                            salary = sal[0][0]
                            user_cur.execute("Select days from paid_leaves")
                            paid_leaves = user_cur.fetchall()[0][0]
                            absent_days = Max_days - present_days
                            if absent_days >= int(paid_leaves):
                                paid_leaves = int(paid_leaves)
                            else:
                                paid_leaves = absent_days
                            bonus = input("\n➤ Enter the Bonus (leave empty if none) : ")
                            if bonus == "":
                                bonus = "0"
                            elif not bonus.isdigit():
                                print("\n⚠ Invalid Bonus.")
                                continue
                            deduction = input("➤ Enter the Deduction (leave empty if none) : ")
                            if deduction == "":
                                deduction = "0"
                            elif not deduction.isdigit():
                                print("\n⚠ Invalid Deduction.")
                                continue
                            # Calculate Salary
                            final_salary = (float(int(salary) / Max_days)) * (present_days + paid_leaves) + int(bonus) - int(deduction)
                            if final_salary < 0:
                                final_salary = 0
                            receipt = "\n\n" + "+" + "-" * 51 + "+\n"
                            receipt += "" + " " * 20 + "SALARY RECEIPT" + " " * 17 + "\n"
                            receipt += "+" + "-" * 51 + "+\n"
                            receipt += " Worker ID         : " + wid.upper() + "\n"
                            receipt += " Post              : " + post + "\n"
                            receipt += " Salary For        : " + (month + "-" + year) + "\n"
                            receipt += "+" + "-" * 51 + "+\n"
                            receipt += " Description     " +  "   Values" + "\n"
                            receipt += "+" + "-" * 51 + "+\n"
                            receipt += " Monthly Salary    : ₹" + salary + "\n"
                            receipt += " Present Days      : " + str(present_days) + "/" + str(Max_days) + "\n"
                            receipt += " Paid Leaves       : " + str(paid_leaves) + "\n"
                            receipt += " Bonus             : ₹" + bonus + "\n"
                            receipt += " Deduction         : ₹" + deduction + "\n"
                            receipt += "+" + "-" * 51 + "+\n"
                            receipt += " FINAL SALARY      : ₹" + str(final_salary) + "\n"
                            receipt += "+" + "-" * 51 + "+" + "\n\n"
                            print(receipt)
                            user_cur.execute("Select * from Given_salary where w_id='%s' and month='%s' and year='%s'" %
                            (wid,month,year))
                            data = user_cur.fetchall()
                            if len(data) != 0:
                                print("\n+------------------------------------------+")
                                print("|          ⚠ SALARY RECORD EXISTS         |")
                                print("+------------------------------------------+")
                                print("Already the salary record for",wid,"exists for",month,"-", year)
                                update = input("\n➤ Need to update it (Yes/No) : ")
                                if update.lower() == "yes":
                                    user_cur.execute("""Update Given_Salary set Total_Salary='%s' where W_ID='%s' and
                                    month='%s' and year='%s'""" %(str(final_salary),wid,month,year))
                                    user_x.commit()
                                    print("\n+------------------------------------------+")
                                    print("|       ✓ SALARY DETAILS UPDATED           |")
                                    print("+------------------------------------------+")
                                else:
                                    print("\n↩ Updation Cancelled.")
                            else:
                                user_cur.execute("""Insert into Given_Salary values('%s','%s','%s','%s')""" %
                                (wid,month,year,str(final_salary)))
                                user_x.commit()
                                print("\n+------------------------------------------+")
                                print("|       ✓ SALARY REGISTERED SUCCESSFULLY   |")
                                print("+------------------------------------------+")
                            notify = input("\nWant to send this receipt to the worker (Yes/No) : ")
                            if notify.lower() == "yes":
                                email_receipt = receipt.replace("|", " ")
                                email_receipt = email_receipt.replace("₹","Rs.")
                                send_notification(email,email_receipt)
                            else:
                                print("\n↩ Receipt not sent to",name.capitalize(),"-",wid)
                        elif choice == "4":  # View Paid Salary
                            user_cur.execute("Select * from Given_Salary")
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n+------------------------------------------+")
                                print("|             ⚠ NO SALARY PAID            |")
                                print("+------------------------------------------+")
                                continue
                            print("\n+------------------------------------------+")
                            print("|             📋 PAID SALARY RECORDS       |")
                            print("+------------------------------------------+")
                            print(tabulate(data,headers=["Worker ID","Month","Year","Total Salary"], tablefmt="grid"))
                        elif choice == "5":  # Delete Salary History
                            print("\n+------------------------------------------+")
                            print("|          🗑️ DELETE SALARY HISTORY      |")
                            print("+------------------------------------------+")
                            wid = input("➤ Enter the Worker ID : ")
                            user_cur.execute("Select * from Workers where w_id='%s'" % (wid,))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n✗ Worker not found, Invalid worker Id")
                                continue
                            print("\n",months)
                            month = input("\n➤ Enter the month's key : ")
                            if month not in months:
                                print("\n⚠ Invalid month key. Please try again.")
                                continue
                            year = input("➤ Enter the year : ")
                            if  not year.isdigit():
                                print("\n⚠ Invalid year. Year must contain only digits.")
                                continue
                            user_cur.execute("Select * from given_salary where w_id='%s' and month = '%s' and year = '%s'" %
                            (wid,months[month],year))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n+------------------------------------------+")
                                print("|       ⚠ NO RECORDS FOUND FOR",wid,"      |")
                                print("+------------------------------------------+")
                                continue
                            sure = input("\n➤ Are You sure (Yes/No) : ")
                            if sure.lower() != "yes":
                                print("\n↩ Deletion Cancelled.")
                                continue
                            user_cur.execute("Delete from given_salary where w_id='%s' and month = '%s' and year = '%s'" %
                            (wid,months[month],year))
                            user_x.commit()
                            print("\n+------------------------------------------+")
                            print("|       ✓ SALARY HISTORY DELETED           |")
                            print("+------------------------------------------+")
                        elif choice == "6":  # Back
                            break
                        else:
                            print("\n⚠ Invalid choice.")
                            print("   Please select an option from 1 to 6.")
                elif choice == "4":
                    print("\n+------------------------------------------+")
                    print("|           📦 PRODUCT MANAGEMENT          |")
                    print("+------------------------------------------+")
                    while True:
                        print("\n+------------------------------------------+")
                        print("|  Press 1 ---> View Products              |")
                        print("|  Press 2 ---> Add Product                |")
                        print("|  Press 3 ---> Update Product             |")
                        print("|  Press 4 ---> Delete Product             |")
                        print("|  Press 5 ---> Out Of Stock               |")
                        print("|  Press 6 ---> Back                       |")
                        print("+------------------------------------------+")
                        choice = input("\n➤ Enter your choice : ")
                        if choice == "1":
                            user_cur.execute("Select * from products")
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n⚠ No Products Found")
                                continue
                            print("\n+------------------------------------------+")
                            print("|              📦 PRODUCT LIST             |")
                            print("+------------------------------------------+")
                            print(tabulate(data,headers=["Product ID","Product Name","Price","Stock"],tablefmt="grid"))
                        elif choice == "2":
                            print("\n+------------------------------------------+")
                            print("|              ✚ ADD PRODUCT              |")
                            print("+------------------------------------------+")
                            pid = add_uid("P","P_ID","Products",user_cur, False)
                            name = input("➤ Enter Product Name : ")
                            if name == "" or name.isspace():
                                print("\n⚠ Invalid Product Name")
                                continue
                            price = input("➤ Enter Price : ")
                            if price == "" or not price.isdigit():
                                print("\n⚠ Invalid Price")
                                continue
                            stock = input("➤ Enter Stock : ")
                            if stock == "" or not stock.isdigit():
                                print("\n⚠ Invalid Stock value")
                                continue
                            user_cur.execute("Insert into products values('%s','%s','%s','%s')" %
                            (pid,name,price,stock))
                            user_x.commit()
                            print("\n+---------------------------------------------+")
                            print("|           ✓ PRODUCT ADDED SUCCESSFULLY      |")
                            print("+---------------------------------------------+")
                        elif choice == "3":
                            print("\n+------------------------------------------+")
                            print("|             ✏️ UPDATE PRODUCT            |")
                            print("+------------------------------------------+")
                            pid = input("➤ Enter Product ID : ")
                            user_cur.execute("Select * from Products where p_id='%s'" % (pid,))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n✗ Invalid Product ID")
                                continue
                            print("\n➤ Press Enter to keep the existing value.")
                            print("\n+-----------------------------------------------+")
                            pname = input("➤ Enter  Product Name : ")
                            if pname == "" :
                                pname = data[0][1]
                            price = input("➤ Enter Price : ")
                            if price == "" :
                                price = data[0][2]
                            elif not price.isdigit():
                                print("\n⚠ Invalid Price")
                                continue
                            stock = input("➤ Enter New Stock : ")
                            if stock == "" :
                                stock = data[0][3]
                            elif not stock.isdigit():
                                print("\n⚠ Invalid Stock value")
                                continue
                            user_cur.execute("Update products set p_name='%s',price='%s',stock='%s' where p_id='%s'" %
                            (pname,price,stock,pid))
                            user_x.commit()
                            print("\n✓ Product Updated Successfully")
                        elif choice == "4":
                            print("\n+--------------------------------------------+")
                            print("|             🗑️ DELETE PRODUCT            |")
                            print("+--------------------------------------------+")
                            pid = input("➤ Enter Product ID : ")
                            user_cur.execute("Select * from Products where p_id='%s'" % (pid,))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n✗ Invalid Product ID")
                                continue
                            sure = input("\n➤ Are you sure you want to delete this product? (Yes/No) : ")
                            if sure.lower() == "yes":
                                user_cur.execute("Delete from Products where p_id='%s'" % (pid,))
                                user_x.commit()
                                print("\n+-----------------------------------------------+")
                                print("|       ✓ PRODUCT DELETED SUCCESSFULLY          |")
                                print("+-----------------------------------------------+")
                                update_uid(user_cur,user_x,"Products","P_ID","P",pid)
                            else:
                                print("\n↩ Deletion Cancelled")
                        elif choice == "5":
                            user_cur.execute("Select * from Products where stock = 0")
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n✓ All Products are In Stock")
                            else:
                                print("\n+------------------------------------------+")
                                print("|          ⚠ OUT OF STOCK PRODUCTS        |")
                                print("+------------------------------------------+")
                                print(tabulate(data,headers=["Product ID","Product Name","Price","Stock"],tablefmt="grid"))
                        elif choice == "6":
                            print("\n↩️  Returning to the previous menu...")
                            break
                        else:
                            print("\n⚠ Invalid choice.")
                            print("  Please select an option from 1 to 6.")
                elif choice == "5":
                    print("\n+------------------------------------------+")
                    print("|              💰 SALES MANAGEMENT         |")
                    print("+------------------------------------------+")
                    while True:
                        print("\n+------------------------------------------+")
                        print("|  Press 1 ---> View Sales                 |")
                        print("|  Press 2 ---> Add Sale                   |")
                        print("|  Press 3 ---> Delete Sale                |")
                        print("|  Press 4 ---> Back                       |")
                        print("+------------------------------------------+")
                        choice = input("\n➤ Enter your choice : ")
                        if choice == "1":
                            user_cur.execute("Select * from Sales")
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n⚠ No Sales Found")
                            else:
                                print("\n+------------------------------------------+")
                                print("|               📋 SALES DETAILS           |")
                                print("+------------------------------------------+")
                                print(tabulate(data,headers=["Sales ID","Product ID","Quantity","Price","Total Amount","Sale Date"],
                                tablefmt="grid"))
                        elif choice == "2":
                            sid = add_uid("S","S_ID","Sales",user_cur,False)
                            pid = input("\n➤ Enter Product ID : ")
                            user_cur.execute("Select * from Products where p_id='%s'"%(pid,))
                            product = user_cur.fetchall()
                            if len(product) == 0:
                                print("\n✗ Invalid Product ID")
                                continue
                            quantity = input("➤ Enter Quantity : ")
                            if not quantity.isdigit() or int(quantity) <= 0:
                                print("\n✗ Invalid Quantity")
                                continue
                            quantity = int(quantity)
                            stock = int(product[0][-1])
                            price = int(product[0][2])
                            if quantity > stock:
                                print("\n⚠ Not Enough Stock")
                                continue
                            total_amount = price*quantity
                            sale_date = input("➤ Enter Sale Date (YYYY-MM-DD) : ")
                            try:
                                datetime.strptime(sale_date,"%Y-%m-%d")
                            except:
                                print("\n✗ Invalid Date")
                                continue
                            user_cur.execute("""Insert into Sales values('%s','%s',%s,%s,%s,'%s')"""%(sid,pid.upper(),quantity,price,
                            total_amount,sale_date))
                            user_cur.execute("Update Products set stock=stock-%s where p_id='%s'"%(quantity,pid))
                            user_x.commit()
                            print("\n+---------------------------------------------+")
                            print("|           ✓ SALE ADDED SUCCESSFULLY         |")
                            print("+---------------------------------------------+")
                        elif choice == "3":
                            sid = input("\n➤ Enter Sale ID : ")
                            user_cur.execute("Select * from Sales where s_id='%s'"%(sid,))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n✗ Invalid Sale ID")
                                continue
                            sure = input("\n➤ Do you want to delete this sale? (Yes/No) : ")
                            if sure.lower() != "yes":
                                print("\n↩ Deletion Cancelled")
                                continue
                            user_cur.execute("Delete from Sales where s_id='%s'"%(sid,))
                            user_x.commit()
                            print("\n+--------------------------------------------+")
                            print("|       ✓ SALE DELETED SUCCESSFULLY          |")
                            print("+--------------------------------------------+")
                            update_uid(user_cur,user_x,"Sales","S_id","S",sid)
                        elif choice == "4":
                            print("\n↩️  Returning to the previous menu...")
                            break
                        else:
                            print("\n⚠ Invalid choice.")
                            print("  Please select an option from 1 to 4.")
                elif choice == "6":
                    while True:
                        print("\n+------------------------------------------+")
                        print("|              📊 SALES REPORT             |")
                        print("+------------------------------------------+")
                        print("|  Press 1 ----> 📅 Daily Sales Report     |")
                        print("|  Press 2 ----> 📆 Monthly Sales Report   |")
                        print("|  Press 3 ----> 📈 Monthly Sales Summary  |")
                        print("|  Press 4 ----> 📊 Yearly Sales Summary   |")
                        print("|  Press 5 ----> ↩ Back                   |")
                        print("+------------------------------------------+")
                        choice = input("\n➤ Enter your choice : ")
                        if choice == "1":
                            date = input("\n➤ Enter date (YYYY-MM-DD) : ")
                            try:
                                datetime.strptime(date,"%Y-%m-%d")
                            except:
                                print("\n✗ Invalid Date format")
                                continue
                            user_cur.execute("""Select P_ID,sum(quantity),sum(total_amount) from Sales  where sale_date='%s'
                            group by P_ID""" % (date,))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n⚠ No sales found for this date")
                                continue
                            total_income = 0
                            for row in data:
                                total_income += row[2]
                            print("\n+------------------------------------------+")
                            print("|             📅 DAILY SALES REPORT        |")
                            print("+------------------------------------------+")
                            print("  Date :",date)
                            print("\n📋 PRODUCT-WISE SALES DETAILS")
                            print(tabulate(data,headers=["Product ID","Total Quantity Sold","Total Revenue"],tablefmt="grid"))
                            print("  Total Income   : ₹",total_income)
                        elif choice == "2":
                            print(months)
                            month = input("\n➤ Enter month's key : ")
                            if month not in months:
                                print("\n✗ Invalid month key")
                                continue
                            year = input("➤ Enter year : ")
                            if not year.isdigit():
                                print("\n✗ Invalid input, Year must contain digits")
                                continue
                            user_cur.execute("""Select P_ID,sum(quantity),sum(total_amount) From Sales where sale_date like '%s'
                            group by P_ID"""%(year + "-" + month + "-%",))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n⚠ No sales found for this month")
                                continue
                            total_sales_income = 0
                            for row in data:
                                total_sales_income += row[2]
                            print("\n+------------------------------------------+")
                            print("|            📆 MONTHLY SALES REPORT       |")
                            print("+------------------------------------------+")
                            print("  Month               :",months[month])
                            print("  Year                :",year)
                            print("  Total Income        : ₹",total_sales_income)
                            print("\n📋 SALES DETAILS")
                            print(tabulate(data,headers=["Product ID","Total Quantity Sold","Total Revenue"],tablefmt="grid"))
                        elif choice == "3":
                            print("\n",months,"\n")
                            month = input("➤ Enter month's key : ")
                            if month not in months:
                                print("\n✗ Invalid month key")
                                continue
                            year = input("➤ Enter year : ")
                            if not year.isdigit():
                                print("\n✗ Invalid input, Year must contain digits")
                                continue
                            user_cur.execute("Select * from Sales where sale_date like '%s'"%(year + "-" + month + "-%",))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n⚠ No sales found for this month")
                                continue
                            no_of_sales = len(data)
                            total_income = 0
                            highest_sale = data[0][4]
                            for row in data:
                                total_income += row[4]
                                if row[4] > highest_sale:
                                    highest_sale = row[4]
                            average_sale = total_income/no_of_sales
                            user_cur.execute("""Select P_ID,Sum(Quantity),Sum(Total_Amount) from Sales where sale_date like '%s'
                            group by P_ID"""%(year + "-" + month + "-%",))
                            product_data = user_cur.fetchall()
                            ranking = list()
                            for row in product_data:
                                ranking.append([row[0],row[1],row[2]])
                            for i in range(len(ranking)):
                                for j in range(i + 1,len(ranking)):
                                    if ranking[i][1] < ranking[j][1]:
                                        temporary = ranking[i]
                                        ranking[i] = ranking[j]
                                        ranking[j] = temporary
                            month=months[month]
                            most_sold_products = ""
                            for row in ranking:
                                if row[1] == ranking[0][1]:
                                    most_sold_products += row[0] + ", "
                            print("\n==============================================================")
                            print("                    MONTHLY SALES SUMMARY")
                            print("==============================================================")
                            print("\n                         ",month,"-",year)
                            print("\n--------------------------------------------------------------")
                            print("                     SALES OVERVIEW")
                            print("--------------------------------------------------------------")
                            print("  Number of Sales       :",no_of_sales)
                            print("  Total Revenue          : ₹",total_income)
                            print("  Average Sale          : ₹",int(average_sale))
                            print("\n--------------------------------------------------------------")
                            print("                    SALES HIGHLIGHTS")
                            print("--------------------------------------------------------------")
                            print("  Most Selling Product  :",most_sold_products[:-2])
                            print("  Quantity Sold         :",ranking[0][1])
                            print("\n  Highest Sale          : ₹",highest_sale)
                            print(" (",month,"-",year,")")
                            print("\n--------------------------------------------------------------")
                            print("                 PRODUCT SALES RANKING")
                            print("--------------------------------------------------------------")
                            result = []
                            rank = 1
                            for i in range(len(ranking)):
                                if i > 0 and ranking[i][1] != ranking[i-1][1]:
                                    rank += 1
                                result.append([rank,ranking[i][0],ranking[i][1],ranking[i][2]])
                            print(tabulate(result,headers=["Rank","Product ID","Quantity Sold","Total Revenue"],tablefmt="grid"))
                        elif choice == "4":
                            year = input("➤ Enter year : ")
                            if not year.isdigit():
                                print("\n✗ Invalid input, Year must contain digits")
                                continue
                            user_cur.execute("Select * from Sales where sale_date like '%s'"%(year + "-%",))
                            data = user_cur.fetchall()
                            if len(data) == 0:
                                print("\n⚠ No sales found for this year")
                                continue
                            no_of_sales = len(data)
                            total_income = 0
                            highest_sale = data[0][4]
                            for row in data:
                                total_income += row[4]
                                if row[4] > highest_sale:
                                    highest_sale = row[4]
                            average_sale = total_income/no_of_sales
                            user_cur.execute("""Select P_ID,Sum(Quantity),Sum(Total_Amount) from Sales where sale_date like '%s'
                            group by P_ID"""%(year + "-%",))
                            product_data = user_cur.fetchall()
                            ranking = list()
                            for row in product_data:
                                ranking.append([row[0],row[1],row[2]])
                            for i in range(len(ranking)):
                                for j in range(i + 1,len(ranking)):
                                    if ranking[i][1] < ranking[j][1]:
                                        temporary = ranking[i]
                                        ranking[i] = ranking[j]
                                        ranking[j] = temporary
                            most_sold_products = ""
                            for row in ranking:
                                if row[1] == ranking[0][1]:
                                    most_sold_products += row[0] + ", "
                            print("\n==============================================================")
                            print("                     YEARLY SALES SUMMARY")
                            print("==============================================================")
                            print("\n                         ",year)
                            print("\n--------------------------------------------------------------")
                            print("                     SALES OVERVIEW")
                            print("--------------------------------------------------------------")
                            print("  Number of Sales       :",no_of_sales)
                            print("  Total Revenue          : ₹",total_income)
                            print("  Average Sale          : ₹",int(average_sale))
                            print("\n--------------------------------------------------------------")
                            print("                    SALES HIGHLIGHTS")
                            print("--------------------------------------------------------------")
                            print("  Most Selling Product  :",most_sold_products[:-2])
                            print("  Quantity Sold         :",ranking[0][1])
                            print("\n  Highest Sale          : ₹",highest_sale)
                            print(" (",year,")")
                            print("\n--------------------------------------------------------------")
                            print("                 PRODUCT SALES RANKING")
                            print("--------------------------------------------------------------")
                            result = []
                            rank = 1
                            for i in range(len(ranking)):
                                if i > 0 and ranking[i][1] != ranking[i-1][1]:
                                    rank += 1
                                result.append([rank,ranking[i][0],ranking[i][1],ranking[i][2]])
                            print(tabulate(result,headers=["Rank","Product ID","Quantity Sold","Total Revenue"],tablefmt="grid"))
                        elif choice == "5":
                            print("\n↩️  Returning to the previous menu...")
                            break    
                        else:
                            print("\n⚠ Invalid choice.")
                            print("  Please select an option from 1 to 5.")
                elif choice == "7":
                    print("\n↩ Returning to the previous menu...")
                    break
                else:
                    print("\n⚠ Invalid choice.")
                    print("  Please select an option from 1 to 7.")
        elif choice == "3":         
            print("\n↩ Returning to the previous menu...")
            break
        else:
            print("\n⚠ Invalid choice.")
            print("  Please select an option from 1 to 3.")




print("\n")
print("              ✦  E M P O W E R   Y O U R   I D E A S  ✦")
print()
print("                  🚀  ENTREPRENEUR ASSISTANT")
print("                ═══════════════════════════════")
print("                   IDEAS  •  INNOVATION  •  GROWTH")
print()
print("                          ◆  EST. 2026  ◆")
while True:
    print("\n+------------------------------------------+")
    print("|               🔐 MAIN MENU               |")
    print("+------------------------------------------+\n")
    print("  Press 1 ----> 🔑 Admin Login")
    print("  Press 2 ----> 👤 User Login\n")
    choice = input("➤ Please select an option to continue: ")
    if choice == "1":
        admin_attempts = 1
        print("\n+------------------------------------------+")
        print("|                🔑 ADMIN LOGIN            |")
        print("+------------------------------------------+")
        while True:
            print("\n  Attempt", admin_attempts, "of 3")
            admin_name = input("➤ Enter Admin ID: ")
            admin_password = input("➤ Enter Password: ")
            if admin_name == "arun" and admin_password == "1234":
                print("\n✓ Admin login successful!")
                break
            admin_attempts += 1
            if admin_attempts == 4:
                print("\n⚠ Invalid admin ID or password.")
                print("  Too many unsuccessful login attempts.")
                print("  Program exiting...")
                sys.exit()
            else:
                print("\n⚠ Invalid admin ID or password.")
                print("  Please try again.")
            if admin_attempts == 3:
                print("\n⚠ Careful! This is your last attempt.")
        print("\n+------------------------------------------+")
        print("|               👋 WELCOME ADMIN           |")
        print("+------------------------------------------+")
        print("|              📊 ADMIN DASHBOARD          |")
        print("+------------------------------------------+")
        loading_bar("INITIALIZING ADMIN CONTROL PANEL",0.04,43)
        while True:
            print("\n+------------------------------------------+")
            print("|               ⚙ ADMIN MENU              |")
            print("+------------------------------------------+")
            print("\n  Press 1 ----> 💼 Manage Business Ideas")
            print("  Press 2 ----> 👥 Manage Users")
            print("  Press 3 ----> 📧 Update Your Email")
            print("  Press 4 ----> ↩ Back\n")
            choice = input("➤ Please select an option to continue: ")
            if choice == "1":
                while True:
                    print("\n+------------------------------------------+")
                    print("|             🏢 BUSINESS IDEAS            |")
                    print("+------------------------------------------+")
                    print("\n  Press 1 ----> 🔍 View Business Ideas")
                    print("  Press 2 ----> ➕ Add Business Idea")
                    print("  Press 3 ----> ✏️ Update Business Idea")
                    print("  Press 4 ----> 🗑  Delete Business Idea")
                    print("  Press 5 ----> ↩ Back\n")
                    print("+------------------------------------------+")
                    choice = input("➤ Please select an option to continue: ")
                    if choice == "1":
                        print("\n+------------------------------------------+")
                        print("|           📋 BUSINESS DIRECTORY          |")
                        print("+------------------------------------------+")
                        loading_bar("Fetching records...",0.01,51)
                        cur.execute("Select * from business_ideas")
                        records = cur.fetchall()
                        if len(records) > 0:
                            print("\n✓ Business ideas retrieved successfully!")
                            print("  Here are the registered business ideas:\n")
                            print(tabulate(records,headers=["B_ID","B_Name","Department","Startup Cost",
                            "Skills","License","Demand","Risk"],tablefmt="grid"))
                            print("\n✓ Business ideas displayed successfully.")
                        else:
                            print("\n⚠ No business ideas found.")
                            print("  Add a new business idea to get started.")
                    elif choice == "2":
                        print("\n+------------------------------------------+")
                        print("|           ✚ ADD BUSINESS IDEA            |")
                        print("+------------------------------------------+")
                        print("  Let's add a new business opportunity!")
                        print("  Please provide the required details below.\n")
                        b_id = add_uid("B","B_ID","Business_Ideas")
                        b_name = input("➤ Enter Business Name: ")
                        if b_name == "":
                            print("⚠ Business name is required. Please try again.")
                            continue
                        dept = input("➤ Enter the Department: ")
                        if dept == "":
                            print("⚠ Department is required. Please try again.")
                            continue
                        startup_cost = input("➤ Enter Minimum Startup Cost: ")
                        if startup_cost == "":
                            print("⚠ Startup cost is required. Please try again.")
                            continue
                        if not startup_cost.isdigit():
                            print("⚠ Amount should contain numbers only.")
                            continue
                        skills = input("➤ Enter Required Skills: ")
                        if skills == "":
                            print("⚠ Required skills must be entered.")
                            continue
                        print("\n✎ License Information")
                        print("  Use commas to separate multiple licenses.")
                        License = input("➤ Enter License Details: ")
                        if License == "":
                            print("⚠ License details are required. Please try again.")
                            continue
                        print("\n📊 Demand Options")
                        print(options)
                        demand = input("➤ Enter Demand's Key: ")
                        if demand == "":
                            print("⚠ You must enter a demand key.")
                            continue
                        if demand not in options:
                            print("⚠ Invalid demand key. Please try again.")
                            continue
                        demand = options[demand]
                        print("\n⚠ Risk Options")
                        print(options)
                        risk = input("➤ Enter Risk's Key: ")
                        if risk == "":
                            print("⚠ You must enter a risk key.")
                            continue
                        if risk not in options:
                            print("⚠ Invalid risk key. Please try again.")
                            continue
                        risk = options[risk]
                        cur.execute("Insert into business_ideas values ('%s','%s','%s','%s','%s','%s','%s','%s')"%
                        (b_id,b_name.upper(),dept.upper(),int(startup_cost),skills.upper(),License.upper(),demand,risk))
                        x.commit()
                        loading_bar("Saving new details...",0.015,50)
                        print(" ✓ Business idea registered successfully!")
                    elif choice == "3":
                        print("\n+------------------------------------------+")
                        print("|         ⚙ UPDATE BUSINESS IDEA           |")
                        print("+------------------------------------------+")
                        print("  Update the selected business idea.")
                        print("  Leave a field empty to keep its existing value.\n")
                        b_id = input("➤ Enter Business ID to Update: ")
                        cur.execute("select * from business_ideas where b_id='%s'"%(b_id,))
                        data = cur.fetchone()
                        if data is None:
                            print("\n⚠ Business ID not found.")
                            print("  Please enter an existing Business ID.")
                            continue
                        print("\n✎ Enter the details below to update.")
                        b_name = input("➤ Enter Business Name: ")
                        if b_name == "":
                            b_name = data[1]
                        dept = input("➤ Enter the Department: ")
                        if dept == "":
                            dept = data[2]
                        startup_cost = input("➤ Enter Minimum Startup Cost: ")
                        if startup_cost == "":
                            startup_cost = data[3]
                        elif not startup_cost.isdigit():
                            print("⚠ Amount should contain numbers only.")
                            continue
                        else:
                            startup_cost = int(startup_cost)
                        skills = input("➤ Enter Required Skills: ")
                        if skills == "":
                            skills = data[4]
                        print("\n✎ License Information")
                        print("  Use commas to separate multiple licenses.")
                        License = input("➤ Enter the required Licenses: ")
                        if License == "":
                            License = data[5]
                        print("\n📊 Demand Options")
                        print(options)
                        demand = input("➤ Enter Demand's Key (or press Enter to keep existing): ")
                        if demand == "":
                            demand = data[6]
                        elif demand not in options:
                            print("⚠ Invalid demand key. Please try again.")
                            continue
                        else:
                            demand = options[demand]
                        print("\n⚠ Risk Options")
                        print(options)
                        risk = input("➤ Enter Risk's Key (or press Enter to keep existing): ")
                        if risk == "":
                            risk = data[7]
                        elif risk not in options:
                            print("⚠ Invalid risk key. Please try again.")
                            continue
                        else:
                            risk = options[risk]
                        cur.execute("""Update business_ideas set b_name='%s',dept='%s',cost_lm=%s,skills='%s',license='%s',
                        demand='%s',risk='%s' where b_id='%s'"""%(b_name.upper(),dept.upper(),startup_cost,skills.upper(),
                        License.upper(),demand,risk,b_id))
                        x.commit()
                        loading_bar("Saving modifications...",0.015,49)
                        print("\n✓ Business idea details updated successfully!")
                        print("  Your changes have been saved.")
                    elif choice == "4":
                        print("\n+------------------------------------------+")
                        print("|         ✖ DELETE BUSINESS IDEA           |")
                        print("+------------------------------------------+")
                        print("  Find and remove a registered business idea.\n")
                        b_id = input("➤ Enter the Business ID: ")
                        cur.execute("Select b_id from business_ideas where b_id='%s'"%(b_id,))
                        records = cur.fetchall()
                        if len(records) == 0:
                            print("\n⚠ Business ID not found.")
                            print("  Please check the ID and try again.")
                            continue
                        print("\n⚠ Deletion Confirmation")
                        print("  This action will permanently remove the business idea.")
                        sure = input("➤ Are you sure you want to delete it? (Yes/No): ")
                        if sure.lower() != "yes":
                            print("\n↩ Deletion cancelled.")
                            print("  The business idea remains unchanged.")
                            continue
                        cur.execute("Delete from business_ideas where b_id='%s'"%(b_id,))
                        x.commit()
                        update_uid(cur,x,"Business_Ideas","B_ID","B",b_id)
                        loading_bar("Removing selected record...",0.015,46)
                        print("\n✓ Business idea deleted successfully.")
                        print("  The record has been removed from the system.")
                    elif choice == "5":
                        print("\n↩ Returning to the previous menu...")
                        break
                    else:
                        print("\n⚠ Invalid choice.")
                        print("  Please select an option from 1 to 5.")
            elif choice == "2":
                while True:
                    print("\n+------------------------------------------+")
                    print("|               👤 MANAGE USERS            |")
                    print("+------------------------------------------+")
                    print("\n  Press 1 ----> 🔍 View User Details")
                    print("  Press 2 ----> ➕ Add New User")
                    print("  Press 3 ----> ✏️ Update User Details")
                    print("  Press 4 ----> 🗑  Delete User")
                    print("  Press 5 ----> ↩ Back\n")
                    choice = input("➤ Please select an option to continue: ")
                    if choice == "1":  # Viewing User
                        print("\n+------------------------------------------+")
                        print("|             👥 USER DIRECTORY            |")
                        print("+------------------------------------------+")
                        loading_bar("Fetching records...",0.01,51)
                        cur.execute("Select * from user_ids")
                        data = cur.fetchall()
                        if len(data) > 0:
                            print("\n✓ User records retrieved successfully!")
                            print("Here are the details of registered users:\n")
                            print(tabulate(data,headers=["User ID","User Name","Password","Status","Email"],tablefmt="grid"))
                            print("\n➤ Users displayed successfully.")
                            continue
                        else:
                            print("\n⚠ No user accounts found.")
                            continue
                    elif choice == "2":  # Adding User
                        print("\n+------------------------------------------+")
                        print("|             ✚ CREATE ACCOUNT            |")
                        print("+------------------------------------------+")
                        print("  Let's get a new user registered!")
                        print("  Please provide the required details below.\n")
                        uid = add_uid("U","u_id","user_ids")
                        user_name = input("➤ Enter the User Name: ")
                        if user_name == "":
                            print("⚠ User name is required. Please try again.")
                            continue
                        cur.execute("Select User_name from user_ids where user_name='%s'"%(user_name,))
                        if len(cur.fetchall()) != 0:
                            print("⚠️ Username already exists!")
                            continue
                        password = input("➤ Create a Password: ")
                        if password == "":
                            print("⚠ Password is required. Please try again.")
                            continue
                        print("\n✉ Email Verification")
                        email = input("➤ Enter the email:")
                        if email == "":
                            print("⚠ Email is required. Please try again.")
                            continue
                        ok = check_email(email)
                        if ok:
                            otp = randint(100000,999999)
                            message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                            send_notification(email,message)
                            print("  A verification code will be sent to your email.")
                            print("\n➤ Please check your inbox for the verification code.")
                            print("  If you did not receive it, enter any alphabet to cancel.")
                            entered_otp = input("➤ Enter the OTP: ")
                            if str(otp) == entered_otp:
                                print("\n✓ Email verification completed successfully!")
                                cur.execute("""Insert into user_ids values('%s','%s','%s','%s','%s')"""%(uid,user_name,password,
                                "Unlocked",email))
                                x.commit()
                                loading_bar("Registering new entry...",0.015,48)
                                print("  ✓ The new user has been registered successfully!")
                            else:
                                print("\n✗ Verification failed.")
                                print("  The OTP is incorrect. No account was created.")
                        else:
                            continue
                    elif choice == "3":  # Updating User
                        print("\n+------------------------------------------+")
                        print("|              ⚙ UPDATE ACCOUNT           |")
                        print("+------------------------------------------+")
                        print("  Update the selected user's account details.")
                        print("  Leave a field empty to keep its existing value.\n")
                        uid = input("➤ Enter the User ID to update: ")
                        cur.execute("Select * from user_ids where U_ID='%s'"%(uid,))
                        data = cur.fetchone()
                        if data is None:
                            print("\n⚠ User ID not found.")
                            print("  Please enter an existing User ID.")
                            continue
                        print("\n✎ Enter the new details below.")
                        uname = input("➤ Enter User Name: ")
                        if uname == "":
                            uname = data[1]
                        password = input("➤ Enter Password: ")
                        if password == "":
                            password = data[2]
                        status = input("➤ Enter Status (Locked OR Unlocked): ")
                        if status == "":
                            status = data[3]
                        elif status.upper() != "LOCKED" and status.upper() != "UNLOCKED":
                            print("⚠ Invalid status. Please try again.")
                            continue
                        email = input("➤ Enter Email: ")
                        if email == "":
                            email = data[4]
                        else:
                            ok = check_email(email)
                            if not ok :
                                continue
                            otp = randint(100000,999999)
                            message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                            send_notification(email,message)
                            entered_otp = input("➤ Enter the OTP: ")
                            if str(otp) != entered_otp:
                                print("✗ Incorrect OTP. Email was not verified.")
                                continue
                            print("✓ Email verification completed successfully!")
                        cur.execute("""update user_ids set user_name='%s',password='%s',status='%s',email='%s' where u_id='%s'"""
                        %(uname,password,status.title(),email,uid))
                        x.commit()
                        loading_bar("Saving modifications...",0.015,49)
                        print("\n✓ User account details updated successfully!")
                        print("  Your changes have been saved.")
                    elif choice == "4":  # Deleting User
                        print("\n+------------------------------------------+")
                        print("|             ✖ DELETE ACCOUNT            |")
                        print("+------------------------------------------+")
                        print("  Find and remove a registered user account.")
                        uid = input("\n➤ Enter the User ID: ")
                        cur.execute("Select User_name from user_ids where U_ID='%s'"%(uid,))
                        if cur.fetchone() is None:
                            print("\n⚠ User ID not found.")
                            print("  Please check the ID and try again.")
                            continue
                        print("\n⚠ Account deletion confirmation")
                        print("  This action will permanently remove the user account.")
                        sure = input("➤ Are you sure you want to delete it? (Y/N): ").lower()
                        if sure == "y":
                            cur.execute("Delete from user_ids where U_ID='%s'"%(uid,))
                            x.commit()
                            print("\n✓ User account deleted successfully.")
                            loading_bar("Removing selected record...",0.015,46)
                            print("  The account has been removed from the system.")
                            update_uid(cur,x,"user_ids","U_ID","U",uid)
                        else:
                            print("\n↩ Deletion cancelled.")
                            print("  The user account remains unchanged.")
                    elif choice == "5":  # Back
                        print("\n↩ Returning to the previous menu...")
                        break
                    else:
                        print("\n⚠ Invalid choice.")
                        print("  Please select an option from 1 to 5.")
            elif choice == "3":
                cur.execute("Select Email from Admin_Details")
                current_email = cur.fetchall()[0][0]
                print("\n+------------------------------------------+")
                print("|          📧 ADMIN EMAIL SETTINGS         |")
                print("+------------------------------------------+")
                print()
                print("   📩 Current Admin Email :",current_email)
                print()
                print("   🔄 Enter your new email address below")
                print("   ──────────────────────────────────────")
                while True:
                    email = input("➤ Enter the email:")
                    ok = check_email(email)
                    if ok:
                        otp = randint(100000,999999)
                        message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                        send_notification(email,message)
                    else:
                        break
                    print("\n   🔐 EMAIL VERIFICATION")
                    print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    print("   📬 Enter the OTP received in your new email.")
                    print("   💡 No OTP received? Type something to exit.")
                    entered_otp = input("\n➤ Enter the OTP : ")
                    if str(otp) == entered_otp:
                        print("\n   ✅ OTP VERIFIED SUCCESSFULLY!")
                        cur.execute("Update admin_details set email = '%s'"%(email,))
                        x.commit()
                        loading_bar("Saving modifications...",0.015,49)
                        print("   📧 ADMIN EMAIL UPDATED SUCCESSFULLY!")
                        print("\n   ✦ Email settings saved securely ✦")
                        print()
                        break
                    else:
                        print("\n   ❌ INCORRECT OTP")
                        print("   ⚠️ Email verification failed.")
                        print()
                        break
            elif choice == "4":
                print("\n↩ Returning to the previous menu...")
                break
            else:
                print("\n⚠ Invalid choice.")
                print("  Please select an option from 1 to 4.")
    elif choice == "2":
        print("\n+----------------------------------------------+")
        print("|               👤 USER LOGIN MENU             |")
        print("+----------------------------------------------+")
        while True:
            print("\n  Press 1 ----> ✚ Create New Account")
            print("  Press 2 ----> 🔑 Signup")
            print("  Press 3 ----> ↩ Back\n")
            choice = input("➤ Please select an option to continue: ")
            if choice == "1":
                print("\n+------------------------------------------+")
                print("|            ✚ CREATE ACCOUNT             |")
                print("+------------------------------------------+")
                #b_id = add_uid("B","B_ID","Business_Ideas")
                uid = add_uid("U","U_ID","User_Ids")
                username = input("➤ Enter the Username: ")
                if username == "":
                    print("\n⚠ Username cannot be empty! Please enter your username.")
                    continue
                cur.execute("Select * from user_ids where user_name = '%s'"%(username,))
                if len(cur.fetchall()) > 0:
                    print("\n⚠ Username already taken! Try another name.")
                    continue
                password = input("➤ Enter the Password: ")
                if password == "":
                    print("\n⚠ Password cannot be empty! Please enter your password.")
                    continue
                email = input("➤ Enter the email:")
                if email == "":
                    print("\n⚠ Email cannot be empty! Please enter your email.")
                    continue
                ok = check_email(email)
                if ok:
                    print("\n📧 Sending OTP to your email...")
                    otp = randint(100000,999999)
                    message = "Subject: Your OTP\n\nYour OTP is: " + str(otp)
                    send_notification(email,message)
                    entered_otp = input("➤ Enter the OTP: ")
                    if entered_otp == str(otp):
                        print("\n✓ OTP Verified Successfully!")
                        cur.execute("""Insert into user_ids (u_id,user_name,password,status,email) values
                        ('%s','%s','%s','%s','%s')"""%(uid,username,password,"Unlocked",email))
                        cur.execute("create database if not exists " + username)
                        x.commit()
                        print("  ✓ Your account has been registered successfully!")
                        user_menu(username)
                        continue
                    else:
                        print("\n✗ Incorrect OTP! Account not created.")
                else:
                    pass
            elif choice == "2":
                print("\n+------------------------------------------+")
                print("|                 🔑 SIGNUP                |")
                print("+------------------------------------------+")
                cur.execute("Select * from admin_details")
                admin_email = cur.fetchone()
                attempts = 1
                username = input("➤ Enter the Username: ")
                if username == "":
                    print("\n⚠ Username cannot be empty! Please enter your username.")
                    continue
                cur.execute("Select * from user_ids where user_name = '%s'"%(username,))
                data = cur.fetchall()
                if len(data) == 0:
                    print("\n✗ Invalid Username!")
                    continue
                account_status = data[0][-2]
                if account_status.lower() == "locked":
                    print("\n🔒 Account Locked!")
                    print("  Contact Admin to regain access.")
                    print("📧 Please contact Admin at",admin_email[0],"for assistance.")
                    sys.exit()
                while True:
                    print(" Attempt:",attempts,"of 3")
                    password = input("➤ Enter the Password: ")
                    if data[0][2] == password:
                        print("\n+------------------------------------------+")
                        print("|             ✓ LOGIN SUCCESSFUL           |")
                        print("+------------------------------------------+")
                        user_menu(username)
                        break
                    else:
                        print("\n✗ Invalid Password!")
                        attempts += 1
                    if attempts == 3:
                        print("Last attempt be careful!")
                    if attempts == 4:
                        print("\n⚠ Too many failed attempts!")
                        print("\n+------------------------------------------+")
                        print("|              🔒 SECURITY ALERT           |")
                        print("+------------------------------------------+")
                        print("|               ACCOUNT LOCKED             |")
                        print("+------------------------------------------+")
                        print("  Contact Admin to regain access.")
                        print("📧 Please contact Admin at",admin_email[0],"for assistance.")
                        message = "Subject: Your Account Has Been Locked Due To Unauthorised Access"
                        send_notification(data[0][-1],message,False)
                        cur.execute("Update user_ids set status = '%s' where user_name='%s'"%("Locked",username))
                        x.commit()
                        break
            elif choice == "3":
                print("\n↩ Returning to the previous menu...")
                break
            else:
               print("\n⚠ Invalid choice.")
               print("  Please select an option from 1 to 3.")
    else:
        print("\n⚠ Invalid choice.")
        print("  Please select an option from 1 to 2.")




        
