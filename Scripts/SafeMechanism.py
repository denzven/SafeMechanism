# SafeMechanism.py
"""
Welcome to SafeMechanism.py!
This is the algorithm of an "Temporary Safe" i had seen during my vacation.
I was so mesmerised by its genius design that i wanted to replicate it in python! so here it is!

How to Use:
Enter your 3-6 digit Pin.
Enter "#" at the end to close the safe.
To open the safe, enter your pin without the "#"
Thats it!
"""
import os
import time

# Clear Terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Variables to change stuff ezpz
LOCK_CHAR = "#"
CLOSED_MSG = "~Closed~"
ERROR_MSG_LOCK_CHAR = f"Error: add a {LOCK_CHAR} in the end to enter the passwd "
ENTER_PASS_MSG = "Please Enter your Passwd: "
ENTER_NEW_PASS_MSG = "Please set a Passwd: "
PASS_SET_MSG = "Your Passwd has been set sucessfully"
OPENED_MSG = "~Opened~"
WRNG_PASSWD = "Wrong Passwd try again"
CONTENT_CON = "Do you want to put anything inside your safe?(press s to skip, enter to input your content): "
CONTENT_INPUT = "Enter your content: "
ERROR_MSG_PASS_LEN = "Your Paswd is lesser than 3 char or greater than 6 char... please use a different Passwd"


def SafeMechanism(Passwd=None, Is_Passwd=False, Is_Locked=False, SafeContent=None):
    """
    This is the main looping function of the safe.
    """

    # Unlocked State
    if Is_Passwd is False and Is_Locked is False:
        Passwd_Input = input(ENTER_NEW_PASS_MSG)
        Passwd = Passwd_Input[:-1]

        # Length Check
        if len(Passwd) >= 3 and len(Passwd) <= 6:

            # End Char Check
            if Passwd_Input[-1] == LOCK_CHAR:
                Content_Con = input(CONTENT_CON)

                # Content Entry
                if Content_Con.lower() == "":
                    SafeContent = input(CONTENT_INPUT)
                if Content_Con.lower() == "s":
                    SafeContent = None

                print(PASS_SET_MSG)
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(CLOSED_MSG)
                time.sleep(2)

                SafeMechanism(Passwd=Passwd, Is_Passwd=True, Is_Locked=True, SafeContent=SafeContent)

            else:
                print(ERROR_MSG_LOCK_CHAR)
                SafeMechanism(Passwd=None, Is_Passwd=False, Is_Locked=False, SafeContent=None)

        else:
            print(ERROR_MSG_PASS_LEN)
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            SafeMechanism(Passwd=None, Is_Passwd=False, Is_Locked=False, SafeContent=None)

    # Locked State
    if Is_Passwd is True and Is_Locked is True:
        Passwd_Input = input(ENTER_PASS_MSG)

        # Passwd Check
        if Passwd_Input == Passwd:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(OPENED_MSG)
            
            # Content Check
            if SafeContent is not None:
                print(SafeContent)
        
            time.sleep(2)
            SafeMechanism(Passwd=None, Is_Passwd=False, Is_Locked=False, SafeContent=None)

        else:
            print(WRNG_PASSWD)
            SafeMechanism(Passwd=Passwd, Is_Passwd=True, Is_Locked=True)

    else:
        SafeMechanism(Passwd=Passwd, Is_Passwd=True, Is_Locked=True)


# Start
SafeMechanism()
