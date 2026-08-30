import mysql.connector
x = mysql.connector.connect(host="localhost",user="root",password="root",database="arun")
cur = x.cursor()
cur.execute("SELECT B_ID, B_NAME FROM business_ideas")
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
