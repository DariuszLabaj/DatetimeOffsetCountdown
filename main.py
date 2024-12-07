from mainWindow import MainWindow
# from timezones import TimeZones


if __name__ == "__main__":
    mainViewModel = MainWindow(1024, 768)
    # mainViewModel.SetTimezoneOffset(TimeZones.Central_Europe)
    mainViewModel.SetDebug()
    mainViewModel.Start()
