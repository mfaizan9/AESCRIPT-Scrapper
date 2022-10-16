import requests
import json
from bs4 import BeautifulSoup
import pandas as pd 
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm.notebook import tqdm
from tqdm import tqdm as tqdm2
from tqdm.contrib.concurrent import thread_map

Total_Data = []
categories_links = []
category_name = []
Product_Links = []

def get_data(url):
    r = requests.get(url).text
    soup = BeautifulSoup(r , 'lxml')
    # Title
    title = soup.find('h1' , {'itemprop':'name'}).text.strip()
    
    # Description
    description = soup.select_one('#product_tabs_description_contents').div
    for t in description.select('style'):
        t.extract()
    description = description.contents
    description = ''.join(map(str, description)).replace('’', "'")
    # Image Link
    image_link = soup.find('img' , {'id':'image'})['src']
    # Video Link
    try:
        Video_Link = ''
        video_div = soup.find_all('a')
        for a in video_div:
            try:
                ytlink = a['href']
                if 'youtube' in ytlink and 'watch' in ytlink:
                    Video_Link = ytlink
            except:
                Video_Link = ''
    except:
        Video_Link = ''


    data = {
        'Product Title': title,
        'Product Link': url,
        'Description': description,
        'Image Preview Link': image_link,
        'Video Preview Link': Video_Link
    }

    Total_Data.append(data)

    return

def category():
    url = 'https://aescripts.com/'
    r = requests.get(url).text
    soup = BeautifulSoup(r , 'lxml')
    cat_div = soup.find('div' , {'id':'browse-main-categories'})
    ul = cat_div.find('ul')
    lis = ul.find_all('li')
    for i in lis:
        cat_names = i.a.text.strip()
        category_name.append(cat_names)

        cat_link = i.a['href']
        categories_links.append(cat_link)
    return




def getProds(url):
    r = requests.get(url).text
    soup = BeautifulSoup(r , 'lxml')
    atags = soup.find_all('a' , class_='product-link')
    for i in atags:
        prodLinks = i['href']
        Product_Links.append(prodLinks)

    return

print('How do you want to scrape?')
print('\n')
print('1: Category Wise')
print('2: Link Wise')
print('\n')
num = int(input('Enter Number: '))
print('\n')

if num == 1:
    category()
    for i in range(len(category_name)):
        print(f'{i+1}: {category_name[i]}')
    print('\nWhich category do you want to scrape?')
    print('\n')
    n = int(input(f'Enter a Number from 1 to {len(category_name)}: '))
    print('\n')
    # Getting the category link
    p = int(input('How many products do you want to scrape? '))
    L = (p//12)+1
    for x in range(1 , L+1):
        link_index = categories_links[n-1] + f'?p={x}'
        getProds(link_index)
    if p<len(Product_Links):
        actual_Products = Product_Links[0:p]
    elif p>len(Product_Links):
        actual_Products = Product_Links
    elif p == len(Product_Links):
        actual_Products = Product_Links
    else:
        print('You entered a wrong number.......')
    # getting Total Data
    print('\n')
    print('Fetching Products Data')
    thread_map(get_data , actual_Products , max_workers=10)
    df = pd.DataFrame(Total_Data)
    file_name = f"{category_name[n-1]}.csv"
    df.to_csv(file_name , index=False )
    print('\nData Stored to CSV')
    time.sleep(3)            
    
elif num==2:
    LINK = input('Enter the Product Link: ')
    r = requests.get(LINK).text
    soup = BeautifulSoup(r , 'lxml')
    title = soup.find('h1' , {'itemprop':'name'}).text.strip()
    fileName = f'{title}.csv'
    get_data(LINK)
    df = pd.DataFrame(Total_Data)
    df.to_csv(fileName , index=False)
    print('\nData Stored to CSV')
    time.sleep(3)
else:
    print('Incorrect Entry....')





# category function




