import enum


class ProgramMode(enum.Enum):
    TimeZoneDisplay = enum.auto()
    PreCountDown = enum.auto()
    CountDown = enum.auto()
    PostCountDown = enum.auto()
