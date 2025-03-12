# https://www.youtube.com/watch?v=GQpQha2Mfpg
import os 
import glob
import pandas as pd
from twilio.rest import Client

# Your Account SID from twilio.com/console
# account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
account_sid = "AC8ad9f658f1fdcc374802542d26f70359"
# Your Auth Token from twilio.com/console
#auth_token  = "your_auth_token"
auth_token  = "c4b9794a933c80da41ae61b46ff3e559"
gsmfrom='+14233800948'
gsmto='+5531991018619'
client = Client(account_sid, auth_token)

cwd=os.getcwd()
list=glob.glob(cwd+"\\*.xlsx")

for file in list:
	print(f'Arquivo: {file}')
	tb=pd.read_excel(file)
	meta=3700
	if (tb['Valor Final'] >=meta).any():
		lines=tb.loc[tb['Valor Final'] >=meta]
		messagem=lines.values[0][2]
		print(messagem)

		message = client.messages.create(to=gsmto, from_=gsmfrom,body=messagem)
		#print(message.sid)
	#print(tb)
