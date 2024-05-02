
# Python PathFinder


## Prerequisites 
- The file files.txt must be in the same directory as the code.
- The file files.txt must contain a list of graph file names, one per line.

## Introduction
- Execute the code.
- Select the desired graph file name by entering the corresponding number.
- Enter the desired number of random distance tests.
- Enter the desired time tolerance for the test to fail to yield results in seconds.
- The code will then perform N-tests on two random points using 5 different types of algorithms. The results of the tests will be appended to an Excel spreadsheet (.xlsx).

>_Observation: Both .gr and .co must have the same name before the extension format. Example: graph.gr and graph.co_

## Python Dependencies
- openpyxl
- psutil

## To install the dependencies, run the following command

```bash
pip install openpyxl psutil
```

## Running the code

```bash
python main.py
```

## All graphs were taken from
[diag.uniroma1.it](http://www.diag.uniroma1.it/~challenge9/download.shtml)