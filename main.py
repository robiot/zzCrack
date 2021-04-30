#######################################
#             zzCrack                  
#         made by robi0t              
#    https://github.com/robi0t        
#                                     
#             LICENSE:
#	GNU General Public License v3.0
#######################################
#If tou experience any error please let me know


from optparse import OptionParser
import zipfile
import os
import sys
import signal
import time


def wordlist_crack(zip_dir, worlist_inp, showoutput_b, resume_index):
    global passFound
    global ignoreStatus
    try:
        z = zipfile.ZipFile(zip_dir)
        print("Loading Wordlist, Please wait")
        try:
            wordlist = open(worlist_inp, 'r', encoding="utf8").read()
            wordlist = wordlist.splitlines()

            tries = 0
            if resume_index != None:
                wordlist = wordlist[resume_index-1:]
                tries = resume_index-1

            print("Generation complete, Trying Passwords")
            if showoutput_b == True:
                for word in wordlist:
                    try:
                        if done==True:
                            ignoreStatus = True
                            save_state("wordlist", zip_dir, worlist_inp, options.charlist, word ,showoutput_b, wordlist)
                            return
                        content = z.namelist()
                        tries += 1
                        print(f"Tries: {tries} >", word)
                        z.setpassword(word.encode('ascii'))
                        z.extract(content[0])
                        os.remove(content[0])
                        passFound = True
                        print(color.RESET + "Password was found after", color.CYAN + f"{tries}", color.RESET + " tries. The password is:", color.GREEN + f"{word}")
                        break
                    except:
                        pass
            elif showoutput_b == False:
                for word in wordlist:
                    try:
                        if done==True:
                            ignoreStatus = True
                            save_state("wordlist", zip_dir, worlist_inp, options.charlist, word ,showoutput_b, wordlist)
                            return
                        content = z.namelist()
                        tries += 1
                        z.setpassword(word.encode('ascii'))
                        z.extract(content[0])
                        os.remove(content[0])
                        passFound = True
                        print(color.RESET + "Password was found after", color.CYAN + f"{tries}", color.RESET + " tries. The password is:", color.GREEN + f"{word}")
                        break
                    except:
                        pass
        except IOError:
            print(color.RED+"\n[--]"+ color.RESET + "The given password list is not a vaild text-file or doesent exist")
            sys.exit()
    except IOError:
        print(color.RED+"\n[--]"+ color.RESET + "Zipfile Doesent Exist")
        sys.exit()

def generate_charlist(charset):
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
    return charlist


def bruteforce(zip_dir, charset, max_letters, showoutput_b, resume_index):
    complete = []
    global passFound
    global ignoreStatus
    

    print("Generating list, Please wait")
    try:
        z = zipfile.ZipFile(zip_dir)
        charlist = generate_charlist(charset)
        for current in range(max_letters):
            a = [i for i in charlist]
            for x in range(current):
                a = [y + i for i in charlist for y in a]
            complete = complete + a

        tries = 0
        if resume_index != None:
            complete = complete[resume_index-1:]
            tries = resume_index-1

        print("Generation complete, Trying Passwords")
        if showoutput_b == True:
            for password in complete:
                try:
                    if done==True:
                        ignoreStatus = True
                        save_state("bruteforce", zip_dir, charset, max_letters, password ,showoutput_b, complete)
                        return
                    content = z.namelist()
                    tries += 1
                    print(f"Tries: {tries} >", password)
                    z.setpassword(password.encode('ascii'))
                    z.extract(content[0])
                    os.remove(content[0])                        
                    passFound = True
                    print(color.RESET + "Password was found after", color.CYAN + f"{tries}", color.RESET + " tries. The password is:", color.GREEN + f"{password}")
                    break
                except:
                    pass
        elif showoutput_b == False:
            for password in complete:
                try:
                    if done==True:
                        ignoreStatus = True
                        save_state("bruteforce", zip_dir, charset, max_letters, password ,showoutput_b, complete)
                        return
                    content = z.namelist()
                    tries += 1
                    z.setpassword(password.encode('ascii'))
                    z.extract(content[0])
                    os.remove(content[0])
                    passFound = True
                    print(color.RESET + "Password was found after", color.CYAN + f"{tries}", color.RESET + " tries. The password is:", color.GREEN + f"{password}")
                    break
                except:
                    pass
        else:
            print("yes")
    except IOError:
        print(color.RED+"\n[--]"+ color.RESET + "Zipfile Doesent Exist")
        sys.exit()
    

