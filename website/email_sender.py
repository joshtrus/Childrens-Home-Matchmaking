import smtplib
import sqlite3
import string

conn = sqlite3.connect('email_list.db')
cursor = conn.cursor()

## getting 'emails' column from the table
cursor.execute("SELECT email FROM email_list")

## fetching all usernames from the 'cursor' object
emails = cursor.fetchall()

# function for sending the emails
def send_email(message): 
    for email in emails:
        strippedText = str(email).replace('(','').replace(')','').replace(',','').replace('\"','')
        server = smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login("emailfortesting2345@gmail.com", "aawu hqdr jrtj kejp")
        server.sendmail("emailfortesting2345@gmail.com",
                        strippedText,
                        message)
        server.quit()


message = input("Please insert email you would like to send? ")
send_email(message)




    

