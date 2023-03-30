"""
Clot - Terminal v 0.0.1
Author : Cactochan

Status  : Somehow works :)
"""


from pynput import keyboard
import subprocess
from sty import fg , bg
import os
import json
import platform
import atexit
import random
import requests

###################################

VERSION = "0.0.1"
CLOT_DIR_ = __file__.split("/").pop()
CLOT_DIR = ""
for e in CLOT_DIR_:
    CLOT_DIR += e

try:
    conf =  open(CLOT_DIR + ".conf", "r")
    COLOR = conf.read()
    conf.close()
except:
    COLOR = ""

if COLOR == "":
    COLOR = False

R = random.choice([70,100,150,180,240])
G = random.choice([70,100,150,180,240])
B = random.choice([70,100,150,180,240])

OS = platform.system()


"""
def times_to():
    size = os.get_terminal_size()
    return int(size.columns)

def back_space():
    print("\b \b", end="")

CUR_KEY = ""

def on_press(key):
    global CUR_KEY

    if key == keyboard.Key.up:
        for e in range(0, int(times_to())-10):
            back_space()

        cur = open(CLOT_DIR+".history_terminal_s", "r").readlines()

        if CUR_KEY == "":
            CUR_KEY = 1

        else:
            CUR_KEY += 1

        print(bg(142, 155, 250)+fg(230,230,230)+f"@{os.getcwd()} [Root:{root}]"+fg.rs+bg.rs, end = "")
        cmd = input(": ")
        CUR_KEY = 1
        print(cur[CUR_KEY * -1], end="")

    elif key == keyboard.Key.down:
        for e in range(0, int(times_to())):
            back_space()

        cur = open(CLOT_DIR+".history_terminal_s", "r").readlines()

        if CUR_KEY == "":
            CUR_KEY = 1

        else:
            CUR_KEY -= 1

        CUR_KEY = 1
        print(bg(142, 155, 250)+fg(230,230,230)+f"@{os.getcwd()} [Root:{root}]"+fg.rs+bg.rs, end = "")
        cmd = input(": ")

        print(cur[CUR_KEY * -1], end="")


listener = keyboard.Listener(
    on_press=on_press)
listener.start()
"""


def add_to_history(cmd):
    try:
        cur = open(CLOT_DIR+".history_terminal_s", "r").readlines()
    except:
        cur = [""]
        os.system(f"touch {CLOT_DIR}.history_terminal_s")

    try:
        if cur[-1][:-1] == cmd:
            return None
    except:
        pass

    f = open(CLOT_DIR+".history_terminal_s", "a")
    f.write(cmd+"\n")
    f.close()


def terminal_width():
    return os.get_terminal_size().columns


def colored(char):
    global R, G, B

    if R < 240:
        R += 5
        return fg(R, G, B) + char + fg.rs

    if R == 240 and B < 240:
        B += 5
        return fg(R, G, B) + char + fg.rs

    if R == 240 and B == 240 and G < 240:
        G += 5
        return fg(R, G, B) + char + fg.rs

    if R and  B and  G == 240:
        R =  random.choice([70,100,150,180,240])
        G =  random.choice([70,100,150,180,240])
        B =  random.choice([70,100,150,180,240])

    if R < 240:
        R += 5
        return fg(R, G, B) + char + fg.rs

    if R == 240 and B < 240:
        B += 5
        return fg(R, G, B) + char + fg.rs

    if R == 240 and B == 240 and G < 240:
        G += 5
        return fg(R, G, B) + char + fg.rs


def exit_man():
    try:
        std_out.close()
    except:
        pass
    try:
        std_out_r.close()
    except:
        pass
    try:
        os.remove(CLOT_DIR+".<<std:out>>")
    except:
        pass
    print("exited")

    
def make_list(str_):
    str_ = str_.replace(" ", "")
    str_ = str_.split(",")
    list_ = []
    for e in str_:
        list_.append(e)
    return list_


def get_command_book(p = True):
    global COLOR

    file_ = CLOT_DIR + "cmd.book.db.json"

    try:
        file = open(file_, "r")
        content = json.loads(file.read())
        file.close()
    except:
        content = ""

    if p:

        if content == "":
            print("No Commands Stored")
        else:
            con = ""
            n = 0

            for e in content:
                con += f"{n} : {e} -- > {content[e]} \n"
                n += 1

            for line in con:
                if  COLOR == False:
                    for char in line:
                        print(colored(char), end="")
                else:
                    if type(COLOR) == str:
                        COLOR = make_list(COLOR)
                    print(fg(COLOR[0], COLOR[1], COLOR[2]) +line+ fg.rs, end="")

    else:
        if content == "":
            return {}

        return content

    
def remove_command(cmd):
    file_ = CLOT_DIR + "cmd.book.db.json"

    try:
        file = open(file_, "r")
        content = json.loads(file.read())
        file.close()

        file = open(file_, "w")
        del content[cmd]
        file.write(json.dumps(content))
        file.close()

    except:
        pass


def add_command(cmd, value):
    file_ = CLOT_DIR + "cmd.book.db.json"

    try:
        file = open(file_, "r")
        content = json.loads(file.read())
        file.close()

        file = open(file_, "w")
        content[cmd] = value
        file.write(json.dumps(content))
        file.close()

    except:
        file = open(file_, "w")
        content = {}
        content[cmd] = value
        file.write(json.dumps(content))
        file.close()


