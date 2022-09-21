def start_service():
    from jnius import autoclass
    print("1 - start_service")
    service = autoclass("org.jupieter.coffee_ante.ServiceCoffeebar")
    mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
    service.start(mActivity, "")
    print("4 - start_service")
    return service

if __name__ == '__main__':
    start_service()
    


