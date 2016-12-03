""" Initializer

Initialize system directories, files and database.

Created by Lahiru Pathirage @ Mooniak<lpsandaruwan@gmail.com> on 2/12/2016
"""

import os, getpass, platform
from os.path import expanduser
from sqlalchemy import create_engine

from service import ChannelService, SystemService
from session import Base, version
from utility import FileManager


def initialize():

    # home directory
    home_directory = expanduser('~')

    # operating system
    system = platform.system()

    # system font directory
    font_directory = ""

    # set system font directory considering operating system type
    if "linux" in system.lower():
        font_directory = home_directory + "/.fonts"
    elif "osx" in system.lower():
        font_directory = home_directory + "/Library/Fonts"
    elif "windows" in system.lower():
        font_directory = os.environ["SYSTEMDRIVE"] + "\\\\Windows\\Fonts"

    # create directories
    file_manager = FileManager()

    file_manager.create_directory(home_directory + '/.fontman')
    file_manager.create_directory(home_directory + '/.fontman/temp')

    # create database
    engine = create_engine(
        'sqlite:///' + home_directory + '/.fontman/fontman.db'
    )
    Base.metadata.create_all(engine)

    # write application initial data
    SystemService().add_new(
        home_directory,
        font_directory,
        system,
        '1h',
        getpass.getuser(),
        version
    )

    ChannelService().add_new(
        'fontman_free',
        'https://raw.githubusercontent.com/fontman/fms-directory/master/list'
        '.json',
        'github'
    )