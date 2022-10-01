

def start_service():
    from jnius import autoclass, cast

    print("1 - start_service")
    service = autoclass("org.jupieter.coffee_ante.ServiceCoffeebar")
    mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
    service.start(mActivity, "")
    try:
        msg_service = autoclass("org.jupieter.coffee_ante.MsgPushService")
        print("service",service)
    except:
        print("NO   MsgPushService")
    try:
        msg_service.start(mActivity)
    except:
        print("NO   msg_service.start")


    try:
        import android
        sdk = android.io.Build.VERSION.SDK_INT
        print("SDK_INT", sdk)
        cod = android.io.Build.VERSION_CODES.O
        print("CODES: ", cod)
       
    except:
        print("NO   msg_service.start")


    return service



if __name__ == '__main__':
    start_service()
    


