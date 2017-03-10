# What is OpenAQ?
https://openaq.org/#/about?_k=n2uisf

## What is this program doing?
Download the csv file of the desired day from Openaq database. It can download all csv files. It can download csv files published as much as daily from desired day.

## How to Use?
Your system should have selenium installed. If it is not installed, you can do automatic installation from here:  
https://github.com/Natgho/Selenium-installerX  

`virtualenv -p python3 env`  
`pip install requirements.txt`  

Download all data:  
`python download.py`  
_All CSV files will download in /data folder._

Download for Until Date:  
`python download.py dd-mm-yyyy`

Merge Downloaded CSV:  
`python download.py merge`