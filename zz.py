#######################################
#             zzCrack                  
#         made by robi0t              
#    https://github.com/robi0t        
#                                     
#             LICENSE:
#           MIT License
#######################################
#If you experience any error please let me know
#version 2.4
from typing import Iterable

from colorama import Fore,Back,Style,init
from itertools import chain,product,islice
from optparse import OptionParser
from zipfile import ZipFile
from pyzipper import AESZipFile
from multiprocessing import Process, Pool, Event, Manager
import string
import signal
import time
import sys
import os

banner='''
▒███████▒▒███████▒ ▄████▄   ██▀███   ▄▄▄       ▄████▄   ██ ▄█▀
▒ ▒ ▒ ▄▀░▒ ▒ ▒ ▄▀░▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ 
░ ▒ ▄▀▒░ ░ ▒ ▄▀▒░ ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ 
  ▄▀▒   ░  ▄▀▒   ░▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ 
▒███████▒▒███████▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄
░▒▒ ▓░▒░▒░▒▒ ▓░▒░▒░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒
░░▒ ▒ ░ ▒░░▒ ▒ ░ ▒  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░
░ ░ ░ ░ ░░ ░ ░ ░ ░░          ░░   ░   ░   ▒   ░        ░ ░░ ░ 
  ░ ░      ░ ░    ░ ░         ░           ░  ░░ ░      ░  ░   
░        ░        ░                           ░               '''


