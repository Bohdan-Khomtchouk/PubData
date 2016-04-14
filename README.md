# PubData

## About

PubData is a genomics search engine and file retrieval system for all bioinformatics databases worldwide.  PubData searches biomedical FTP data in a user-friendly fashion similar to how PubMed searches biomedical literature.  PubData is hosted as a standalone GUI software program, while PubMed is hosted as an online web server.  PubData is built on novel network programming and natural language processing algorithms that can patch into the FTP servers of any user-specified bioinformatics database, query its contents, and retrieve files for download.

Future plans include adding web server support for PubData, and contributions from the open source community are welcome.

PubData is designed as a graphical user interface (GUI) software program written in the Python programming language and PySide (Python binding of the cross-platform GUI toolkit Qt).  PubData can remotely search, access, view, and retrieve files from the deeply nested directory trees of any major bioinformatics database via a local computer network.  

By assembling all major bioinformatics databases under the roof of one software program, PubData allows the user to avoid the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using an Internet browser.  More importantly, it allows a user to query multiple databases simultaneously for user-specified keywords (e.g., `human`, `cancer`, `transcriptome`).  As such, PubData allows researchers to search, access, view, and download files from the FTP servers of any major bioinformatics database directly from one centralized location.  By using only a GUI, PubData allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the comfort of their local computer.

PubData is an ongoing bioinformatics software project financially supported by the United States Department of Defense (DoD) through the National Defense Science and Engineering Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering Graduate (NDSEG) Fellowship, 32 CFR 168a.

Please cite: "Khomtchouk et al.: 'PubData: genomics search engine for bioinformatics databases', 2016 (in preparation)" within any source that makes use of any methods inspired by PubData.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Installation

### Requirements

* Python >= 2.7

## Screenshots

When you open PubData, first pick a bioinformatics database to login to:

![screenshot1](https://cloud.githubusercontent.com/assets/9893806/14540544/9ed860c2-0253-11e6-93e7-77ffd2a934d4.png)
![screenshot2](https://cloud.githubusercontent.com/assets/9893806/14540546/a15c2b62-0253-11e6-9753-3cf1005e6dad.png)

If your favorite bioinformatics database is not yet in the list, just add it yourself:

![screenshot4](https://cloud.githubusercontent.com/assets/9893806/14540549/a59546aa-0253-11e6-8812-31a245561517.png)
![screenshot5](https://cloud.githubusercontent.com/assets/9893806/14540551/a705302c-0253-11e6-96b7-cb5f8808e4fa.png)

If you want to search multiple existing databases simultaneously, tick the respective checkboxes and then click the “Smart search” feature (e.g., search for *Homo sapiens* files):

![screenshot3](https://cloud.githubusercontent.com/assets/9893806/14540548/a46a199a-0253-11e6-892c-927bb9395530.png)
![screenshot6](https://cloud.githubusercontent.com/assets/9893806/14540552/a8bddedc-0253-11e6-984f-2a4c96c55223.png)

Browse the most relevant results and download your file:

![screenshot7](https://cloud.githubusercontent.com/assets/9893806/14540557/ac0dd15a-0253-11e6-98b3-3c9b770370dd.png)
![screenshot8](https://cloud.githubusercontent.com/assets/9893806/14540559/ae5bbee0-0253-11e6-9b9e-4eeae47752ef.png)



