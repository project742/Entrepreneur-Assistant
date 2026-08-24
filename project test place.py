import mysql.connector as ms
import tabulate
x=ms.connect(host="localhost",user="root",passwd="root",database="arun")
cur=x.cursor()
userids=dict()

def check_id_for_admin(n,pwd):
    if n  not in userids:
        return  True
    else:
        print("Existing Username , try another username")
        userid=input("Enter the user name:")
        password=input("Enter the password:")
        check_id_for_admin(userid,password)
def admin_dashboard():
    print("1----> To Manage businessideas table")
    print("2----> To Manage businessideas1 table")
    print("3----> To Manage User_ids table")
    print("B---->Back")
    choice=input("Enter your choice:")
    if choice == "3":
        businessideas_table()
def businessideas_table():
    print("Press 1 -----> View User Details")
    print("Press 2 -----> Add a User")
    print("Press 3 -----> Delete a  User")
    print("Press B -----> Back")
    choice=input("Enter the choice:")
    if choice == "1":
        #fetching userid table
        cur.execute("Select * from user_ids")
        data=cur.fetchall()
        if len(data)>0:
            print("Showing User Id Details...")
            print(tabulate.tabulate(data, headers=["User Name", "Password"], tablefmt="grid"))
            businessideas_table()
        else:
            print("No Users Found")
            businessideas_table()
    elif choice == "2":
        #fetching userid table
        cur.execute("Select * from user_ids")
        data=cur.fetchall() 
        #fetching userid details
        for  i in data:
            userids[i[0]]=i[1]
        userid=input("Enter the User Id:")
        password=input("Enter the Password:")
        if check_id_for_admin(userid,password):
            cur.execute("insert into user_ids values('%s','%s')"%(userid,password))
            x.commit()
            print("User Added Successfully")
            businessideas_table()
    elif choice.lower() == "b":
        admin_dashboard()
    else:
        print("Invalid Input, Please Entry the Valid Option")
        businessideas_table()
admin_dashboard()
