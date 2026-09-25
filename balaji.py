"""def check_date():
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
    sender_password = ""
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
                            print("Invalid Input")"""
