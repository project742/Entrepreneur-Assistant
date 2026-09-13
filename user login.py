import mysql.connector
from tabulate import tabulate
x = mysql.connector.connect(host="localhost",user="root",password="root",database="arun")
cur = x.cursor()

def input_phone():
   while True:
       phone = input("Enter Phone Number: ")
       if len(phone) == 10:
            pass
       else:
            print("Invalid phone number. Enter exactly 10 digits.")
            continue
       if phone.isdigit():
            return phone
       else:
            print("Invalid phone number. Enter only digits.")
            
while True:
    print("Press 1 ----> Login")
    print("Press 2 ----> Signup")
    print("Press 3 ----> Back")
    choice = input("Enter the choice:").lower()
    if choice == "1":
        while True:
            username = input("Enter the Username:")
            cur.execute("Select * from user_ids where user_name = '%s'"%(username,))
            if len(cur.fetchall()) > 0:
                print("Username already Taken,Try another name")
                continue
            break
        password = input("Enter the Password:")
        cur.execute("Insert into user_ids  (user_name,password,phone) values ('%s','%s','%s')"%
        (username,password,input_phone()))
        x.commit()
        print("Account Created Successfully")
    elif choice == "2":
        attempts = 0
        while True:
            username = input("Enter the username:")
            cur.execute("Select * from user_ids where user_name = '%s'"%(username,))
            data = cur.fetchall()
        
            if len(data) == 0:
                print("Invalid Username")
                break

            account_status = data[0][-1]
            if account_status.lower() == "locked":
                print("Account locked")
                break
            while True:
                attempts += 1
                print("Attempt: " + str(attempts) + " of 3")
                password = input("Enter the password:")

                if data[0][1] == password:
                    escape = True   
                    print("Account Found")
                    print("Welcome " + str(data[0][0]))
                    #user() ----> Function for user entire menu
                    break
                else:
                    print("Invalid Password")
                    if attempts == 3:
                        escape = True
                        print("Too many attempts..") #send notification to admin to change the no of attempts in the table"
                        print("\n-----------Security Alert-------------------")
                        print("Account Locked")
                        print("Contact Admin for the access of your account")
                        print("--------------------------------------------\n")
                        cur.execute("Update  user_ids set attempts = '%s' where user_name='%s'"%
                        ("Locked",username))
                        x.commit()
                        break
            if escape:
                break
    elif choice == "3":
       break
    else:
        print("Inavlid Input")
        continue
    continue

"""
+-----------+----------+-----------+----------+
| user_name | password | phone     | attempts |
+-----------+----------+-----------+----------+
| Arun      | 000      | NULL      | Unlocked |
| Vaish     | 111      | NULL      | Unlocked |
| Manish    | 8989     | NULL      | Unlocked |
| Shailesh  | 6767     | NULL      | Unlocked |
| dwe       | edew     | edw       | Unlocked |
| Aswanth   | ewd      | edwed     | Unlocked |
| Baish     | 121223   | 123123213 | Unlocked |
+-----------+----------+-----------+----------+"""
