# Bidnamic Coding Challenge

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
2. When a file arrives, parses it and calculates the ROAS for each search term and writes out
a new csv file.
3. Output file format :
 
    processed/$currency/search_terms/$timestamp.csv_ of the format:

    _search_term, clicks, cost, impressions, conversion_value, roas_

Besides the three main functionalities, the process also tracks all the important events and logs into the file logs.log. It validates the CSV files and their corresponding columns in a way that if a file itself is corrupted or if any of the columns which are mandatory for the output do not exist, the process will not calculate the ROAS. In case of corrupted rows (data), the process will clean up the data by itself.

## Prerequisites
- Python 3.9
- git
- [pip](https://pip.pypa.io/en/stable/)
- [venv](https://docs.python.org/3/library/venv.html)



## Setup

Project runs in its own virtual environment isolated from any external influence. All project dependencies are listed in **requirements.txt** located in root directory. 

Execute following steps in order to properly setup project:
1. Ensure that all the prerequisites are met.
2. Clone this repository to your file system.
3. Create a new virutal enviroment using _venv_:
    
    `python3.9 -m venv <name_of_virutal_env>`

4. Activate the virtual enviroment:

    `source <name_of_virutal_env>/bin/activate`

5. Install project dependencies listed in _requirements.txt_:
    
    `pip install -r requirements.txt`
6. Start process:

    `python3.9 main.py`

Alternatively, instead of running process from source code, you can install roas-calculator package with command:

     pip install .

While running, process constantly monitors for new CSV files in the directory. Every time a new CSV is created, process will trigger file processing and ROAS calculation.



## Terminating process

To terminate process, open terminal and execute the following commands:

1. Find the daemon process _python3.9 main.py_:

    `ps axuw | grep main`

   Output Example:

   `matijas     8890  4.3  0.7 565412 55312 ?        Sl   12:13   0:00 python3.9 main.py`

   `matijas     8896  0.0  0.0  17672   724 pts/2    S+   12:13   0:00 grep --color=auto main`

2. Kill the process using process id. In this example id is 8890.

   `kill 8890`

## Limitations
Project can only run on UNIX based operating system, because [python-daemon](https://pypi.org/project/python-daemon/) package is used for implementation of python daemon process.


## Contact
Created by [Nikola Matijas](nikolamatijas@outlook.com) - feel free to contact me for any questions.
