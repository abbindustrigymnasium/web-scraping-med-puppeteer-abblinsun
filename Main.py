import json
import os
import matplotlib.pyplot as plt

# Definiera en function som clearar terminalen och eventuellt skriver ut min meny
def cls(bool = False, bool2 = False):
    #clearar bash terminalen
    os.system('clear')
    if bool:
        print("Smash Info".center(50))
        breakline()
        print("Move names:")
        # Skriver upp alla namnen på alla moves för användaren
        for move in data:
            print(move["Name"])
        breakline()
        if bool2:
            print("v - View a specific move")
            print("d - Diagrams")
            print("e - Exit the program")
            breakline()
    

# Definera en funktion för att slippa skriva print 50 "-" när jag ska ha en linje i programmet
def breakline():
    print("-"*50)

# Definera en plotterfunktion så jag slipper skriva i princip samma funktion 4 ggr
def plotter(x, y, list):
    xList = []
    yList = []
    for move in list:
        xList.append(move[x])
        try:
            yList.append(int(move[y].split("/")[0]))
            plt.annotate(move["Name"],
                            xy=(move[x], int(
                                move[y].split("/")[0])),
                            xytext=(move[x], int(move[y].split("/")[0])+1),)
        except:
            yList.append(0)
            plt.annotate(move["Name"],
                            xy=(move[x], 0),
                            xytext=(move[x], 1,))
    plt.plot(xList, yList, "o")
    plt.show()
    conBut()

# Definera funtion som agerar som continue knapp
def conBut():
    input("Press enter to continue...")

# Läser in datat från webscrapningen
with open("data.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())

# Då smashbros moves ofta har flera hitboxes och de ofta gör olika mängd skada så räknar jag ut ett medelvärde per hitbox och tar det gånger så många gånger den skadar
for move in data:
# Tar fram ett average damage för de olika hitboxerna för en attack samt städar lite då datat på hemsidan var lite konstigt
    AvgDmg = 0
    for dmgNum in move["Damage"].replace("(", "").replace(")", "").replace("%", "").split("/"):
        dmgNum = dmgNum.split("—")
        try:
            dmgNum[0] = dmgNum.split(",")
        except:
            pass
        if len(dmgNum) > 1:
            dmgNum = dmgNum[0]
        try:
            AvgDmg += float(dmgNum[0])
        except:
            pass
    AvgDmg = AvgDmg / len(move["Damage"].replace("(", "").replace(")", "").replace("%", "").split("/"))

# Räknar ut ungefärliga totala damagen för en attack genom att ta medeldamagen delat på antalet gånger det attakerar 
    move["Damage"] = AvgDmg*len(move["Startup"].split("/"))

#Själva programmet, en loop som kör tills man stänger av programmet
while True:
    cls(True, True)
    # Ber användaren mata in ett kommando
    action = input("Selection > ").lower().strip()
    breakline()
    # Stänger pogramet
    if action == "e":
        exit()
    # Ber användaren mata in namn på ett move för att man ska kunna se all data till det movet.
    elif action == "v":
        i = True
        while i:
            cls(True)
            selectedMove = input("Input move name: ").lower() 
            for move in data:
                if move["Name"].lower() == selectedMove:
                    for key, d in move.items():
                        print(f'{key}: {d}')
                    i = False
                    break

            else:
                print("Invalid Name...")       
                breakline()
                conBut()
        breakline()
        conBut()

    elif action == "d":
        cls()
        plt.clf()
        print("Diagram types:\n")
        print("1 | Damage - Total Frames")
        print("2 | Damage - Startup")
        print("3 | Damage - Endlag")
        print("4 | Startup - Total Frames")
        print("5 | Endlag - Total Frames")
        breakline()
        # Ber användaren mata in diagramtyp och ritar upp ett diagram med min plotterfunktion samt namnger axlarna på grafen och tar ett nytt värde om användaren matar in felaktikt värde
        while True:
            diaType = input("Dragram type > ").strip()
            if diaType == "1":
                plt.xlabel("Damage in %")
                plt.ylabel("Total frames")
                plotter("Damage", "TotalFrames", data,)
                break
            elif diaType == "2":
                plt.xlabel("Damage in %")
                plt.ylabel("Startup lag in frames")
                plotter("Damage", "Startup", data)
                break
            elif diaType == "3":
                plt.xlabel("Damage in %")
                plt.ylabel("End lag in frames")
                plotter("Damage", "EndLag", data)
                break
            elif diaType == "4":
                plt.xlabel("Startup in Frames")
                plt.ylabel("Total Frames")
                plotter("Startup", "TotalFrames", data)
                break
            elif diaType == "5":
                plt.xlabel("Endlag in Frames")
                plt.ylabel("Total Frames")
                plotter("EndLag", "TotalFrames", data)
                break
            else:
                print("invalid input. Try again...")
    else:
        print("Invalid input\n")
        conBut()