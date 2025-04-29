Verify Gmail App Password
Gmail requires an App Password for third-party apps (like your Flask app) when using SMTP with 2-Step Verification enabled.
Steps to generate an App Password:
Go to your Google Account: myaccount.google.com.
Enable 2-Step Verification if not already enabled (Security > 2-Step Verification).
Go to Security > App Passwords (search for "App Passwords" if not visible).
Select App: Mail and Device: Other (Custom Name), then generate a 16-character App Password.
Copy this password (e.g., xxxx xxxx xxxx xxxx).
Update .env File
Ensure your .env file contains the correct credentials:
text

Copy
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
Replace your_email@gmail.com with your Gmail address
Replace your_app_password with the 16-character App Password (no spaces).


Run the app:
Execute: python email_sender.py
The server will start at http://localhost:5000.  

the sent email might appear in the recipient spam folder 
