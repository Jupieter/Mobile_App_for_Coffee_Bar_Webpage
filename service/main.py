def start_service():
    from jnius import autoclass, cast
    print("1 - start_service")
    # service = autoclass("org.jupieter.coffee_ante.ServiceCoffeebar")
    # mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
    # service.start(mActivity, "")

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    try:
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        print("currentActivity",currentActivity)
    except:
        print("NO   currentActivity")
    try:
        context = cast('android.content.Context', currentActivity.getApplicationContext())
        print("context",context)
    except:
        print("NO   context")
    try:
        service = autoclass("org.jupieter.coffee_ante.MsgPushService")
        # service = autoclass("org.jupieter.coffee_ante.ServiceCoffeebar")
    except:
        print("NO   MsgPushService")
    # try:
    #     service.start(currentActivity, "")
    #     # context.startService(service)
    # except:
    #     print("NO   MsgPushService")
    return service

    # try:
    #     context = cast('android.content.Context', currentActivity.getApplicationContext())
    #     print("context",context)
    # except:
    #     print("NO   context")
    # PythonActivity = autoclass('org.kivy.android.PythonActivity')
    # try:
    #     currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
    #     print("currentActivity",currentActivity)
    # except:
    #     print("NO   currentActivity")
    # try:
    #     job_service = autoclass("org.jupieter.coffee_ante.Util")
    #     print("job_service",job_service)
    # except:
    #     print("NO   job_service")
    # try:
    #     job_service.scheduleJob(context)
    #     print("job_service.scheduleJob",job_service)
    # except:
    #     print("NO   job_service.scheduleJob")
    # print("4 - start_service")
    # return job_service

if __name__ == '__main__':
    start_service()
    


