import os
import smtplib
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Email configuration
app.config['EMAIL_USERNAME'] = os.getenv('EMAIL_USERNAME')
app.config['EMAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['SMTP_SERVER'] = os.getenv('SMTP_SERVER')
app.config['SMTP_PORT'] = int(os.getenv('SMTP_PORT', 587))
app.config['EMAIL_SENDER_NAME'] = os.getenv('EMAIL_SENDER_NAME', 'Wami22')

def create_email(sender, recipient, subject, body):
    """Create a properly formatted email message"""
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{app.config['EMAIL_SENDER_NAME']} <{sender}>"
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['Date'] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    msg['Message-ID'] = f"<{datetime.now().timestamp()}@{app.config['SMTP_SERVER'].split('.')[0]}>"
    
    # Add both plain text and HTML versions
    text_part = MIMEText(body, 'plain')
    html_part = MIMEText(f"<html><body>{body}</body></html>", 'html')
    
    msg.attach(text_part)
    msg.attach(html_part)
    
    return msg

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not all([recipient, subject, message]):
            flash('All fields are required.')
            return redirect(url_for('index'))

        try:
            # Create email message
            email = create_email(
                sender=app.config['EMAIL_USERNAME'],
                recipient=recipient,
                subject=subject,
                body=message
            )

            # Send email
            with smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT']) as server:
                server.starttls()
                server.login(app.config['EMAIL_USERNAME'], app.config['EMAIL_PASSWORD'])
                server.sendmail(
                    app.config['EMAIL_USERNAME'], 
                    recipient, 
                    email.as_string()
                )
            
            flash('Email sent successfully! Check your inbox.')
        except Exception as e:
            flash(f'Failed to send email: {str(e)}')
        
        return redirect(url_for('index'))
    
    return render_template('inbox.html')

if __name__ == '__main__':
    app.run(debug=True)