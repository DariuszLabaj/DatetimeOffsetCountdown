from py_resource_manager import ResourceManager

class StringsClass:
    """Auto-generated resource class"""
    _rm = ResourceManager()
    def findString(self, value: str) -> str:
        return self._rm.get_string(value.replace(" ", "")).strip()

    @property
    def NextTimezone(self) -> str:
        return self._rm.get_string("NextTimezone").strip()
    @property
    def HappyNewYear(self) -> str:
        return self._rm.get_string("HappyNewYear").strip()
    @property
    def HoursLeft(self) -> str:
        return self._rm.get_string("HoursLeft").strip()
    @property
    def MinutesLeft(self) -> str:
        return self._rm.get_string("MinutesLeft").strip()
    @property
    def ChristmasIsland(self) -> str:
        return self._rm.get_string("ChristmasIsland").strip()
    @property
    def NewZealand(self) -> str:
        return self._rm.get_string("NewZealand").strip()
    @property
    def Fiji(self) -> str:
        return self._rm.get_string("Fiji").strip()
    @property
    def Sydney(self) -> str:
        return self._rm.get_string("Sydney").strip()
    @property
    def Queensland(self) -> str:
        return self._rm.get_string("Queensland").strip()
    @property
    def Japan(self) -> str:
        return self._rm.get_string("Japan").strip()
    @property
    def China(self) -> str:
        return self._rm.get_string("China").strip()
    @property
    def Indonesia(self) -> str:
        return self._rm.get_string("Indonesia").strip()
    @property
    def Bangladesh(self) -> str:
        return self._rm.get_string("Bangladesh").strip()
    @property
    def Pakistan(self) -> str:
        return self._rm.get_string("Pakistan").strip()
    @property
    def Azerbaijan(self) -> str:
        return self._rm.get_string("Azerbaijan").strip()
    @property
    def Russia(self) -> str:
        return self._rm.get_string("Russia").strip()
    @property
    def Greece(self) -> str:
        return self._rm.get_string("Greece").strip()
    @property
    def CentralEurope(self) -> str:
        return self._rm.get_string("CentralEurope").strip()
    @property
    def UnitedKingdom(self) -> str:
        return self._rm.get_string("UnitedKingdom").strip()
    @property
    def Azores(self) -> str:
        return self._rm.get_string("Azores").strip()
    @property
    def Greenland(self) -> str:
        return self._rm.get_string("Greenland").strip()
    @property
    def Brazil(self) -> str:
        return self._rm.get_string("Brazil").strip()
    @property
    def Canada(self) -> str:
        return self._rm.get_string("Canada").strip()
    @property
    def EastUSA(self) -> str:
        return self._rm.get_string("EastUSA").strip()
    @property
    def CentralUSA(self) -> str:
        return self._rm.get_string("CentralUSA").strip()
    @property
    def MountainUSA(self) -> str:
        return self._rm.get_string("MountainUSA").strip()
    @property
    def PacificUSA(self) -> str:
        return self._rm.get_string("PacificUSA").strip()
    @property
    def Alaska(self) -> str:
        return self._rm.get_string("Alaska").strip()
    @property
    def Honolulu(self) -> str:
        return self._rm.get_string("Honolulu").strip()
    @property
    def Midway(self) -> str:
        return self._rm.get_string("Midway").strip()
    @property
    def BakerIsland(self) -> str:
        return self._rm.get_string("BakerIsland").strip()

Strings = StringsClass()