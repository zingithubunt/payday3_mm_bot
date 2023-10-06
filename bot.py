import cv2
import pyautogui
import time
import PySimpleGUI as sg
import threading
import pathlib

heists = ["No rest for the wicked","Road Rage","Dirty Ice","Rock the Cradle","Under the Surphaze","Gold & Sharke","99 Boxes","Touch the Sky"]
difficulties = ["Normal","Hard","Very hard","Overkill"]
cancel = False
done = False
foundPlayers = False
foundLobby = False
path = str(pathlib.Path(__file__).parent.resolve())

def searchHeist(heist, difficulty):
    global cancel
    cancel = False

    heistX, heistY = 0, 0
    diffX, diffY = 1200, 770
    diffClicks = 0

    if difficulty == difficulties[0]:
        diffClicks = 0

    elif difficulty == difficulties[1]:
        diffClicks = 1

    elif difficulty == difficulties[2]:
        diffClicks = 2

    elif difficulty == difficulties[3]:
        diffClicks = 3

    if heist == heists[0]:
        heistX, heistY = 600, 700

    elif heist == heists[1]:
        heistX, heistY = 1400, 700

    elif heist == heists[2]:
        heistX, heistY = 330, 700

    elif heist == heists[3]:
        heistX, heistY = 950, 700

    elif heist == heists[4]:
        heistX, heistY = 1600, 700

    elif heist == heists[5]:
        heistX, heistY = 330, 700

    elif heist == heists[6]:
        heistX, heistY = 940, 700

    elif heist == heists[7]:
        heistX, heistY = 1600, 700

    pyautogui.leftClick(400, 300) 
    if heist in heists[2:5]: 
        pyautogui.leftClick(871, 836)
        time.sleep(0.3)
    elif heist in heists[5:8]: 
        pyautogui.leftClick(1385, 836)
        time.sleep(0.3)
    pyautogui.leftClick(heistX, heistY) 
    for i in range(diffClicks):
        pyautogui.moveTo(diffX+1, diffY+1) 
        pyautogui.leftClick(diffX, diffY) 
    pyautogui.leftClick(900, 800) 
    pyautogui.leftClick(400, 900) 
    time.sleep(0.3) 
    pyautogui.leftClick(400,900) 

def checkForPlayers():
    global cancel
    global foundPlayers
    count = 0
    image = pyautogui.locateOnScreen(path+"\\noPlayersInLobby.png", grayscale=True, confidence=.8)
    while image == None:
        image = pyautogui.locateOnScreen(path+"\\noPlayersInLobby.png")
        print("Players in lobby?")
        time.sleep(0.5)
        count = count+1
        if count>4:
            cancel = True
            foundPlayers = True
            break

        if cancel == True:
            break

    if cancel is not True:
        pyautogui.leftClick(400,850)
        pyautogui.leftClick(920,580)
        time.sleep(2)

def lobbyFound():
    image = pyautogui.locateOnScreen(path+"\\foundLobby.png")
    
    while image == None:
        image = pyautogui.locateOnScreen(path+"\\foundLobby.png", grayscale=True, confidence=.8)

        if cancel == True:
            break
        
    if cancel is not True:
        checkForPlayers()

def gui():
    global cancel

    layout = [
        [sg.Text("Heist:"), sg.OptionMenu(values=heists, size=20, key="-HEIST-", disabled=False)],
        [sg.Text("Difficulty:"), sg.OptionMenu(values=difficulties, size=20, key="-DIFFICULTY-", disabled=False)],
        [sg.Button("search", size=20, disabled=False), sg.Button("cancel", size=20, disabled=True)]
    ]

    window = sg.Window("PAYDAY3 Matchmaking Bot", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "search":

            window["-HEIST-"].update(disabled=True)
            window["-DIFFICULTY-"].update(disabled=True)
            window["search"].update(disabled=True)

            selected_heist = values["-HEIST-"] 
            selected_difficutly = values["-DIFFICULTY-"] 
            
            searchHeist(selected_heist, selected_difficutly)

            window["cancel"].update(disabled=False)
            window.perform_long_operation(lobbyFound, "-OPERATION DONE-")

        elif event == "-OPERATION DONE-":
            if cancel == True:
                print("Search canceled!")
                if foundPlayers is True:
                    sg.popup_ok("Players found!", keep_on_top=True)
                    window.write_event_value("cancel", "cancel")
            else:
                window.write_event_value("search", "search")

        elif event == "cancel":
            cancel = True
            window["-HEIST-"].update(disabled=False)
            window["-DIFFICULTY-"].update(disabled=False)
            window["search"].update(disabled=False)
            window["cancel"].update(disabled=True)


if __name__ == "__main__":
    gui()
