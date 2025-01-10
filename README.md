# zzCrack v2
Ever forgot your password to a zipfile or you just want to crack the password for some reason, Then zzCrack is what you need

This is an advanced tool to crack passwords on zip-files by wordlists or bruteforce.

You can also save the current state in wordlist and return from it anytime

## Download:
You can download it as a zipfile or however you want
Then cd into the folder where zz.py is located and run
```
pip install -r requirements.txt
```

## Usage:
Run main.py with either arguments(more advanced) or without arguments(easy)

Argument Help: ```zz.py --help```

### Exampel Usage:
#### Without arguments:
```
▒███████▒▒███████▒ ▄████▄   ██▀███   ▄▄▄       ▄████▄   ██ ▄█▀
▒ ▒ ▒ ▄▀░▒ ▒ ▒ ▄▀░▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ 
░ ▒ ▄▀▒░ ░ ▒ ▄▀▒░ ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ 
  ▄▀▒   ░  ▄▀▒   ░▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ 
▒███████▒▒███████▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄
░▒▒ ▓░▒░▒░▒▒ ▓░▒░▒░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒
░░▒ ▒ ░ ▒░░▒ ▒ ░ ▒  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░
░ ░ ░ ░ ░░ ░ ░ ░ ░░          ░░   ░   ░   ▒   ░        ░ ░░ ░ 
  ░ ░      ░ ░    ░ ░         ░           ░  ░░ ░      ░  ░   
░        ░        ░                           ░               

https://github.com/robi0t


Enter a directory/name to a .zip file > test.zip
Which attack type would you like to run
0: Bruteforce    1: Wordlist > 0

[+] Which characters to use in the attack (combine to use multiple, separated by +)
 0: Only small letters
 1: Only big letters
 2: Only numbers
 3: Only signs
 4: Everything
> 0

[-+] Max length > 4

Do you want to output everything (slower) or not (faster)  y/n > y
```

#### With arguments:
```python zz.py -f test.zip -w rockyou.txt```

`--stream` will print everything it tries, but it makes the process slower

```python zz.py -f test.zip -b -c 0+2 -l 4 --stream```

```python zz.py --restore 0```

`-p` will set the number of processes used to crack the password

```python zz.py -f test.zip -b -c 0+2 -l 4 -p 16```


### If you experience any error please post an issue
