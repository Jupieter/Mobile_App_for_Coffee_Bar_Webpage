'''
This python service file asks for the coffee-made id. 
If the id is greater than the file containing the id number, it sends a notification.
'''

from time import sleep
import requests
from jnius import autoclass
# from plyer import notification
from  service.notification_android import AndroidNotification

an = AndroidNotification()
PythonService = autoclass('org.kivy.android.PythonService')
print("PythonService")
PythonService.mService.setAutoRestartService(True)
# job_service = autoclass("org.jupieter.coffee_ante.Util")
print("No Job Service")
# job_service.setAutoRestartService(True)

try:
    ofi = open('max_coffee_id.txt', 'x')
    f = open('max_coffee_id.txt', 'w')
    f.write(str(0))
    f.close()
except:
    print("have file max_coffee_id.txt")

def open_file():
    ofi = open('max_coffee_id.txt', 'r')
    old_id = int(ofi.read())
    ofi.close()
    return old_id

def write_file(old_id = 0):
    f = open('max_coffee_id.txt', 'w')
    f.write(str(old_id))
    f.close()


def load_data():
    try:
        store = requests.get('https://coffeeanteportas.herokuapp.com/c_app/coffee_notify/').json()
        if store == []:
            dt = 'No coffee today'
        else:
            new_coffe = store["new_date"]
            max_id = store["max_id"]
            dt = new_coffe[0:10]+'\n' + new_coffe[11:16]       
        return max_id, dt
    except:
        dt = 'Problem with internet conection'
        return dt

# Timer not here in this python file is in JobSheduler

max_id, dt = load_data()
print("Coffeebar  service running.....", dt)
old_id = open_file()
print("old id:  ", old_id, "requested id:  ", max_id)
try:
    an.notify(title='Coffee Service', message = dt,  toast=True)
except:
    print("NO Toast")
if max_id > old_id:
    write_file(max_id)
    try: 
        an.notify(title='New Coffee', message = dt,  toast=False, app_icon='image/coffe_icon1.png')
        # notification.notify(title='New Coffee', message = dt,  toast=False)
    except:
        print("No work the notification")
