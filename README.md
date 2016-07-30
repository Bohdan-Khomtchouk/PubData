![pubdatalogo](https://cloud.githubusercontent.com/assets/9893806/16898720/bb487dba-4bb3-11e6-866a-a879942403e3.png)

# PubData

## About

PubData is a genomics search engine and file retrieval system for all bioinformatics databases worldwide.  PubData searches biomedical FTP data in a user-friendly fashion similar to how PubMed searches biomedical literature.  PubData is hosted as a standalone GUI software program, while PubMed is hosted as an online web server.  PubData is built on novel network programming and natural language processing algorithms that can patch into the FTP servers of any user-specified bioinformatics database, query its contents, and retrieve files for download.

Future plans include adding web server support for PubData, and contributions from the open source community are welcome.

PubData is designed as a graphical user interface (GUI) software program written in the Python programming language and PyQt4 (Python binding of the cross-platform GUI toolkit Qt).  PubData can remotely search, access, view, and retrieve files from the deeply nested directory trees of any major bioinformatics database via a local computer network.  

By assembling all major bioinformatics databases under the roof of one software program, PubData allows the user to avoid the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using an Internet browser.  More importantly, it allows a user to query multiple databases simultaneously for user-specified keywords (e.g., `human`, `cancer`, `transcriptome`).  As such, PubData allows researchers to search, access, view, and download files from the FTP servers of any major bioinformatics database directly from one centralized location.  By using only a GUI, PubData allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the comfort of their local computer.

PubData is an ongoing bioinformatics software project financially supported by the United States Department of Defense (DoD) through the National Defense Science and Engineering Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering Graduate (NDSEG) Fellowship, 32 CFR 168a.

Please cite: "Khomtchouk et al.: 'PubData: genomics search engine for bioinformatics databases', 2016 (in preparation)" within any source that makes use of any methods inspired by PubData.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Installation

### Requirements

* Python >= 2.7

### Linux:
* Make sure you have Python 2.7 installed.
* Python libraries needed: PyQt4, PyQt
* Git clone PubData directory.
* Navigate to /interface directory.
* Run “python GUI.py”.
* If you are missing a Python library, it will tell you when running this. 

## Screenshots

![s1_lean](https://cloud.githubusercontent.com/assets/9893806/14683412/9bb0cb6a-06f8-11e6-8e91-1279b9159c57.png)
![s2_lean](https://cloud.githubusercontent.com/assets/9893806/14683417/9f30459a-06f8-11e6-848b-05e695b3f1b4.png)
![s3_lean](https://cloud.githubusercontent.com/assets/9893806/14683424/a764e9dc-06f8-11e6-9a24-d5a20c0c4e14.png)
![s4_lean](https://cloud.githubusercontent.com/assets/9893806/14683425/a8d5b3c8-06f8-11e6-83a0-1e9a6c73544c.png)
![s5_lean](https://cloud.githubusercontent.com/assets/9893806/14683428/ab37473a-06f8-11e6-8231-5d09dc248086.png)

When you open PubData, first pick a bioinformatics database to login to:

![s6_lean](https://cloud.githubusercontent.com/assets/9893806/14683433/b2016ff0-06f8-11e6-813c-a1eccf2a2e30.png)

Logged into PANTHER (Protein ANalysis THrough Evolutionary Relationships) Classification System database:

![s7_lean](https://cloud.githubusercontent.com/assets/9893806/14683441/b53109a6-06f8-11e6-9065-b74e22d51c80.png)

If you don’t see your favorite database in the list, you can manually insert it yourself (convenient for recently published databases):

![s8_lean](https://cloud.githubusercontent.com/assets/9893806/14683444/b73f6f4e-06f8-11e6-80d7-893ca56a16d1.png)
![s9_lean](https://cloud.githubusercontent.com/assets/9893806/14683448/bd1b40c8-06f8-11e6-82a9-0459c6b56c7e.png)

Let’s say you want to "Google search" multiple databases simultaneously:

![s10_lean](https://cloud.githubusercontent.com/assets/9893806/14683452/c080e0c4-06f8-11e6-9c50-4931a31b600d.png)

Keyword search for ChIP-seq files across these selected databases (multiple keywords may be used as well):

![s11_lean](https://cloud.githubusercontent.com/assets/9893806/14683455/c21264d0-06f8-11e6-98cc-6cc74f5b5588.png)

Showing all relevant search results pertaining to ChIP-seq files across all selected databases:

![s13_lean](https://cloud.githubusercontent.com/assets/9893806/14683461/c696bcea-06f8-11e6-8334-37ba00b48b1c.png)

Keyword search for RNA-seq files across these selected databases (multiple keywords may be used as well):

![s12_lean](https://cloud.githubusercontent.com/assets/9893806/14683458/c4601ec6-06f8-11e6-8bb6-3d47a5ebbe3f.png)

Showing all relevant search results pertaining to RNA-seq files (from the selected databases):

![s14_lean](https://cloud.githubusercontent.com/assets/9893806/14683465/cabf7348-06f8-11e6-85f7-2c61a9a12d2c.png)



