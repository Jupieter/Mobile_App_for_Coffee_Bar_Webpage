from time import sleep
import requests
from jnius import autoclass

PythonService = autoclass('org.kivy.android.PythonService')
print("PythonService")
PythonService.mService.setAutoRestartService(True)

# def load_data():
#     try:
#         store = requests.get('https://coffeeanteportas.herokuapp.com/c_app/todaytcoffee/').json()
#         # print('STORE',store)
#         if store == []:
#             print('No coffee today')
#         else:
#             list_data = []
#             for item in store:
#                 list_data.append({'date': item['c_make_date'], "pkey": item['id']})
#             first_coffe = list_data[0]['date']
#             first_id = list_data[0]['pkey']
#             dt = first_coffe[0:10]+' ' + first_coffe[11:19]
#             print(first_id, ' Next Coffee:  ', dt)
#             return dt
#     except:
#         print('Problem with internet conection')
# 

while True:
    print("Coffeebar  service running.....")
    # dt = load_data()
    # print(dt)
    sleep(8)