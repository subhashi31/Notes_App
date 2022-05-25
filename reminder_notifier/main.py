import time
from plyer import notification
import pymysql
from time import strftime
import datetime as dt

def notifyMe(message):
    for t in range(2):
        notification.notify(
            title="Reminder",
            message=message,
            app_icon="",
            timeout=5
        )
        time.sleep(50)

if __name__ == '__main__':



    while True:

        con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
        mycursor = con.cursor()

        mycursor.execute("select Date from reminder_table")
        dates = mycursor.fetchall()
        datelist = list(dates)

        sorted_dates=[]
        for i in datelist:
            for j in i:
                sorted_dates.append(j)

        sorted_dates.sort(key=lambda date: dt.datetime.strptime(date, "%d-%m-%Y"))

        print(sorted_dates)

        today = f"{dt.datetime.now():%d-%m-%Y}"
        print(today)

        if len(sorted_dates) > 0:

            while len(sorted_dates) > 0 and sorted_dates[0] != today:
                sorted_dates.pop(0)

            print(sorted_dates)

            if len(sorted_dates) > 0:
                if sorted_dates[0] == today:

                    mycursor.execute("select Time from reminder_table where Date=%s",(today))
                    times = mycursor.fetchall()
                    timelist = list(times)

                    sorted_times = []
                    for i in timelist:
                        for j in i:
                            sorted_times.append(j)


                    sorted_times = sorted(sorted_times)

                    time_now = strftime('%H:%M:%S')

                    while len(sorted_times) > 0 and sorted_times[0] < time_now:
                        sorted_times.pop(0)

                    if len(sorted_times) > 0:
                        if sorted_times[0] == time_now:

                            mycursor.execute("select Event from reminder_table where Time=%s", (sorted_times[0]))
                            message = mycursor.fetchone()
                            message = message[0]
                            print("here")
                            #notify function

                            notifyMe(message)

                            #delete reminder
                            mycursor.execute("DELETE from reminder_table where Event=%s and Date=%s and Time=%s", (message, sorted_dates[0], sorted_times[0]))

                            con.commit()
        con.close()









