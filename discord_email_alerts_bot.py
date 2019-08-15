import discord
from discord.ext import commands
import email
import imaplib
import time

##username and password for Gmail Account
username = '' 
password = ''

##login to gmail via imap
mail = imaplib.IMAP4_SSL("imap.gmail.com") 
mail.login(username, password)

##discord bot initialisation and async def
client = commands.Bot(command_prefix = '.')
@client.event
async def on_ready():

    print("Bot is ready")
    
    ##defining variables for storing raw email data and count logic
    previous_subject = ""
    previous_date = ""
    whole_Counter = 0
    subject_list = []
    from_list = []
    date_list = []
    x = True

    ##runs endless loop to check for new emails
    while x == True:
        n = -1

        ##while size of subject list is not equal to 5
        while (len(subject_list) != 5):

            ##select inbox, strip down into emails and extract data into variables
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
            
            ##check for attachments
            counter = 1
            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                filename = part.get_filename()
                if not filename:
                     ext = '.html'
                     filename = 'msg-part-%08d%s' %(counter, ext)
                counter += 1
                
            ##logic to filter out tradingview emails
            if (("liked" or "is now following") not in (subject_)) and (from_ == "TradingView <noreply@tradingview.com>"):
                subject_list.append(subject_)
                from_list.append(from_)
                date_list.append(date_)
            n = n-1

        ##logic to check for new alerts and post them to specific channel
        k=0
        if (previous_date != date_list[0]):
            print("New emails!")

            while ((whole_Counter !=0) and (date_list[k] != previous_date)):
                if (("TradingView Alert:" in subject_list[k]) and ("1H" in subject_list[k])):
                    channel = client.get_channel() ##fill in channel ID
                    await channel.send("@everyone **"+subject_list[k]+"**")
                if(("TradingView Alert:" in subject_list[k]) and ("15M" in subject_list[k])):
                    channel = client.get_channel() ##fill in channel ID
                    await channel.send("@everyone **"+subject_list[k]+"**")
                if (k == 4):
                    break
                k=k+1

        ##Assigning variables for iterative logic
        whole_Counter = whole_Counter + 1
        previous_subject = subject_list[0]
        previous_date = date_list[0]
        
        #Clear lists
        subject_list.clear()
        from_list.clear()
        date_list.clear()

        #Print iteration count and wait 500 seconds for next check
        print(whole_Counter)
        time.sleep(500)

client.run('') ##discord client ID










