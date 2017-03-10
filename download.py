from selenium import webdriver
from pyvirtualdisplay import Display
from time import sleep
from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
import os
import sys
from datetime import datetime, timedelta as td

addresses = OrderedDict()
path = os.getcwd() + "/"


def get_page_source():
    global addresses
    display = Display(visible=0, size=(1024, 768))
    display.start()
    driver = webdriver.Chrome()
    link = "https://openaq-data.s3.amazonaws.com/index.html"
    driver.get(link)
    sleep(10)
    links = driver.page_source
    driver.close()
    display.stop()
    soup = BeautifulSoup(links, "html.parser")
    for a in soup.find_all('a', href=True):
        addresses[a.text] = a['href']


def save_to_data_files():
    global addresses, path
    if not os.path.exists(path + "data"):
        os.makedirs(path + "data")
    for csv_name, address in addresses.items():
        if os.path.isfile(path + "data/" + csv_name):
            print(csv_name + " already downloaded...")
        else:
            print("start download {} file".format(csv_name))
            r = requests.get(address)
            with open(path + "data/" + csv_name, "wb") as code:
                code.write(r.content)

    print("Download Complete!")


def download_one_day(filename):
    global addresses
    print(filename + " downloaded...")
    r = requests.get(addresses[filename])
    with open(path + "data/" + filename, "wb") as code:
        code.write(r.content)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        get_page_source()
        save_to_data_files()
        print("{} CSV files downloaded...".format(len(addresses)))

    elif sys.argv[1] == "untilday":
        get_page_source()
        until_day = sys.argv[2]
        until_day = datetime.strptime(until_day, "%d-%m-%Y")
        today = datetime.strptime(datetime.today().strftime('%d-%m-%Y'), "%d-%m-%Y")
        delta = today - until_day
        file_counter = 0
        for i in range(delta.days + 1):
            file_counter += 1
            tmp_day = until_day + td(days=i)
            tmp_day = tmp_day.strftime("%Y-%m-%d")
            download_one_day(str(tmp_day) + ".csv")
        print("{} files downloaded...".format(file_counter))

    elif sys.argv[1] == "merge":
        csv_list = os.listdir(path + "data/")
        today = datetime.today().strftime('%d-%m-%Y')
        if os.path.isfile(path + "alldata-" + today + ".csv"):
            os.remove(path + "alldata-" + today + ".csv")
        fout = open(path + "alldata-" + today + ".csv", "a")
        for file_name in csv_list:
            for line in open(path + "data/" + file_name):
                fout.write(line)
        fout.close()
        print("{} csv files merged...".format(len(csv_list)))

    elif sys.argv[1] == "onedate":
        get_page_source()
        download_one_day(sys.argv[2] + ".csv")
