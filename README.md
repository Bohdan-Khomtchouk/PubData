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

![main-window](https://cloud.githubusercontent.com/assets/9893806/13992741/a86270a4-f0f3-11e5-903d-8bcac9127cc0.png)
![edit-servers](https://cloud.githubusercontent.com/assets/9893806/13992743/aa6d227c-f0f3-11e5-865b-1fad5568c24a.png)
![write-the-keyword-for-search](https://cloud.githubusercontent.com/assets/9893806/13992748/ae49899e-f0f3-11e5-96a9-65392fddbb24.png)
![search-result](https://cloud.githubusercontent.com/assets/9893806/13992773/c0d094f4-f0f3-11e5-8672-20cf9e8573e2.png)
![openning-a-path-from-serach-resutl](https://cloud.githubusercontent.com/assets/9893806/13992781/c6efae92-f0f3-11e5-9bc9-e71b518db14e.png)
![select-server-names-for-search](https://cloud.githubusercontent.com/assets/9893806/13992790/cf336c60-f0f3-11e5-8542-ee169271d487.png)
