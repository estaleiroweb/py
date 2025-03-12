import pandas as pd
import openpyxl as xl
from twilio.rest import Client



# Your Account SID from twilio.com/console
# account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
account_sid = "AC8ad9f658f1fdcc374802542d26f70359"
# Your Auth Token from twilio.com/console
#auth_token  = "your_auth_token"
auth_token  = "c4b9794a933c80da41ae61b46ff3e559"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+5531991018619", 
    from_="+15017250604",
    body="Hello from Python!")

print(message.sid)




####################### FILES #######################

import os 
import glob

print("Path at terminal when executing this file")
cwd=os.getcwd()
print(cwd + "\n")

print("This file path, relative to os.getcwd()")
print(__file__ + "\n")

print("This file full path (following symlinks)")
full_path = os.path.realpath(__file__)
print(full_path + "\n")

print("This file directory and name")
path, filename = os.path.split(full_path)
print(path + ' --> ' + filename + "\n")

print("This file directory only")
print(os.path.dirname(full_path))

print("Files1")
print(os.listdir(cwd)) 
print([f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd,f)) and f.endswith(".py")]) 

print("Files2")
arr = []
# r=root, d=directories, f = files
for r, d, f in os.walk(cwd):
    for file in f:
        if file.endswith(".py"):
            arr.append(os.path.join(r, file))
print (arr)

print("Files3")
print(glob.glob("*.*")) 

print("Files4")
print(next(os.walk(cwd))[2])

print("Files5")
print([ f.name for f in os.scandir(cwd) if f.is_file() and f.name.endswith(".py")])
print([os.path.join(r,file) for r,d,f in os.walk(cwd) for file in f if file.endswith(".py") ])

print("Files6")
print([glob.glob(cwd+"\\*.xlsx")])