def _noargs():
    print(bannerAscii)
    print("\nhttps://github.com/robi0t\n")
    zip_dir = input(color.RESET +'\nEnter a directory/name to a .zip file > ')
    attack_type = input('Which attack type would you like to run\n0: Bruteforce\t 1: Wordlist > ')

    if attack_type == "1":
        worlist_inp = input("[+] Enter a directory/name to a password list > ")
        showOutPut = input("\nDo you want to output everything (slower) or not (faster)  y/n > ")
        if showOutPut.lower() == "y":
            showoutput_b = True
        else:
            showoutput_b = False
        wordlist_crack(zip_dir,worlist_inp, showoutput_b, None)

    elif attack_type == "0":
        charset = input('\n[+] Which characters to use in the attack (combine to use multiple, separated by +)\n 0: Only small letters\n 1: Only big letters\n 2: Only numbers\n 3: Only signs\n 4: Everything\n> ')
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
        bruteforce(zip_dir, charset, max_letters, showoutput_b, None)
    else:
        print("Invalid Input")
        
    if passFound == False and ignoreStatus == False:
        print(color.RED+"\n[--]", color.RESET + "Couldnt Crack The Password With The Current Options")
        try:
            os.remove(content[0])
        except:
            pass

def _args():
    if options.zipfile == None and options.reslist == False and options.restore == None:
        print("No Zipfile Given")
        return
    zip_dir = options.zipfile
        
    if options.wordlist != None:
        worlist_inp = options.wordlist
        if options.showoutput == True:
            showoutput_b = True
        else:
            showoutput_b = False
        wordlist_crack(zip_dir,worlist_inp, showoutput_b, None)

    elif options.bruteforce == True:
        charset = options.charlist
        if charset == None:
            print("No Charlist Given")
            return
        max_letters_inp = options.maxlenght
        if max_letters_inp == None:
            print("No MaxLenght Given")
            return
        try:
            max_letters = int(max_letters_inp)
            if max_letters < 0:
                print("The given MaxLenght is not a vaild Positive number")
                return
        except:
            print("The given MaxLenght is not a vaild Integer number")
            return

        if options.showoutput == True:
            showoutput_b = True
        else:
            showoutput_b = False
        bruteforce(zip_dir, charset, max_letters, showoutput_b, None)

    elif options.restore != None:
        restore()
        return
    elif options.reslist == True:
        savefiles = [f for f in os.listdir("./stateSaves") if os.path.isfile(os.path.join("./stateSaves", f))]
        for saves in savefiles:
           print(f"{savefiles.index(saves)} > {savefiles[savefiles.index(saves)]}")
        print("\n\n usage:[-r (file index)] [--restore (file index)]")
        return
    else:
        print("No Cracking Type Given")
        return
    if passFound == False and ignoreStatus == False:
        print(color.RED+"\n[--]", color.RESET + "Couldnt Crack The Password With The Current Options")
        try:
            os.remove(content[0])
        except:
            pass

