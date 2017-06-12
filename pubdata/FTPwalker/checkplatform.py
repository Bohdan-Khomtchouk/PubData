"""
=====
checkplatform.py
=====

Check the platform type.

============================

"""

import platform


def check():
    """
       Return the platforms name if its one of Linux, Windows or Mac.
       otherwise raise an exception.
    """
    platform_name = platform.system().lower()

    if "linux" in platform_name:
        return "Linux"
    elif "windows" in platform_name:
        return "Windows"
    elif "darwin" in platform_name:
        return "Mac"
    else:
        raise Exception("""Undefined platform. This application has been designed
for any of the Mac, Linux, Windows platforms. And your platform is {}""".format(platform_name))
