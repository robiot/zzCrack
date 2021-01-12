import zipfile
import os
import sys
import threading

from colorama import init
init()
from colorama import Fore, Back, Style

charlist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
complete = []
max_letters = 4

in_menu = True
do_bruteforce = True
passFound = False

class color:
    DarkGray = "\x1b[90m"
    LightGray = "\x1b[37m"
    White = "\x1b[97m"
    Default = "\x1b[39m"
    PURPLE = '\033[1;35;48m'
    CYAN = '\033[1;36;48m'
    BOLD = '\033[1;37;48m'
    BLUE = '\033[1;34;48m'
    GREEN = '\033[1;32;48m'
    YELLOW = '\033[1;33;48m'
    RED = '\033[1;31;48m'
    BLACK = '\033[1;30;48m'
    UNDERLINE = '\033[4;37;48m'
    END = '\033[1;37;0m'
    HEADER = '\033[95m'

bannerAscii = Fore.LIGHTCYAN_EX + r'''
  _______        _____                _    
 |___  (_)      / ____|              | |   
    / / _ _ __ | |     _ __ __ _  ___| | __
   / / | | '_ \| |    | '__/ _` |/ __| |/ /
  / /__| | |_) | |____| | | (_| | (__|   < 
 /_____|_| .__/ \_____|_|  \__,_|\___|_|\_|
         | |                               
         |_|                                 '''

if in_menu == True:
    print(bannerAscii)
    print(color.White + ' ')
    zip_dir = input('[+] Enter a directory/name to a .zip file > ')
    attack_type = input('Which Attack Type Would You Like To Run\n0: Bruteforce\t 1: Wordlist > ')
    if attack_type == "1":
        worlist_inp = input("[+] Enter a directory/name to a password list > ")
        showOutPut = input("\nDo you want to output everything (slower) or not (faster)  y/n > ")
        if showOutPut.lower() == "y":
            showoutput_b = True
        else:
            showoutput_b = False
        try:
            z = zipfile.ZipFile(zip_dir)
            try:
                wordlist = open(worlist_inp, 'r').read()
                wordlist = wordlist.splitlines()
                tries = 0

                if showoutput_b == True:
                    for word in wordlist:
                        try:
                            content = z.namelist()
                            tries += 1
                            print(f"Tries: {tries} >", word)
                            z.setpassword(word.encode('ascii'))
                            z.extract(content[0])
                            os.remove(content[0])
                            passFound = True
                            print(Style.RESET_ALL + "Password was found after", Fore.CYAN + f"{tries}", Style.RESET_ALL + " tries. The password is:", Fore.GREEN + f"{word}")
                            break
                        except:
                            pass
                elif showoutput_b == False:
                    for word in wordlist:
                        try:
                            content = z.namelist()
                            tries += 1
                            z.setpassword(word.encode('ascii'))
                            z.extract(content[0])
                            os.remove(content[0])
                            passFound = True
                            print(Style.RESET_ALL + "Password was found after", Fore.CYAN + f"{tries}", Style.RESET_ALL + " tries. The password is:", Fore.GREEN + f"{word}")
                            break
                        except:
                            pass
            except IOError:
                print(Fore.RED+"\n[--]"+ Style.RESET_ALL + "The given password list is not a vaild text-file or doesent exist")
        except IOError:
            print(Fore.RED+"\n[--]"+ Style.RESET_ALL + "Zipfile Doesent Exist")
    else:
        charset = input('\n[+] Which characters to use in the attack (combine to use multiple, separated by +)\n 0: Only small letters\n 1: Only big letters\n 2: Only numbers\n 3: Only signs\n 4: Everything\n> ')
        #0
        if charset == "0":
            charlist = 'abcdefghijklmnopqrstuvwxyz'
        elif charset == "1":
            charlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif charset == "2":
            charlist = "0123456789"
        elif charset == "3":
            charlist = r'~`!@#£€$¢¥§%°^&*()-_+={}[]|\/:;"<>,.?'+"'"
        elif charset == "4":
            charlist = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#£€$¢¥§%°^&*()-_+={}[]|\/:;"<>,.?'+"'"
        elif charset == "0+1":
            charlist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif charset == "0+2":
            charlist = 'abcdefghijklmnopqrstuvwxyz1234567890'
        elif charset == "0+3":
            charlist = r'abcdefghijklmnopqrstuvwxyz~`!@#£€$¢¥§%°^&*()-_+={}[]|\/:;"<>,.?'+"'"
        elif charset == "0+1+2":
            charlist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        elif charset == "0+1+3":
            charlist = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~`!@#£€$¢¥§%°^&*()-_+={}[]|\/:;"<>,.?'+"'"
        elif charset == "0+1+2+3":
            charlist = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#£€$¢¥§%°^&*()-_+={}[]|\/:;"<>,.?'+"'"
        elif charset == "1+2":
            charlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        elif charset == "1+3":
            charlist = r'ABCDEFGHIJKLMNOPQRSTUVWXYZ~`!@#£€$¢¥§%°^&*()-_+={}[]|\/:;"<>,.?'+"'"
        elif charset == "1+2+3":
            charlist = r'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#£€$¢¥§%°^&*()-_+={}[]|\/:;"<>,.?'+"'"
        elif charset == "2+3":
            charlist = r'1234567890~`!@#£€$¢¥§%°^&*()-_+={}[]|\/:;"<>,.?'+"'"
        else:
            print("Not an available option. Make sure to have them in order and separated by a +")
            sys.exit()
        max_letters_inp = input("\n[-+] Max length > ")
        try:
            max_letters = int(max_letters_inp)
            if max_letters < 0:
                print("The given number is not a vaild Positive number")
                sys.exit()
        except:
            print("The input given is not a vaild Integer number")
            sys.exit()
        showOutPut = input("\nDo you want to output everything (slower) or not (faster)  y/n > ")
        if showOutPut.lower() == "y":
            showoutput_b = True
        else:
            showoutput_b = False

        try:
            z = zipfile.ZipFile(zip_dir)

            for current in range(max_letters):
                a = [i for i in charlist]
                for x in range(current):
                    a = [y + i for i in charlist for y in a]
                complete = complete + a


            tries = 0

            if showoutput_b == True:
                for password in complete:
                    try:
                        content = z.namelist()
                        tries += 1
                        print(f"Tries: {tries} >", password)
                        z.setpassword(password.encode('ascii'))
                        z.extract(content[0])
                        os.remove(content[0])
                        passFound = True
                        print(Style.RESET_ALL + "Password was found after", Fore.CYAN + f"{tries}", Style.RESET_ALL + " tries. The password is:", Fore.GREEN + f"{password}")
                        break
                    except:
                        pass
            elif showoutput_b == False:
                for password in complete:
                    try:
                        content = z.namelist()
                        tries += 1
                        z.setpassword(password.encode('ascii'))
                        z.extract(content[0])
                        os.remove(content[0])
                        passFound = True
                        print(Style.RESET_ALL + "Password was found after", Fore.CYAN + f"{tries}", Style.RESET_ALL + " tries. The password is:", Fore.GREEN + f"{password}")
                        break
                    except:
                        pass
        except IOError:
            print(Fore.RED+"\n[--]"+ Style.RESET_ALL + "Zipfile Doesent Exist")

if passFound == False:
    print(Fore.RED+"\n[--]", Style.RESET_ALL + "Couldnt Crack The Password With The Current Options")
    try:
        os.remove(content[0])
    except:
        pass