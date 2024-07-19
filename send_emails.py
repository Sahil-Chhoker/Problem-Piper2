import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from fastapi import APIRouter, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from db.models.user import User
from db.session import SessionLocal
from core.config import settings
from db.repository.questions import get_a_random_question
from schemas.questions import Question
from apscheduler.triggers.cron import CronTrigger
import pytz

class EmailSender:
    def __init__(self):
        self.email_sender = settings.SENDER_EMAIL
        self.email_password = settings.EMAIL_PASSWORD
        self.smtp_server = 'smtp.gmail.com'
        self.port = 465

        if not self.email_password:
            raise ValueError("Email password not found in environment variables.")

    def send_email(self, receiver: str, subject: str, body: str):
        try:
            em = MIMEMultipart("alternative")
            em['From'] = self.email_sender
            em['To'] = receiver
            em['Subject'] = subject
            em.attach(MIMEText(body, "html"))

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.sendmail(self.email_sender, receiver, em.as_string())
        except Exception as e:
            if isinstance(e, OSError) and e.errno == 10060:
                time.sleep(5)
                self.send_email(receiver, subject, body)
            else:
                raise HTTPException(status_code=500, detail="Failed to send email.")

router = APIRouter()
email_sender = EmailSender()

def send_email_to_subscribers():
    db = SessionLocal()
    
    question = get_a_random_question(db)
    if not question:
        raise HTTPException(status_code=500, detail="Failed to fetch question.")
    question_data = Question.from_orm(question)

    subject = "Today's Question"
    body = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Today's Coding Question</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    background-color: #f0f4f8;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background-color: #4a90e2;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                }}
                .content {{
                    padding: 30px;
                }}
                .question {{
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    color: #2c3e50;
                }}
                .preview {{
                    font-style: italic;
                    margin-bottom: 20px;
                    color: #34495e;
                    background-color: #ecf0f1;
                    padding: 15px;
                    border-radius: 5px;
                }}
                .details {{
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .details p {{
                    margin: 5px 0;
                    color: #2c3e50;
                }}
                .details strong {{
                    color: #3498db;
                }}
                .link {{
                    display: inline-block;
                    background-color: #2ecc71;
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    text-align: center;
                    transition: background-color 0.3s ease;
                }}
                .link:hover {{
                    background-color: #27ae60;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    Daily Coding Challenge
                </div>
                <div class="content">
                    <div class="question">
                        {question_data.name}
                    </div>
                    <div class="preview">
                        {question_data.preview}
                    </div>
                    <div class="details">
                        <p><strong>Difficulty:</strong> {question_data.difficulty_name}</p>
                        <p><strong>Max Score:</strong> {question_data.max_score}</p>
                        <p><strong>Success Ratio:</strong> {question_data.success_ratio}</p>
                    </div>
                    <a class="link" href="{question_data.link}" target="_blank">Solve Challenge</a>
                </div>
                <div class="footer">
                    Happy coding!<br>
                    The Coding Challenge Team
                </div>
            </div>
        </body>
        </html>
        """


    try:
        subscribers = db.query(User).filter(User.is_subscribed == True).all()
        for subscriber in subscribers:
            email_sender.send_email(subscriber.email, subject, body)
    finally:
        db.close()

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Define the IST timezone
ist = pytz.timezone('Asia/Kolkata')

# Schedule the job to run every day at 9:30 AM IST
scheduler.add_job(
    send_email_to_subscribers, 
    CronTrigger(hour=22, minute=5, timezone=ist)
)

@router.on_event("startup")
async def startup_event():
    scheduler.start()

@router.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
