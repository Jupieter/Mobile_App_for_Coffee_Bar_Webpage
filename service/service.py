from time import sleep
import requests
from jnius import autoclass
from plyer import notification

PythonService = autoclass('org.kivy.android.PythonService')
print("PythonService")
PythonService.mService.setAutoRestartService(True)

def load_data():
    notification.notify(title='New Coffee', message="New coffe time:", toast=True, timeout=1)
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
            dt = first_coffe[0:10]+' ' + first_coffe[11:19]
            print(first_id, ' Next Coffee:  ', dt)
        return dt
    except:
        dt = 'Problem with internet conection'
        return dt


while True:
    dt = load_data()
    print("Coffeebar  service running.....", dt)
    sleep(10)