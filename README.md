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

![select-server-for-connect](https://cloud.githubusercontent.com/assets/9893806/14414608/b08b9656-ff63-11e5-8764-448dafa0dfbb.png)
![root-directory](https://cloud.githubusercontent.com/assets/9893806/14414613/b427e616-ff63-11e5-9f01-fc42ddaffa73.png)
![edit-servers](https://cloud.githubusercontent.com/assets/9893806/14414614/b9b979dc-ff63-11e5-851d-368825865d2a.png)
![add-keyword-to-search](https://cloud.githubusercontent.com/assets/9893806/14414615/bb88d014-ff63-11e5-9997-7bb2c7188e32.png)
![edit-server-add-new](https://cloud.githubusercontent.com/assets/9893806/14414616/bdbe96e8-ff63-11e5-95f7-9a02444b1474.png)
![edit-server-update-exist-name](https://cloud.githubusercontent.com/assets/9893806/14414618/c2bf7748-ff63-11e5-976a-a4c738474eb3.png)
![result-of-seach](https://cloud.githubusercontent.com/assets/9893806/14414622/c857eab4-ff63-11e5-9982-4280532d3c2d.png)
![open-one-of-the-paths](https://cloud.githubusercontent.com/assets/9893806/14414620/c50dc75c-ff63-11e5-94a3-c5eba96cb501.png)
![downloading-file](https://cloud.githubusercontent.com/assets/9893806/14414624/caefc7ec-ff63-11e5-8a70-f477e07c8d4d.png)
