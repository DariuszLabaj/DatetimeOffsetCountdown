from src import MainWindow
import os
from py_resource_manager import ResourceManager
ResourceManager(os.path.dirname(os.path.abspath(__file__)) + "/Resources/Strings")
# from timezones import TimeZones


if __name__ == "__main__":
    mainViewModel = MainWindow(1024, 768)
    # mainViewModel.SetTimezoneOffset(TimeZones.Central_Europe)  # Set timezone manually if automatic one does not work for some reason
    # mainViewModel.SetDebug()
    mainViewModel.Start()
