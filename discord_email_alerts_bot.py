import discord
from discord.ext import commands
import email
import imaplib
import time

username = '' #email
password = '' #password

client = commands.Bot(command_prefix = '.')

##async function runs on program startup
@client.event
async def on_ready():
    
    ##initialise lists and iteration variables
    print("Bot is ready")
    previous_subject = ""
    previous_date = ""
    whole_Counter = 0
    subject_list = []
    from_list = []
    date_list = []
    x = True
    
    ##loop to run main body of code inside async function
    while x == True:
        
        ##login with Imap
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        r, d = mail.login(username, password)
        assert r == 'OK', 'login failed'
        n = -1
        
        ##try and except statement,
        try:
            
            #if decompose inbox into emails and emails into data, put data into lists
            while (len(subject_list) != 5):
                mail.select("inbox")
                result, data = mail.uid('search', None, "ALL")
                inbox_item_list = data[0].split()
                most_recent = inbox_item_list[n]
                oldest = inbox_item_list[0]
                result2, email_data = mail.uid('fetch', most_recent, '(RFC822)')
                raw_email = email_data[0][1].decode("utf-8")
                email_message = email.message_from_string(raw_email)
                from_= email_message['From']
                subject_ = email_message['Subject']
                date_ = email_message['Date']

                counter = 1
                for part in email_message.walk():
                    if part.get_content_maintype() == "multipart":
                        continue
                    filename = part.get_filename()
                    if not filename:
                         ext = '.html'
                         filename = 'msg-part-%08d%s' %(counter, ext)
                    counter += 1

                ##filter emails to be posted    
                if (("" or "") not in (subject_)) and (from_ == ""):
                    subject_list.append(subject_)
                    from_list.append(from_)
                    date_list.append(date_)
                n = n-1

            k=0
            if (previous_date != date_list[0]):
                print("New emails!")

                ##checks if email subjects in list meet criteria and posts to channel
                while ((whole_Counter !=0) and (date_list[k] != previous_date)):
                    if (("" in subject_list[k]) and ("" in subject_list[k])):
                        channel = client.get_channel() ##enter specific channel
                        await channel.send("@everyone **"+subject_list[k]+"**")
                    if(("TradingView Alert:" in subject_list[k]) and ("15M" in subject_list[k])):
                        channel = client.get_channel() ##enter specific channel
                        await channel.send("@everyone **"+subject_list[k]+"**")
                    if (k == 4):
                        break
                    k=k+1

            ##counter iterations and variable assignments for comparisons in next iteration
            whole_Counter = whole_Counter + 1
            previous_subject = subject_list[0]
            previous_date = date_list[0]

            ##clear lists
            subject_list.clear()
            from_list.clear()
            date_list.clear()
            
            ##print iteration number, sleep for 5 minutes before checking for new emails
            print(whole_Counter)
            time.sleep(300)
        
        #catch any exceptions, logout
        except mail.abort:
            continue
        mail.logout()
            
client.run('') ##enter discord client number
