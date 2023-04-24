import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime
import time

my_sender = '2809744636@qq.com'
my_pass = 'mtplhanyxzjddfjb'
my_user = '285723576@qq.com'

messages = [
    "记得吃药， 心脏药， 胃药。爱你的儿子",
    "记得吃药， 心脏药， 胃药。爱你的儿子，别忘了吊针哦",
    "记得吃药， 心脏药， 胃药。爱你的儿子，别忘了吊针哦(看到这个记得给我看看我改一下代码)"
]

subjects = [
    "记得吃药",
    "记得吃药,别忘了吊针哦",
    "记得吃药(看到这个记得给我看看我改一下代码)"
]

sent_count = 0
subject_index_offset = 0
last_subject_reset_date = datetime.datetime.now().date()


def mail():
    ret = True
    # try:
    global sent_count, subject_index_offset, last_subject_reset_date
    message_index = ((int(sent_count) // 60) % 3)
    subject_index = (((int(sent_count) // 3) % 60) + int(subject_index_offset)) % 3

    if sent_count == 180:
        current_date = datetime.datetime.now().date()


        if (current_date - datetime.datetime.strptime(last_subject_reset_date, '%Y-%m-%d').date()).days >= 30:
            subject_index_offset = 0
            last_subject_reset_date = current_date.isoformat()
        else:
            subject_index_offset = 1

        sent_count = 0

    msg = MIMEText(messages[message_index], 'plain', 'utf-8')
    msg['From'] = formataddr(["Your son", my_sender])
    msg['To'] = formataddr(["JF", my_user])
    msg['Subject'] = f"{subjects[int(subject_index)]} ({int(sent_count) + 1}/{180})"

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()

    sent_count = str(int(sent_count) +1 )
    print(f"Email sent successfully. Total emails sent: {sent_count}")

    # Save the current state to a file
    with open("email_state.txt", "w") as f:
        f.write(f"{sent_count},{subject_index_offset},{last_subject_reset_date}")


# except Exception as e:
# ret = False
# print(f"Email sending failed. Error message: {str(e)}")

# return ret


print("Start")
# Load the previous state if available
try:
    if os.path.exists('email_state.txt'):
        with open('email_state.txt', mode='r', encoding='utf-8') as f:
            sent_count, subject_index_offset, last_subject_reset_date = f.read().split(",")
            print(
                f"Loaded previous state: sent count = {sent_count}, subject index offset = {subject_index_offset}, last subject reset date = {last_subject_reset_date}")
    else:
        with open("email_state.txt", mode='w', encoding='utf-8') as f:
            initial_state = f"0,0,{datetime.datetime.now().date().isoformat()}"
            f.write(initial_state)
            sent_count, subject_index_offset, last_subject_reset_date = initial_state.split(",")
            print(f"No prior state found. Created a new one: {initial_state}")
except FileNotFoundError:
    pass

# Send a start-up email
mail_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with smtplib.SMTP_SSL("smtp.qq.com", 465) as connection:
    msg = MIMEText("The automated email program has started.", 'plain', 'utf-8')
    msg['From'] = formataddr(["sender", my_sender])
    msg['To'] = formataddr(["CK", "285723576@qq.com"])
    msg['Subject'] = "Program started at {}".format(mail_time)

    connection.login(my_sender, my_pass)
    connection.sendmail(my_sender, [my_user], msg.as_string())
    print("Start-up email sent!")

# Send the emails every day at 9am, 12pm, and 10pm
while True:
    now = datetime.datetime.now()

    # Send emails at 9am, 12pm, and 10pm
    for i in [(9, 0), (12, 0), (21, 0)]:
        if now.hour == i[0]:  # and now.minute == i[1]:
            mail()
            print(f"Sending email at {now}.")

    time.sleep(60)  # Sleep for 1 minute before checking again
