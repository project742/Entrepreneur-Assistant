import mysql.connector as ms
x=ms.connect(host="localhost",user="root",passwd="root",database="arun")
cur=x.cursor()
L=dict()
n=1
page=0

cur.execute("Select name from articles")
data = cur.fetchall()

for i in data:
    for j in i:
        L[n]=j
    n+=1
print(L)  #busuiness names

def book():
    a=0
    print("====Book====")
    print("Page:1 ")
    for i,j in L.items():
        print(i,"\t",j)
        a+=1
        if a%10==0:
            break
    print("p--->previous page n--->next page")
        
book()