def search_command(keyword):
    global COLOR

    content = get_command_book(p=False)

    c = 0

    for e in content:
        if keyword in e or keyword in content[e]:

            e_ = e

            e = e.split(keyword)

            c = 0
            for x in e:



                if  COLOR == False:
                    for char in x:
                        print(colored(char), end="")

                else:

                    if type(COLOR) == str:
                        COLOR = make_list(COLOR)

                    print(fg(COLOR[0], COLOR[1], COLOR[2]) + x + fg.rs, end="")

                if c != len(e) - 1:

                    print("\033[1;4m" + keyword + "\033[0m", end="")

                c += 1

            e = content[e_]
            e = e.split(keyword)

            print("  --->  ", end = "")

            c = 0

            for x in e:

                if  COLOR == False:
                    for char in x:
                        print(colored(char), end="")
                else:
                    if type(COLOR) == str:
                        COLOR = make_list(COLOR)

                    print(fg(COLOR[0], COLOR[1], COLOR[2]) + x + fg.rs, end="")

                if c != len(e) - 1:
                    print("\033[1;4m" + keyword + "\033[0m", end="") 

                c +=  1
            print("")
            c = 0

            
def is_root_linux():
    return os.geteuid() == 0

OS = platform.system()

def clear():
    if OS == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    
def update(v):
    os.system("pip3 uninstall clot-terminal")
    os.system(f"pip3 install clot-terminal=={v}")
    clear()


    
def main():
    global COLOR, CLOT_DIR, VERSION

    VERSION = "0.0.1"

    clear()

    std_out = ""
    std_out_r = ""

    cmd = None

    atexit.register(exit_man)

    while True:
        if OS != "Windows":
            root = is_root_linux()
        else:
            root = False
        try:
            print(bg(142, 155, 250)+fg(230,230,230)+f"@{os.getcwd()} [Root:{root}]"+fg.rs+bg.rs, end = "")
            cmd = input(": ")

        except:
            pass

        if cmd.replace(" ","") != "":
            add_to_history(cmd)

        if cmd == "":
            continue

        if cmd == "clear":
            clear()
            continue

        if cmd == "exit":
            break

        if cmd == "help":
            help_ = """
    ===========================================================
       /$$$$$$  /$$             /$$    
      /$$__  $$| $$            | $$    
     | $$  \__/| $$  /$$$$$$  /$$$$$$  
     | $$      | $$ /$$__  $$|_  $$_/  
     | $$      | $$| $$  \ $$  | $$    
     | $$    $$| $$| $$  | $$  | $$ /$$
     |  $$$$$$/| $$|  $$$$$$/  |  $$$$/
      \______/ |__/ \______/    \___/  

                                         - Cactochan


                    >>>Internal Commands<<<

        \thelp - Shows this
        \tupdate - Updates the terminal if any update found
        \texit - Exit

        \tcolor <mix or rgb_color_code> - Fg color of terminal

        \thistory - Shows the command history

        \tcommand_book -  Shows the command book
        \tadd_cmd <cmd> <note> - Adds to command book
        \tremove_cmd <cmd> - Remove a command
        \tsearch_cmd <keyword>

                    >>>Other Info<<<

        \tHistory is stored in the file named
             ".history_terminal_s"
        \tThe file ".<<std:out>>" is used as standart output
        \tCommand Book is stored in "cmd.book.db.json"
        \tConfigs in ".conf"

    Github : <github.com/merwin-asm/Clot>
    ===========================================================
        """

            for line in help_.split("\n"):

                for char in line:
                    char = char.replace("\n", "")
                    print(colored(char), end="")

                print("")

            continue
        if cmd == "update":
            version_ = requests.get("https://raw.githubusercontent.com/merwin-asm/Clot/main/current.ver").text
            version_ = version_.replace("\n", "")
            
            if version_ != VERSION:
                update(version_)
            continue

        if cmd == "history":
            cur = open(CLOT_DIR+".history_terminal_s", "r").readlines()
            for e in cur:
                for char in e:
                    if char != "\n":
                        print(char, end="")
                print("")
            continue

        try:
            if cmd.split(" ")[0] == "color":
                if cmd.split(" ")[1] == "mix":
                    try:
                        f = open(CLOT_DIR + ".conf", "w")
                        f.write("")
                        f.close()
                        COLOR = False
                    except:
                        COLOR = False
                else:
                    try:
                        f = open(CLOT_DIR + ".conf" , "w")
                        f.write(cmd.split(" ")[1])
                        f.close()
                        COLOR = cmd.split(" ")[1]
                    except:
                        f = open(CLOT_DIR + ".conf" , "x")
                        f.write(cmd.split(" ")[1])
                        f.close()
                        COLOR = cmd.split(" ")[1]
                continue
        except:
            continue

        if cmd == "command_book":
            get_command_book()
            continue

        cmd = cmd.split(" ")

        try:
            if cmd[0] == "add_command":
                val = ""
                for e in cmd[2:]:
                    val += e + " "
                add_command(cmd[1], val)
                continue
        except:
            print("Error : Args not passed")
            continue

        try:
            if cmd[0] == "remove_command":
                remove_command(cmd[1])
                continue
        except:
            print("Error : Args not passed")
            continue

        try:
            if cmd[0] == "search_command":
                search_command(cmd[1])
                continue
        except:
            print("Error : Args not passed")
            continue

        std_out = open(CLOT_DIR+".<<std:out>>", "a")

        try:
            subprocess.call(cmd, stdout=std_out)
        except:
            print("Error : Cmd / File not found")
            continue

        std_out.close()

        std_out_r = open(CLOT_DIR+".<<std:out>>", "r")


        for line in std_out_r.readlines():
            if  COLOR == False:
                for char in line:
                    char = char.replace("\n", "")
                    print(colored(char), end="")
                print("")
            else:
                if type(COLOR) == str:
                    COLOR = make_list(COLOR)

                print(fg(COLOR[0], COLOR[1], COLOR[2]) +line+ fg.rs)

        std_out_r.close()

        os.remove(CLOT_DIR+".<<std:out>>")
        
if __name__ == "__main__":
    main()
