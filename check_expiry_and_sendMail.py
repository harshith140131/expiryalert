import time
import datetime
import sqlite3
# from send_mail import send_email  # Import the send_email function from the previous example
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import os
def main():
    def send_email(email, item, expiry_date):

        print("hi send email")
        # Set up SMTP server details
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "expiryrem@gmail.com"  # Update with your Gmail email address
        sender_password = "ouqd afvt qikr nzds"  # Update with your Gmail password
        


        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = f"Reminder: Expiry Date for {item}"
        print("hi email2")
        # Calculate reminder date (1 day before expiry)
        expiry_date = datetime.datetime.strptime(expiry_date, "%Y-%m-%d")
        reminder_date = expiry_date - datetime.timedelta(days=1)

        # Compose message body
        message_body = f"Reminder: The expiry date for {item} is approaching. Please take necessary actions.\n"
        message_body += f"Expiry Date: {expiry_date.strftime('%Y-%m-%d')}"
        msg.attach(MIMEText(message_body, 'plain'))
        print("hi email3")

        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        print("hi email4")

        # Send email
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
    def check_expiry_dates():
        print("check_expiry_dates")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "invoiceItems.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
    
        # Calculate reminder date (1 day before expiry)
        reminder_date = datetime.date.today()
        check_date = reminder_date + datetime.timedelta(days=10)
        print(check_date)
        print(type(check_date))
        check_date=str(check_date)
        # Query the database for items with expiry dates equal to the reminder date
        query = f"SELECT email, item, expiry_date FROM invoice_items WHERE expiry_date = '{check_date}'"
        print(query)
        c.execute(query)
        rows = c.fetchall()
        print(rows)
        for row in rows:
            email, item, expiry_date = row
            send_email(email, item, expiry_date)

        conn.close()
    check_expiry_dates()
    

# Schedule the check_expiry_dates function to run daily at midnight


if __name__=='__main__':
    print("executing")
    main()
