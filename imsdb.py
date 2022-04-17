from importlib.resources import contents
from xxlimited import new
from bs4 import BeautifulSoup
from numpy import full
import requests
import copy
import csv
import sys
import os

url = "https://imsdb.com/all-scripts.html"

# print(soup.title)


def souper(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup, req.status_code

soup, _ = souper(url)    


index = 1


path, dirs, files = next(os.walk("data/imsdb"))
file_count = len(files)


for link in soup.find_all('a'):
    
    if index <= file_count :
        index = index + 1
        continue
        
    
    if link.get('href').startswith("/Movie"):
        
        movie_link = link.get('href')
        
        movie_name = None
        
        try:
            movie_name = movie_link.split("/")[2].split("Script")[0].strip()
        except:
            
            continue
        
        movie_name = movie_name.replace(" ","-")
        full_url = "https://imsdb.com/scripts/"+movie_name+".html"
        
        # print(full_url)
        sub_soup, status_code = souper(full_url)
        
        
        
        if status_code == 200:
            content = sub_soup.find("td", class_="scrtext")         
            
            print(" ********************************* ", full_url)
            # print(content("tr")[-1]("td")[1].find_all('a'))
            
            
            try:
                content("tr")[-1]("td")[1].find_all('a')
            except:
                continue
            
            if content("tr")[-1]("td")[1].find_all('a') is not None:
                # print(">>")

                last_row = None
                
                try:
                    last_row = content("tr")[-1]("td")[1].find_all('a')
                except:
                    continue
                
                c = [i.get_text() for i in last_row]
                c.pop(0)
                c.pop(-1)
                
                if len(c[0].split(" ")) > 1:
                    c.pop(0)
                
                if len(c[0].split(" ")) > 1:
                    c.pop(0)
                    
                if len(c[0].split(" ")) > 1:
                    c.pop(0)
                
                if len(c[0].split(" ")) > 1:
                    c.pop(0)
            
                
                print(c)
                
            content.find('table').decompose()
            content.find('div').decompose()
            

            c.insert(0, str(index))
    
            with open(r'sheet/imsdb.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(c)
                
        
                
            f = open("data/imsdb/"+str(index) + ".txt", "w")
            f.write(content.get_text())
            f.close()
            
            # print(content)
            # print(str(index))
            index = index + 1
            
    print(" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Done : " + str(index))
print("<<><><><><>  Done")