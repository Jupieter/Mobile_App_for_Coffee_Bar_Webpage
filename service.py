from time import sleep

from jnius import autoclass

PythonService = autoclass('org.kivy.android.PythonService')
print("PythonService")
PythonService.mService.setAutoRestartService(True)


while True:
    print("Coffeebar  service running.....")
    sleep(5)