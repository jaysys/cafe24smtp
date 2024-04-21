from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

app = Flask(__name__)

# SQLite3 database initialization
conn = sqlite3.connect('emails.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS emails
             (id INTEGER PRIMARY KEY AUTOINCREMENT, sender_email TEXT, receiver_email TEXT, subject TEXT, body TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        receiver_email = request.form['receiver_email']
        subject = request.form['subject']
        body = request.form['body']

        # Email sending
        smtp_server = "smtp.cafe24.com"
        smtp_port = 587
        smtp_user_email = "vvvv@smartcity.cafe24.com"
        smtp_user_pwd = "vvvv!"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        #server.starttls()
        server.set_debuglevel(1)  # 디버그 모드 활성화
        server.login(smtp_user_email, smtp_user_pwd)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        # Save email to database
        conn = sqlite3.connect('emails.db')
        c = conn.cursor()
        c.execute("INSERT INTO emails (sender_email, receiver_email, subject, body) VALUES (?, ?, ?, ?)",
                  (sender_email, receiver_email, subject, body))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

@app.route('/emails')
def emails():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute("SELECT * FROM emails")
    emails = c.fetchall()
    conn.close()
    return render_template('emails.html', emails=emails)

if __name__ == '__main__':
    app.run(debug=True)
