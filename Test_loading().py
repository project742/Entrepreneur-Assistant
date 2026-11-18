import time
def loading_bar(text,delay,space):
    print("\n")
    print("                                                   ⚙ PLEASE WAIT...")
    print(" "*space + text + "\n")
    print("                                              [",end="")
    for i in range(24): 
        print("█",end="")
        time.sleep(delay)
    print("] 100%")
    print("\n")
loading_bar("Registering new entry...",0.015,48)

