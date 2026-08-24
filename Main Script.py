import pickle

def available(name):
    while name in Dict:
        print("Name taken, try another name")
        global Uname
        uname=input("Enter the username:")
    Uname=uname
    return True
def checkid(n,Id):
    if n in Dict and Dict[n]==Id:
        print("Opening main menu")
    else:
        print("Incorrect password or username , try again")
        uname=input("Enter the user name:")
        Pass=input("Enter the password:")
        checkid(uname,Pass)
    
        
#getting registered username and password
f=open("E:\Python Programs\Project\project.bin","rb+")
Dict=pickle.load(f)


#Create\Login system
print("Press 1 to Create a account")
print("Press 2 to Signup")
wish=int(input("Enter your choice:"))


if wish==1:
    uname=input("Enter the username:")
    if available(uname):
        password=input("Enter the password:")
        Dict.update({Uname:password})
        f.seek(0)
        pickle.dump(Dict,f)
        print(pickle.load(f))
        f.close()
        
        print("Account created successfully")
        print("Opening main menu")

elif wish==2:
    uname=input("Enter the user name:")
    Pass=input("Enter the password:")
    checkid(uname,Pass)
    



"""
    roll=int(input("Enter the number:"))
    name=input("Enter the name:")
    conn=mysql.connector.connect(host="localhost",password="root",user="root")
    cur=conn.cursor()
    cur.execute("Create database " + db)
    conn.close()

    conn=mysql.connector.connect(host="localhost",password="root",user="root",database=db)
    cur=conn.cursor()
    cur.execute("CREATE table t1(roll int,name varchar(30))")
    sql="insert into t1 values (%s,%s)"
    data=(roll,name)
    cur.execute(sql,data)
    conn.commit()
    
    conn.close()

#cur.execute(create database project)
#cur.execute("CREATE table t1(roll int,name varchar(30))")

#cur.execute("insert into t1 values(3,'kumar')")
#conn.commit()
"""
