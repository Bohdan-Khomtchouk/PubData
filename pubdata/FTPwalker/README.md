[![Build Status](https://travis-ci.org/Bohdan-Khomtchouk/FTPwalker.svg?branch=master)](https://travis-ci.org/Bohdan-Khomtchouk/FTPwalker)
[![Open Source Love](https://badges.frapsoft.com/os/gpl/gpl.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![PyPI version](https://badge.fury.io/py/FTPwalker.svg)](https://badge.fury.io/py/FTPwalker)

# FTPwalker

`FTPwalker` is a Python package for optimally traversing extremely large FTP directory trees.  It constitutes the algorithmic heart of the [PubData](https://github.com/Bohdan-Khomtchouk/PubData) search engine.  FTPwalker creates a dictionary formatted as a JSON file in the user’s home directory containing all the full paths as keys and the respective filenames as values.  FTPwalker is designed with speed in mind by utilizing state-of-the-art high performance parallelism and concurrency algorithms to traverse FTP directory trees.  The resultant hash table (i.e., dictionary) supports fast lookup for any file in any biological database.


## Funding

`FTPwalker` is financially supported by the United States Department of Defense (DoD) through the National Defense Science and Engineering Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering Graduate (NDSEG) Fellowship, 32 CFR 168a.

## Screenshots

<img width="495" alt="screen shot 2016-09-05 at 2 24 14 pm" src="https://cloud.githubusercontent.com/assets/9893806/18255169/893a6ffc-7374-11e6-99fa-4569fc247629.png">
=======
