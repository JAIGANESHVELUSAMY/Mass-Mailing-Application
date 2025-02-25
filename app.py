import streamlit as st
import smtplib
import pandas as pd
from email.message import EmailMessage

# Hardcoded app passwords for Gmail and Outlook
GMAIL_APP_PASSWORD = "asnh sgqb gmwr fhvs"  # Replace with your actual Gmail app password
OUTLOOK_APP_PASSWORD = "kjydtmsbmbqtnydk"  # Replace with your actual Outlook app password

# Streamlit app layout
st.title("Bulk Email Sender")

# Email provider selection
email_provider = st.radio("Select your email provider:", ("Gmail", "Outlook"))

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file with recipient email addresses", type="csv")

# Text input for sender email and subject/body
FROM_EMAIL = st.text_input("Enter your email address:", "")
SUBJECT = st.text_input("Enter the subject of the email:", "")
BODY = st.text_area("Enter the body of the email:", "")

# Function to send email
def send_email(from_email, to_emails, subject, body, provider):
    try:
        # Create the email message
        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = from_email
        message['To'] = ', '.join(to_emails)  # Join list into a string

        # Set SMTP server and password based on the selected provider
        if provider == "Gmail":
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            app_password = GMAIL_APP_PASSWORD
        else:  # Outlook
            smtp_server = "smtp.office365.com"
            smtp_port = 587
            app_password = OUTLOOK_APP_PASSWORD

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(from_email, app_password)  # Log in with the corresponding app password
            smtp.send_message(message)  # Send the email
            return "Email sent successfully to all recipients!"

    except Exception as e:
        return f"Error: {e}"

# Button to send the email
if st.button("Send Email"):
    if uploaded_file is not None and FROM_EMAIL and SUBJECT and BODY:
        # Read the CSV file
        try:
            df = pd.read_csv(uploaded_file)
            # Assuming the email addresses are in a column named 'email'
            to_emails_list = df['email'].dropna().tolist()  # Drop any NaN values and convert to list
            
            if to_emails_list:
                result = send_email(FROM_EMAIL, to_emails_list, SUBJECT, BODY, email_provider)
                st.success(result)
            else:
                st.error("No valid email addresses found in the CSV file.")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
    else:
        st.error("Please fill in all fields and upload a CSV file.")
