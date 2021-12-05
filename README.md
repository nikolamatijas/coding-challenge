# Bidnamic Coding Challange

## Table of Contents
* [General Info](#general-information)
* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [Terminating process](#terminating-process)
* [Limitations](#limitations)
* [Contact](#contact)


## General Information
Bidnamic system ingests search term data from Google Adwords into a S3 Data Lake, one possible
format is CSV. Once ingested, application calculates Return On Ad Spend(ROAS) value for each search term.

`ROAS = conversion value / cost`

Application is implemented as **python daemon** process that:
1. Monitors a directory for new csv files.
2. When a file arrives, parse it and calculate the ROAS for each search term and write out
a new csv file.
3. Output file format :
 
    processed/$currency/search_terms/$timestamp.csv_ of the format:

    _search_term, clicks, cost, impressions, conversion_value, roas_


## Prerequisites
- Python 3.9
- git
- [pip](https://pip.pypa.io/en/stable/)
- [venv](https://docs.python.org/3/library/venv.html)



## Setup(installation and running)

Project runs in own virtual environment isolated from any external influence. All project dependencies are listed in **requirements.txt** located in root directory. 

Execute following steps in order to properly setup project:
1. Ensure that all the prerequisites are met.
2. Clone this repository to your file system.
3. Create new virutal enviroment using _venv_:
    
    `python3.9 -m venv <name_of_virutal_env>`

4. Activate virtual enviroment:

    `source <name_of_virutal_env>/bin/activate`

5. Install project dependencies listed in _requirements.txt_:
    
    `pip install -r requirements.txt`
6. Start process:

    `python3.9 main.py`

Process is now monitoring for new CSV files in directory. Every time when new CSV is created, process will trigger file processing.



## Terminating process

To terminate process open terminal and execute following commands:

1. Find first daemon process _python3.9 main.py_:

    `ps axuw | grep main`

   Output:

   `matijas     8890  4.3  0.7 565412 55312 ?        Sl   12:13   0:00 python3.9 main.py`

   `matijas     8896  0.0  0.0  17672   724 pts/2    S+   12:13   0:00 grep --color=auto main`

2. Kill process using process id. In this example id is 8890.

   `kill 8890`

## Limitations
Project can only run on UNIX based operating system, because for implementation of python daemon process
[python-daemon](https://pypi.org/project/python-daemon/) is used.


## Contact
Created by [Nikola Matijas](nikolamatijas@outlook.com) - feel free to contact me for any questions.