class zzCrack():
    passFound_print = lambda tries, word, start_time: (
        f"{Style.RESET_ALL}Password was found after {Fore.LIGHTCYAN_EX + str(tries)} {Style.RESET_ALL}tries.\n"
        f"The password is: {Fore.LIGHTGREEN_EX + word}{Style.RESET_ALL}\n"
        f"Time taken: {Style.BRIGHT + Fore.RED + zzCrack.format_time(start_time)}")
    passNotFound_print = lambda tries, start_time: (
        f"{Style.RESET_ALL}Do not find valid password after {Fore.LIGHTCYAN_EX + str(tries) + Style.RESET_ALL} tries.\n"
        f"Time taken: {Style.BRIGHT + Fore.RED + zzCrack.format_time(start_time)}"
    )
    tries_print = lambda tries, word: f"Tries: {tries} > {word}"
    def __init__(self):
        self.saves_dir = os.path.dirname(os.path.abspath(__file__))+"/stateSaves"
        self.passFound = False
        self.done = False
        self.zip_func = ZipFile
    
    def signal_handler(self, signal, frame):
        self.done = True

    @staticmethod
    def format_time(start_time):
        elapsed_time = time.time() - start_time
        days = int(elapsed_time // (24 * 3600))
        elapsed_time %= (24 * 3600)
        hours = int(elapsed_time // 3600)
        elapsed_time %= 3600
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_string = ""
        if days:
            time_string += f"{days}d "
        if hours:
            time_string += f"{hours}h "
        if minutes:
            time_string += f"{minutes}m "
        time_string += f"{seconds}s"
        return time_string


    #############
    # Wordlist
    #############
    def wlist_crack(self, tries, wordlist, z, stream, archive_dir, wordlist_inp):
        content = z.namelist()
        start_time = time.time()
        for word in wordlist:
            try:
                if self.done:
                    confirm = input("\nAre you sure you want to stop (y/n) > ").lower()
                    if confirm == "y": self.save_state(archive_dir, wordlist_inp, word, stream, wordlist); return
                    self.done = False

                tries += 1
                if stream: print(zzCrack.tries_print(tries,word))
                z.setpassword(word.encode('utf8', errors='ignore'))
                z.read(content[0])
                self.passFound = True
                print(zzCrack.passFound_print(tries,word,start_time))
                return word
            except Exception as ex:
                pass

    def wlist_crack_entry(self, archive_dir, wordlist_inp, showoutput_b, resume_index):
        tries = 0
        try:
            try: _archive = self.zip_func(archive_dir, "r")
            except Exception as ex: print(ex); sys.exit(1)

            print("Loading Wordlist, Please wait")
            _wordlist = open(wordlist_inp, 'r', encoding="utf8", errors='ignore')
            wordlist = _wordlist.read().splitlines()
            _wordlist.close()
            if resume_index != None:
                wordlist = wordlist[resume_index-1:]
                tries = resume_index-1
            print("Generation complete, Trying Passwords")

            return self.wlist_crack(tries, wordlist, _archive, showoutput_b, archive_dir, wordlist_inp)
        except IOError:
            print("Archive Or Wordlist Doesn't Exist")
            sys.exit(1)


    #############
    # Bruteforce
    #############
    def generate_charlist(self, charset):
        chars = [
            string.ascii_lowercase,     # 0
            string.ascii_uppercase,     # 1
            string.digits,              # 2
            string.punctuation,         # 3
            string.printable            # 4
        ]

        allowed_chars = set("01234+")
        charlist = ''.join(''.join([chars[int(c)] for c in charset.split('+') if c in allowed_chars]))
        if charlist == "": print("Invalid charset"); sys.exit(1)
        return charlist

    def memsafe_generate_bruteforce_list(self, charset, max_length):
        charlist = self.generate_charlist(charset)
        return (''.join(candidate)
            for candidate in chain.from_iterable(product(charlist, repeat=i)
            for i in range(1, max_length + 1)))

    def bruteforce_crack_sp(self, zip_dir, zip_func, stream, charset, max_length):
        tries = 0
        zip_file = zip_func(zip_dir, "r")
        content = zip_file.namelist()
        start_time = time.time()
        for word in self.memsafe_generate_bruteforce_list(charset, max_length):
            try:
                if self.done == True:
                    confirm = input("\nAre you sure you want to stop (y/n) > ").lower()
                    if confirm == "y": return
                    self.done = False

                tries += 1
                if stream: print(zzCrack.tries_print(tries,word))
                zip_file.setpassword(word.encode('utf8', errors='ignore'))
                zip_file.read(content[0])
                self.passFound = True
                print(zzCrack.passFound_print(tries,word,start_time))
                return word
            except Exception as ex:
                pass
        print(zzCrack.passNotFound_print(tries,start_time))

    # Batched giant generator into small pieces
    @staticmethod
    def batched_generator(gen:Iterable, batch_size):
        while True:
            batch = list(islice(gen, batch_size))  # Take out batch_size elements each time
            if not batch:
                break
            yield batch  # yield this batch

    @staticmethod
    def bf_crack_unit(gen, zip_dir, zip_func, stream, stop_event, tries):
        zip_file = zip_func(zip_dir, "r")
        content = zip_file.namelist()
        for word in gen:
            # Profile shows this check would cause performance degradation due to synchronization overhead.
                # Exits early if other processes have already succeeded.
                # if stop_event.is_set():
                #     return None
            try:
                tries += 1
                if stream: print(zzCrack.tries_print(tries,word))
                zip_file.setpassword(word.encode('utf8', errors='ignore'))
                zip_file.read(content[0])
                stop_event.set()
                return word
            except Exception as ex:
                pass
        return None

    def bruteforce_crack_mp(self, zip_dir, zip_func, stream, charset, max_length, pool_size = 4):
        max_active_tasks = pool_size * 2  # Limit the max active tasks as twice the size of pool to prevent excessive memory usage
        batch_size = 1000
        start_time = time.time()
        pass_generator = self.memsafe_generate_bruteforce_list(charset, max_length)
        sub_generators = self.batched_generator(pass_generator, batch_size)
        stop_event = Manager().Event()
        result = None
        with Pool(processes = pool_size) as pool:
            active_tasks = []
            task_id = 0
            try:
                # Dynamical async apply tasks
                for sub_gen in sub_generators:
                    if stop_event.is_set():
                        break
                    if stream:
                        print(f"Apply task: {task_id}")
                    task = pool.apply_async(self.bf_crack_unit,
                                            args=(sub_gen, zip_dir, zip_func, stream, stop_event, task_id * batch_size + 1))
                    task_id += 1
                    active_tasks.append(task)

                    # Follow the max_active_tasks limit
                    while len(active_tasks) >= max_active_tasks:
                        # Reverse traversal and remove finished task
                        for i in range(len(active_tasks) - 1, -1, -1):
                            task = active_tasks[i]
                            if task.ready():
                                active_tasks.pop(i)
                                if task.get() is not None:
                                    # Trigger stop event, if task finished and find the password
                                    stop_event.set()
                                    result = task.get()

                        # Block a short period to avoid excessive cycling
                        time.sleep(0.01)

                # Wait all tasks finished
                for task in active_tasks:
                    task.wait()
                    if task.get() is not None:
                        break

            except KeyboardInterrupt:
                print("Terminating due to user interruption.")
            finally:
                pool.terminate()
                pool.join()

        # extract result
        while result is None and len(active_tasks) > 0:
            if active_tasks[0].get() is not None:
                stop_event.set()
                result = active_tasks[0].get()
            active_tasks.remove(active_tasks[0])

        if result is not None:
            print(zzCrack.passFound_print(task_id * batch_size, result, start_time))
        else:
            print(zzCrack.passNotFound_print(task_id * batch_size, start_time))
        return result


    def bruteforce_crack_entry(self, archive_dir, charset, max_letters, showoutput_b, resume_index):
        try:
            try: _archive = self.zip_func(archive_dir, "r")
            except Exception as ex: print(ex); sys.exit(1)
            print("Started...")
            if options.process_num is not None and int(options.process_num) > 1:
                self.bruteforce_crack_mp(archive_dir, self.zip_func, showoutput_b, charset, max_letters, int(options.process_num))
            else:
                self.bruteforce_crack_sp(archive_dir, self.zip_func, showoutput_b, charset, max_letters)
        except IOError:
            print("zip_file Doesn't Exist")
            sys.exit(1)

    ######################
    # Restore/Save state
    ######################
    def save_state(self, archive_dir, wordlist_inp, current_word, showoutput_b, generated_list):
        while True:
            saveState = input("\nDo you want to save the Current State and continue from here later? [--restore]  (y/n) > ").lower()
            if saveState == "y":
                try:
                    print("[+] Saving Current State")
                    if not os.path.exists(self.saves_dir): os.makedirs(self.saves_dir)
                    
                    name = f"{self.saves_dir}/{time.strftime('%b-%d-%Y-%H-%M-%S')}-wordlist.txt"
                    f = open(name,"w")
                    f.write(f"{os.path.abspath(archive_dir)},{os.path.abspath(wordlist_inp)},{int(showoutput_b)},{generated_list.index(current_word)}")
                    f.close()
                    print(f"[finished] {name}")
                    break
                except IOError as ex:
                    print(f"Error when saving file: {ex}")
                except Exception as ex:
                    print(f"Unexpected error: {ex}")
            elif saveState == "n":
                break
                    

    def restore(self):
        try:
            savefiles = [f for f in os.listdir("./stateSaves") if os.path.isfile(os.path.join("./stateSaves", f))]
            restoreNbr = int(options.restore)
            print(savefiles[restoreNbr])
            f = open(f"./stateSaves/{savefiles[restoreNbr]}")
            resfile = f.read().split(',')
            f.close()

            self.wlist_crack_entry(resfile[0], resfile[1], bool(int(resfile[2])), int(resfile[3]))
        except FileNotFoundError:
            print("No restore files found")
        except IndexError as ex:
            print(f"Restore file index given is not valid or the restorefile is broken {ex}")
        except Exception as ex:
            print(f"Unexpected error: {ex}")

    #################
    # No args / Args
    #################
    def _noargs(self):
        print(Fore.CYAN + banner)
        print("\nhttps://github.com/robi0t\n"+Style.RESET_ALL)
        archive_dir = input('\nEnter a directory/name to a .zip file > ')
        attack_type = input('Which attack type would you like to run\n0: Bruteforce\t 1: Wordlist > ')

        if attack_type == "1":
            wordlist_inp = input("[+] Enter a directory/name to a password list > ")
            showOutPut = input("\nDo you want to output everything (slower) or not (faster)  y/n > ")
            if showOutPut.lower() == "y":
                showoutput_b = True
            else:
                showoutput_b = False
            self.wlist_crack_entry(archive_dir, wordlist_inp, showoutput_b, None)

        elif attack_type == "0":
            charset = input('\n[+] Which characters to use in the attack (combine to use multiple, separated by +)\n 0: Only small letters\n 1: Only big letters\n 2: Only numbers\n 3: Only symbols\n 4: Everything\n> ')
            try:
                max_letters = int(input("\n[-+] Max length > "))
                if max_letters < 0:
                    print("The given number is not a valid Positive number")
                    sys.exit(1)
            except:
                print("The input given is not a valid Integer")
                sys.exit(1)
            showOutPut = input("\nDo you want to output everything (slower) or not (faster)  y/n > ")
            if showOutPut.lower() == "y": showoutput_b = True
            else: showoutput_b = False
            self.bruteforce_crack_entry(archive_dir, charset, max_letters, showoutput_b, None)
        else:
            print("Invalid Input")
        sys.exit(1)

    def _args(self):
        if options.archive == None and options.reslist == False and options.restore == None:
            print("No zip_file Given")
            sys.exit(1)

        if options.use_pyzipper:
            self.zip_func = AESZipFile

        archive_dir = options.archive
            
        if options.wordlist != None:
            wordlist_inp = options.wordlist
            showoutput_b = options.showoutput
            
            self.wlist_crack_entry(archive_dir, wordlist_inp, showoutput_b, None)

        elif options.bruteforce == True:
            charset = options.charlist
            if charset == None:
                print("No Charlist Given")
                sys.exit(1)

            max_letters_inp = options.maxlength
            if max_letters_inp == None:
                print("No MaxLength Given")
            try:
                max_letters = int(max_letters_inp)
                if max_letters < 0:
                    print("The given MaxLength is not a valid Positive number")
                    sys.exit(1)
            except:
                print("The given MaxLength is not a valid Integer")
                sys.exit(1)

            showoutput_b = options.showoutput
            self.bruteforce_crack_entry(archive_dir, charset, max_letters, showoutput_b, None)

        elif options.restore != None:
            self.restore()
        
        elif options.reslist == True:
            try:savefiles = [f for f in os.listdir("./stateSaves") if os.path.isfile(os.path.join("./stateSaves", f))]
            except: print("No savefiles found"); sys.exit(1)
            print('\n'.join(f"{savefiles.index(saves)} > {savefiles[savefiles.index(saves)]}" for saves in savefiles))
            print("\n\nusage:[-r (file index)] [--restore (file index)]")
            
        else:
            print("No Cracking Method Given")
        sys.exit(1)


    #################
    # Main
    #################
    def main(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        if len(sys.argv[1:]) == 0:
            self._noargs()
        else:
            self._args()
        print(Style.RESET_ALL)
    
        if not self.passFound:
            print("Couldn't Crack The Password With The Current Options")
        

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", dest="archive", metavar=" ",
                    help="Archive To Crack")
    parser.add_option("-w", dest="wordlist",
                    help="Enter the name Or directory to the wordlist for a wordlist attack", metavar=" ")
    parser.add_option("-b",
                    action="store_true", dest="bruteforce", default=False,
                    help="Attack method to bruteforce the zip_file password")              
    parser.add_option("-c", dest="charlist",
                    help="(Required for Bruteforce)\nWhich characters to use in the Bruteforce attack (combine to use multiple, separated by +) 0: Only small letters | 1: Only big letters | 2: Only numbers | 3: Only signs | 4: Everything", metavar=" ") #byt
    parser.add_option("-l", dest="maxlength",
                    help="The max length for the bruteforce passwords (Required for Bruteforce)", metavar=" ")
    parser.add_option("-s", "--stream",
                    action="store_true", dest="showoutput", default=False,
                    help="Stream tried passwords (slower)")
    parser.add_option("-r", "--restore", dest="restore",
                    help="Restore state From save (do --rl for a list of valid options)", metavar=" ")
    parser.add_option("--rl",
                    action="store_true", dest="reslist", default=False,
                    help="Shows a list of all restore files found")
    parser.add_option("--aes", "--use-pyzipper", action="store_true", dest="use_pyzipper", default=False,
                    help="Use pyzipper lib to deal with AES encrypted zip file")
    parser.add_option("-p", dest = "process_num", default = 1, metavar="NUMBER",
                    help="Set the number of processes used in crack password (Limited for Bruteforce)")
    (options, args) = parser.parse_args()

    init()
    zzCrack().main()