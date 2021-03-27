from win10toast_click import ToastNotifier
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyperclip
import re
import webbrowser

hasGotFirst = False

toaster = ToastNotifier()

configFile = 'config.json' # Enter your own config file

cred = credentials.Certificate(configFile)
app = firebase_admin.initialize_app(cred, {
  'databaseURL': 'myDataBaseUrl' # this is not my actual database URL, for security purposes
})

def listener(data):
  global hasGotFirst
  if hasGotFirst:
    try:
      msg = str(data.data['value'])
      matches = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', msg)
      if matches:
        webbrowser.open(msg)
      else:
        toaster.show_toast("Data Sent From Phone", msg, callback_on_click=lambda val=msg: click(val), icon_path='')
    except:
      pass
  hasGotFirst = True

def click(data):
  pyperclip.copy(data)

db.reference('/').listen(listener)
