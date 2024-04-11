from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_mail(from_gmail, to_gmail, from_gmail_key):
    print("mail func called")
    message = MIMEMultipart()
    html = f"""
    <html>
        <head></head>
            <body>
                <h1>ALERT</h1>
                <h2>Too much crowd in the designated area! Please send a security.</h2>
            </body>
    </html>
    """
    body = MIMEText(html, 'html')
    message.attach(body)
    with open(f"captures/capture.png", "rb") as f:
        img_data = f.read()
        image = MIMEImage(img_data, name="test0.png")
        image.add_header('Content-ID', '<image1>')
        image.add_header('Content-Disposition', 'inline', filename='image.jpg')
        message.attach(image)
    message["Subject"] = f"Intrusion detection system"
    message["From"] = from_gmail
    message["To"] = to_gmail
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_gmail, from_gmail_key)
        server.sendmail(from_gmail, to_gmail, message.as_string())