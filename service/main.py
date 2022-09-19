@staticmethod
def start_service():
    from jnius import autoclass
    print("1 - start_service")
    service = autoclass("org.jupieter.coffee_ante.ServiceCoffeebar")
    print("2 - start_service")
    mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
    print("3 - start_service")
    service.start(mActivity, "")
    print("4 - start_service")
    return service


