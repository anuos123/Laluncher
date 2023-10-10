from winotify import Notification
import datetime
import time
import getpass
import schedule

def notify():

    # pm弹窗时间周四/周五 5点弹窗,网页是https://kitsu.zuru.cloud/timesheets/
    # at弹窗时间,网页是https://kitsu.zuru.cloud/my-tasks/timesheets：
    # 日报 - 星期1-星期5,每天上午10点半和下午5点各自弹一次,持续10分钟(已填写,则不会触发)
    # 周报 - 周四-周五,每天下午4点半 - 5点,持续20分钟(已填写,则不会触发)

    # 获取当前时间
    now = datetime.datetime.now()
    print(now)
    weekday = now.strftime("%A")

    # 获取当前用户名称
    username = getpass.getuser()
    if username=='lvy':
        launch = 'https://kitsu.zuru.cloud/timesheets'
    else:
        launch = 'https://kitsu.zuru.cloud/my-tasks/timesheets'

    task = f'{weekday} Task'
    daily = r'每日任务'
    message = f"Hi,{username}\n现在是休息时间...\n填写{daily},才能劳逸结合..."
    icon = r"C:/Users/kangwen/Desktop/ZT_Install/logo.ico"

    toast = Notification(app_id=task,
                         title=daily,
                         msg=message,
                         icon=icon,
                         duration='long',
                         launch=launch
                         )

    toast.show()

def run():
    at_time = '11:10','11:12','11:42',"16:05","16:10","16:15"
    for at in at_time:
        schedule.every().monday.at(at).do(notify)
        schedule.every().tuesday.at(at).do(notify)
        schedule.every().wednesday.at(at).do(notify)
        schedule.every().thursday.at(at).do(notify)
        schedule.every().friday.at(at).do(notify)

    while True:
        schedule.run_pending()
        time.sleep(1)
