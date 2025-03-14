import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Load user credentials from a YAML file
with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create authentication instance
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Login/Register UI
st.title("Expiry Alert System")

name, authentication_status, username = authenticator.login()



if authentication_status:
    st.sidebar.success(f"Welcome, {name}!")
    
    # Expiry Reminder Option
    st.subheader("Set Expiry Reminder")
    days_before_expiry = st.number_input("Send Reminder Before (Days)", min_value=1, max_value=30, step=1)

    # Display Email Sent Status
    if st.button("Check Emails Sent"):
        # Simulate checking sent emails
        st.write("Emails sent successfully!")

    authenticator.logout("Logout", "sidebar")

elif authentication_status is False:
    st.error("Username or password is incorrect")

elif authentication_status is None:
    st.warning("Please enter your username and password")

import streamlit as st
import smtplib
import pandas as pd
from email.message import EmailMessage
import datetime

# Function to send email
def send_email(to_email, subject, body):
    sender_email = "toontrendz14@gmail.com"   # Replace with your email
    sender_password = "$2b$12$y.K0Gr4IRy4DSjEM7B6a/uqHdyHSjkODo2sIGilY.2gTmYGfeGv3a"   # Replace with your app password

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"

# Streamlit UI
st.title("Expiry Alert System")

# User input: Email and Expiry Date
st.subheader("Set Expiry Reminder")
user_email = st.text_input("Enter your email:")
expiry_date = st.date_input("Select the expiry date:")
days_before_expiry = st.number_input("Send Reminder Before (Days)", min_value=1, max_value=30, step=1)

# Calculate reminder date
if expiry_date:
    reminder_date = expiry_date - datetime.timedelta(days=days_before_expiry)
    st.write(f"Reminder will be sent on: {reminder_date}")

# Send email button
if st.button("Send Expiry Reminder"):
    today = datetime.date.today()
    if today >= reminder_date:
        email_status = send_email(user_email, "Expiry Alert", f"Your item is about to expire on {expiry_date}!")
        st.write(email_status)
    else:
        st.write("Reminder email will be sent on the scheduled date.")
