def start_service():
    from jnius import autoclass, cast
    print("1 - start_service")
    # service = autoclass("org.jupieter.coffee_ante.ServiceCoffeebar")
    mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
    # service.start(mActivity, "")
    # PythonActivity = autoclass('org.kivy.android.PythonActivity')
    # currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
    # context = cast('android.content.Context', currentActivity.getApplicationContext())
    job_service = autoclass("org.jupieter.coffee_ante.Util")
    context = mActivity.getApplicationContext()
    job_service.scheduleJob(context)
    print("4 - start_service")
    # return job_service

if __name__ == '__main__':
    start_service()
    


