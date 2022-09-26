from time import sleep
import requests
from jnius import autoclass
# from plyer import notification
from  service.notification_android import AndroidNotification

PythonService = autoclass('org.kivy.android.PythonService')
print("PythonService")
PythonService.mService.setAutoRestartService(True)

def load_data():
    try:
        store = requests.get('https://coffeeanteportas.herokuapp.com/c_app/todaytcoffee/').json()
        # print('STORE',store)
        if store == []:
            dt = 'No coffee today'
        else:
            list_data = []
            for item in store:
                list_data.append({'date': item['c_make_date'], "pkey": item['id']})
            first_coffe = list_data[0]['date']
            first_id = list_data[0]['pkey']
            dt = first_coffe[0:10]+' ' + first_coffe[11:16]
            print(first_id, ' Next Coffee:  ', dt)
        return dt
    except:
        dt = 'Problem with internet conection'
        return dt


while True:
    dt = load_data()
    print("Coffeebar  service running.....", dt)
    try: 
        an = AndroidNotification()
        an.notify(title='New Coffee', message = dt,  toast=True)
    except:
        print("Maybe permission for service")
    sleep(15)