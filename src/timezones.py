import datetime
from enum import IntEnum
from typing import Optional


class TimeZones(IntEnum):
    Christmas_Island = 14
    New_Zealand = 13
    Fiji = 12
    Sydney = 11
    Queensland = 10
    Japan = 9
    China = 8
    Indonesia = 7
    Bangladesh = 6
    Pakistan = 5
    Azerbaijan = 4
    Russia = 3
    Greece = 2
    Central_Europe = 1
    United_Kingdom = 0
    Azores = -1
    Greenland = -2
    Brazil = -3
    Canada = -4
    East_USA = -5
    Central_USA = -6
    Mountain_USA = -7
    Pacific_USA = -8
    Alaska = -9
    Honolulu = -10
    Midway = -11
    Baker_Island = -12


class TimezoneOffset:
    def __init__(self, timezone: Optional[TimeZones] = None):
        if timezone:
            self.__timezone = timezone
        else:
            local_timezone = datetime.datetime.now().astimezone().tzinfo  # Get the system timezone
            if local_timezone is None:
                self.__timezone = TimeZones.Baker_Island
            else:
                offsetTime = local_timezone.utcoffset(datetime.datetime.now())
                offset_hours = offsetTime.seconds // 3600 if offsetTime is not None else 0
                self.__timezone = TimeZones(offset_hours)
        self.__ctdPtn = datetime.datetime(year=datetime.datetime.now().year+1, month=1, day=1)
        self.__timezonesOffsets = {x.name.replace('_', ' '): datetime.timedelta(
            hours=x-self.__timezone) for x in list(TimeZones)}

    def setCountdownPoint(self, countdownPoint: datetime.datetime):
        self.__ctdPtn = countdownPoint

    def getTimeInAllTimezones(self) -> dict[str, datetime.datetime]:
        now = datetime.datetime.now()
        return {name: now+offset for name, offset in list(self.__timezonesOffsets.items())}

    def getTimedeltaInAllTimezones(self):
        timezones = self.getTimeInAllTimezones()
        return {name: self.__ctdPtn-offset for name, offset in list(timezones.items())}

    def getLowestTimedelta(self):
        deltas = self.getTimedeltaInAllTimezones()
        future_deltas = {k: v for k, v in deltas.items() if v > datetime.timedelta()}
        if not future_deltas:
            timezone, min_delta = min(deltas.items(), key=lambda x: x[1])
        else:
            timezone, min_delta = min(future_deltas.items(), key=lambda x: x[1])
        totalSeconds = int(min_delta.total_seconds())
        hours, h_reminder = divmod(totalSeconds, 3600)
        minutes, seconds = divmod(h_reminder, 60)
        return timezone, hours, minutes, seconds
