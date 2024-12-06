import datetime
import os
import time
from timezones import TimeZones, TimezoneOffset


if __name__ == '__main__':
    app = TimezoneOffset(TimeZones.Central_Europe)
    app.setCountdownPoint(datetime.datetime(year=2023, month=12, day=3, hour=17, minute=30))
    now = datetime.datetime.now()
    lastSecond = now.second
    end = now + datetime.timedelta(hours=125)
    os.system('cls')
    lastText = ''
    while now < end:
        now = datetime.datetime.now()
        if now.second != lastSecond:
            timezone, hours, minutes, seconds = app.getLowestTimedelta()
            if timezone:
                if hours:
                    text = (f'{hours} hours\n{timezone}')
                elif minutes:
                    text = (f'{minutes} minutes\n{timezone}')
                else:
                    text = (f'{seconds} seconds\n{timezone}')
                if lastText != text:
                    # with open('test.txt', '+w') as file:
                    #     file.write(text)
                    os.system("cls" if os.name == "nt" else "clear")
                    print(text)
            lastSecond = now.second
        time.sleep(0.1)
