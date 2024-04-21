import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 보내는 사람, 받는 사람, 비밀번호, SMTP 서버 설정
smtp_server = "smtp.cafe24.com"
smtp_port = 587
smtp_user_email = "xxx@xxxx.cafe24.com"
smtp_user_password = "xxx!"

# 이메일 내용 구성
sender_email ="xxx@xxxx.cafe24.com" #이걸 체크하네?? smtp_user_email과 같아야 하네!??
receiver_email = "xxxx@icloud.com"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Hi! 폼메일!5"
   
body = '''
안녕하세요.
This is a email sent from cafe24 email smtp
감사합니다.
--
jHo
'''

message.attach(MIMEText(body, "plain"))

# SMTP 서버에 연결
server = smtplib.SMTP(smtp_server, smtp_port)
server.set_debuglevel(1)  # 디버그 모드 활성화
#server.starttls()
server.login(smtp_user_email, smtp_user_password)

# 이메일 보내기
server.sendmail(sender_email, receiver_email, message.as_string())

# SMTP 서버 연결 종료
server.quit()

print("Email sent successfully!")

