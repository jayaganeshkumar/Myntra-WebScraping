import requests 
import json
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
import time
import urllib3
import csv

urllib3.disable_warnings()



options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

s = requests.Session()

driver = webdriver.Chrome(executable_path=r'D:\chromedriver.exe', options=options)
driver.set_script_timeout(4)

with open("tshirts_{}.csv".format(str(time.strftime('%b-%d-%Y_%H%M', time.localtime()))), "w") as f1:
    writer = csv.writer(f1)
    writer.writerow(['prodURL', 'prodName', 'prodBrand', 'Size Available', 'Price', 'MRP', 'Gender', 'Description', 'prim_img_link', 'sec_img_link'])
    for d in range(1, 201):
        driver.get("https://www.myntra.com/tshirts?f=Categories%3ATshirts&p={}&plaEnabled=false".format(d))

        soup = BeautifulSoup(driver.page_source,"html.parser")

        count = soup.select(".product-base")

        data = []
        m = 0

        for i in count:
            curr = []
            link = i.a["href"]
            link = "https://www.myntra.com/" + link
            curr.append(link)
            data.append(curr)

        read1 = soup.select(".product-productMetaInfo")

        for j in read1:

            itemname = j.select(".product-product")
            itemname = itemname[0].getText()
            data[m].append(itemname)

            name = j.select(".product-brand")
            name = name[0].getText()
            data[m].append(name)

            m += 1

        m = 0
        for i in data:
            var1 = requests.get(i[0], headers=headers, verify=False)
            read = BeautifulSoup(var1.text,"html.parser")
            
            script = None
            s = read.find_all("script")

            for si in s:
                if si.string:
                    if "pdpData" in si.string:
                        script = si.string
                        break

            json_data = json.loads(script[script.index('{'):])

            sizes = []
            size1 = json_data['pdpData']['sizes']
            for i in range(len(size1)):
                if size1[i]['available']:
                    sizes.append(size1[i]['label'])
            data[m].append(sizes)

            price = json_data['pdpData']['price']['discounted']
            data[m].append(price)

            mrp = json_data['pdpData']['price']['mrp']
            data[m].append(mrp)

            gender = json_data['pdpData']['analytics']['gender']
            data[m].append(gender)

            description = json_data['pdpData']['productDetails'][0]['description']
            data[m].append(description)

            prim_img = json_data['pdpData']['media']['albums'][0]['images'][0]['imageURL']
            data[m].append(prim_img)
            
            data[m].append(json_data['pdpData']['media']['albums'][0]['images'])
            m += 1            
            
        writer.writerows(data)
