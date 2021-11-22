"""
Welcome to SafeMechanism(GUI).


"""

# Imports
import tkinter as tk
import tkinter.messagebox
import sys
import os
import base64
import pyAesCrypt as aes

def DenzEncrypt(InputFile,InputPin):
    global PIN
    global PassKey

    buffer = 64 * 1024
    PathToFile,FileExt = os.path.splitext(InputFile)
    OutputFile1 = f"{PathToFile}.denz~"
    OutputFile = f"{PathToFile}.denz"
    ConfigText = f"####DenzEncrypt####|{InputPin}|{PathToFile}|{InputFile}|{OutputFile}|####\n"
    with open(InputFile,'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.write(ConfigText)
        for line in lines:
            f.write(line)
        f.close()
    aes.encryptFile(InputFile,OutputFile1,InputPin,buffer)
    base64.encode(open(OutputFile1,"rb"),open(OutputFile,"wb"))
    os.remove(InputFile)
    os.remove(OutputFile1)

def DenzDecrypt(InputFile,InputPin):
    global PIN
    global PassKey
    buffer = 64 * 1024
    PathToFile,FileExt = os.path.splitext(InputFile)
    OutputFile1 = f"{PathToFile}.denz~"
    OutputFile = f"{PathToFile}.txt"
    base64.decode(open(InputFile,"rb"),open(OutputFile1,"wb"))
    try:
        aes.decryptFile(OutputFile1,OutputFile,InputPin,buffer)
    except Exception:
        PIN = ''
        e.delete('0', 'end')
        os.remove(OutputFile1)
        tkinter.messagebox.showerror('PIN ERROR!', 'PIN entered is Incorrect!')

    with open(OutputFile,'r+') as f:
        FirstLine = f.readline()
        print(FirstLine)
        FileInfo = FirstLine.split("|")
        if FileInfo[0] == "####DenzEncrypt####":
            PassKey = FileInfo[1]
            #PathToFile = FileInfo[2]
            #InputFile = FileInfo[3]
            #OutputFile = FileInfo[4]
            return PassKey
    
def EncryptFile(InputFile,InputPin):
    global PIN
    global PassKey
    global SafeContent
    buffer = 64 * 1024
    """INFO INFO.

    info
    """

    PathToFile,FileExt = os.path.splitext(InputFile)
    if FileExt == '.txt':
        if len(PIN) >= 3 and len(PIN) <= 6:
            print("PIN SET")
            PIN = ''
            e.delete('0', 'end')
            tkinter.messagebox.showinfo('PIN SET', f'PIN has been set to: {InputPin}')            
            DenzEncrypt(InputFile,InputPin)
            tkinter.messagebox.showinfo('Response', f'Okay, {InputFile} has been locked sucessfully')
            root.destroy()

        else:
            print("PIN NOT VALID!")
            print("INVALID PIN: " + PIN)
            PIN = ''
            e.delete('0', 'end')
            tkinter.messagebox.showerror('PIN NOT VALID!', 'PIN entered is invalid, the PIN must be between 3-6 chars long!')

    elif FileExt == '.denz':
        OutputFile = f"{PathToFile}.txt"
        OutputFile1 = f"{PathToFile}.denz~"
        PassKey = DenzDecrypt(InputFile,InputPin)
        if InputPin == PassKey:
            with open(OutputFile, 'r') as f:
                data = f.read().splitlines(True)
            with open(OutputFile, 'w') as f:
                f.writelines(data[1:])
                os.remove(InputFile)
                os.remove(OutputFile1)
            print("PIN OK")
            print("OK PIN: " + PIN)
            PIN = ''
            e.delete('0', 'end')
            tkinter.messagebox.showinfo('PIN OK', f'PIN is Correct! {InputFile} unlocked')
            PassKey = None
            root.destroy()

        else:
            print("PIN ERROR2!")
            print("ERROR PIN: " + PIN)
            PIN = ''
            e.delete('0', 'end')
            tkinter.messagebox.showerror('PIN ERROR!', 'PIN entered is Incorrect!')
            #os.remove(OutputFile)
            #os.remove(OutputFile1)
            EncryptFile(InputFile,PassKey)

    else:
        tkinter.messagebox.showwarning('File Error!', 'InputFile is not a .txt file!')
        return


def GetSafeContent():
    """INFO INFO.

    info
    """
    global user_text
    global SafeContent
    SafeContent = user_text.get("1.0", 'end-1c')
    print("SafeContent: " + SafeContent)
    top.destroy()
    tkinter.messagebox.showinfo('CONTENT SET', 'SafeContent has been set!')
    tkinter.messagebox.showinfo('Response', 'Okay, your safe has been locked sucessfully')


def GetUserInput():
    """INFO INFO.

    info
    """
    global user_text
    global top

    top = tk.Toplevel()
    top.title("User Input")
    try:
        top.iconbitmap("Icons\\SafeMechaismIcon.ico")
        pass
    except Exception as e:
        pass


    my_frame = tk.Frame(top)
    my_frame.pack(padx=5, pady=5)

    text_scroll = tk.Scrollbar(my_frame)
    text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    user_text = tk.Text(my_frame, width=50, height=15, font=('Helvetica', 16),
                        selectbackground='yellow', selectforeground='black',
                        undo=True, yscrollcommand=text_scroll.set)
    user_text.pack()

    text_scroll.config(command=user_text.yview)

    text_submit_btn = tk.Button(top, text='Submit Text', command=GetSafeContent)
    text_submit_btn.pack(pady=10)


def MainSafe(value):
    """INFO INFO.

    info
    """
    global PIN
    global PassKey
    global SafeContent

    if value == '*':
        PIN = PIN[:-1]
        e.delete('0', 'end')
        e.insert('end', PIN)

    elif value == '#':
        if PassKey is None and len(sys.argv) == 1:
            if len(PIN) >= 3 and len(PIN) <= 6:
                PassKey = PIN
                print("PIN SET")
                print("PassKey: " + PassKey)
                PIN = ''
                e.delete('0', 'end')
                tkinter.messagebox.showinfo('PIN SET', f'PIN has been set to: {PassKey}')

                SafeContentPerm = tkinter.messagebox.askquestion('askquestion', 'Do you want to put some content?')
                if SafeContentPerm == 'yes':
                    GetUserInput()
                elif SafeContentPerm == 'no':
                    tkinter.messagebox.showinfo('Response', 'Okay, your safe has been locked sucessfully')
                    SafeContent = None
                else:
                    tkinter.messagebox.showwarning('error', 'Something went wrong!')

            else:
                print("PIN NOT VALID!")
                print("INVALID PIN: " + PIN)
                # clear `PIN`
                PIN = ''
                # clear `entry`
                e.delete('0', 'end')
                tkinter.messagebox.showerror('PIN NOT VALID!', 'PIN entered is invalid, the PIN must be between 3-6 chars long!')

        elif sys.argv[1] is not None:
            EncryptFile(sys.argv[1],PIN)

        else:
            print("PIN ERROR!")
            print("ERROR PIN: " + PIN)
            PIN = ''
            e.delete('0', 'end')
            tkinter.messagebox.showerror('PIN ERROR!', 'PIN entered is Incorrect!')

    else:
        PIN += value
        e.insert('end', value)

        if PIN == PassKey:
            print("PIN OK")
            print("OK PIN: " + PIN)
            PIN = ''
            e.delete('0', 'end')
            tkinter.messagebox.showinfo('PIN OK', 'PIN is Correct! unlocked')
            print("SafeContent :" + SafeContent)
            if SafeContent is not None:
                tkinter.messagebox.showinfo('Your Message', f'your message was: \n {SafeContent}')
            PassKey = None

    print("Current: ", PIN)


NumPad = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#'],
]

PIN = ''
PassKey = None
SafeContent = None

root = tk.Tk()
root.title("SafeMechaism(GUI)")
root.geometry('350x450+700+200')
try:
    top.iconbitmap("Icons\\SafeMechaismIcon.ico")
    pass
except Exception as e:
    pass

e = tk.Entry(root, font=("Calibri 20"))
e.grid(row=0, column=0, columnspan=3, ipady=10)

for y, row in enumerate(NumPad, 1):
    for x, key in enumerate(row):
        tk.Grid.columnconfigure(root,x,weight=1)
        tk.Grid.rowconfigure(root,y,weight=1)
        b = tk.Button(root, text=key, command=lambda val=key: MainSafe(val), font=("Calibri 20"))
        b.grid(row=y, column=x,sticky="NSEW")

tkinter.messagebox.showinfo('Welcome!', "Welcome to the Safe! this is a temporary safe that remembers your last put password and locks it until unlocked and forgets the password! click ok to use the safe!",parent=root)
root.mainloop()
