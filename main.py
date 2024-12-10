import os
import sys
from typing import Optional
from py_resource_manager import ResourceManager
import pygame
ResourceManager(os.path.dirname(os.path.abspath(__file__)) + "/Resources/Strings")

from src.timezones import TimeZones
from src import MainWindow
import argparse


def process_args(args: Optional[list[str]] = None) -> list[str]:
    """
    Processes raw arguments by removing the script path if present and splitting combined arguments.

    Args:
        args (Optional[list[str]], optional): The list of arguments to process. Defaults to sys.argv.

    Returns:
        list[str]: A list of processed arguments.
    """
    if args is None:
        args = sys.argv
    script_path = os.path.abspath(__file__)
    if args and script_path == os.path.abspath(args[0]):
        args = args[1:]
    processed_args: list[str] = []
    for arg in args:
        if " " in arg:
            processed_args.extend(arg.split())
        elif arg:
            processed_args.append(arg)
    return processed_args

if __name__ == "__main__":
    raw_args = process_args()
    parser = argparse.ArgumentParser(description="Countdown script for New Year celebrations.")
    parser.add_argument("--timezone", "-t ", type=str, help="Specify the timezone for the countdown")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--windowed", "-w", action="store_true", help="Enable windowed mode")
    args = parser.parse_args(raw_args)
    timezone:TimeZones | None = TimeZones.get(args.timezone) if isinstance(args.timezone, str) else None
    if args.windowed:
        mainViewModel = MainWindow(1024, 768)
    else:
        mainViewModel = MainWindow(1024, 768, flags=pygame.SRCALPHA | pygame.FULLSCREEN)
    if timezone is not None:
        if args.verbose: print(f"Countdown for timezone: {timezone}")
        mainViewModel.SetTimezoneOffset(timezone)  # Set timezone manually if automatic one does not work for some reason
    if args.debug:
        if args.verbose: print("Debug mode enabled")
        mainViewModel.SetDebug()
    mainViewModel.Start()