def save_state(_type, zip_dir, worlist_inp, max_lenght, current_word, showoutput_b, generated_list):
    while True:
        saveState = input("\nDo you want to save the Current State and continue from here later? [--restore]  (y/n) > ").lower()
        if saveState == "y":
            print("[+] Saving Current State")
            if not os.path.exists('stateSaves'):
                os.makedirs('stateSaves')
            if _type == "wordlist":
                name = f"./stateSaves/{time.strftime('%b-%d-%Y-%H-%M-%S')}-wordlist.txt"
                f = open(name,"w+")
                f.write(f"{_type}\n{worlist_inp}\nnone\n{generated_list.index(current_word)}\n{showoutput_b}\n{zip_dir}")
                f.close()
                print(f"[finished] {name}")
                return
            elif _type == "bruteforce":
                name= f"./stateSaves/{time.strftime('%b-%d-%Y-%H-%M-%S')}-bruteforce.txt"
                f = open(name,"w+")
                f.write(f"{_type}\n{worlist_inp}\n{max_lenght}\n{generated_list.index(current_word)}\n{showoutput_b}\n{zip_dir}")
                f.close()
                print(f"[finished] {name}")
                return
            else:
                print("Unexpected Error")
        elif saveState == "n": 
            return

def restore():
    savefiles = [f for f in os.listdir("./stateSaves") if os.path.isfile(os.path.join("./stateSaves", f))]

    try:
        restoreNbr = int(options.restore)
        print(savefiles[restoreNbr])
        f = open(f"./stateSaves/{savefiles[restoreNbr]}")
        resfile = f.read().split('\n')

        if resfile[4] == "True":
            showoutput = True
        else:
            showoutput = False
        resfile[3] = int(resfile[3])
        if resfile[0] == "bruteforce":
            bruteforce(resfile[5], resfile[1], int(resfile[2]), showoutput, resfile[3])
        elif resfile[0] == "wordlist":
            wordlist_crack(resfile[5], resfile[1], showoutput, resfile[3])
            
    except Exception as ex:
        print("Restore file index given is broken or not valid")
        print(ex)
        return
        

if __name__ == "__main__":
    passFound = False
    ignoreStatus = False
    done = False
    def signal_handler(signal, frame):
        global done
        done=True
    signal.signal(signal.SIGINT, signal_handler)

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
        RESET = '\033[0m'

    bannerAscii = color.CYAN + r'''
  _______        _____                _    
 |___  (_)      / ____|              | |   
    / / _ _ __ | |     _ __ __ _  ___| | __
   / / | | '_ \| |    | '__/ _` |/ __| |/ /
  / /__| | |_) | |____| | | (_| | (__|   < 
 /_____|_| .__/ \_____|_|  \__,_|\___|_|\_|
         | |                               
         |_|                                 ''' 

    parser = OptionParser()
    parser.add_option("-z", dest="zipfile", metavar=" ",
                    help="Zipfile To Crack (Required)")
    parser.add_option("-w", dest="wordlist",
                    help="Enter The Name Or Directory To The Wordlist For A Wordlist Attack", metavar=" ")
    parser.add_option("-b",
                    action="store_true", dest="bruteforce", default=False,
                    help="Attack Method To Bruteforce The Zipfile Password")              
    parser.add_option("-c", dest="charlist",
                    help="(Required for Bruteforce)\nWhich characters to use in the Bruteforce attack (combine to use multiple, separated by +)\t\t\t\t\t 0: Only small letters\t\t\t\t\t 1: Only big letters\t\t\t\t\t 2: Only numbers\t\t\t\t\t 3: Only signs\t\t\t\t\t\t 4: Everything", metavar=" ") #byt
    parser.add_option("-m", dest="maxlenght",
                    help="The Max Lenght For The Bruteforce Passwords (Required for Bruteforce)", metavar=" ") #byt
    parser.add_option("-s", "--stream",
                    action="store_true", dest="showoutput", default=False,
                    help="Stream Tried Passwords (slower)")
    #restore
    parser.add_option("-r", "--restore", dest="restore",
                    help="Restore State From Save (do --rl for a list of vaild options)", metavar=" ") #byt
    parser.add_option("--rl",
                    action="store_true", dest="reslist", default=False,
                    help="Shows a list of all restore files found")
    (options, args) = parser.parse_args()


    os.system('title [zzCrack]')
    if len(sys.argv[1:]) == 0:
        _noargs()
    else:
        _args()
    print(color.RESET)
