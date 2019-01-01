'''
Created on Oct 1, 2018

@author: huangjes
'''
#!usr/bin/python
#coding=gbk
print("hello world!")

import sys
import csv
# import http.cookiejar
import urllib.request
# import requests
from bs4 import BeautifulSoup
cnt=1
# def generate_allurl(user_in_nub):
#     url = 'https://sh.lianjia.com/ershoufang/pg{}/'
#     for url_next in range(1,int(user_in_nub)):
#         yield url.format(url_next)

#access the webpage as specified URL, and return page objects
def access_url(url_addr):
    #url_response=requests.get(url_addr,)
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
    urllib.request.install_opener(opener)
    page = urllib.request.urlopen(url_addr)
    if page.getcode() == 200:
        html = page.read()
        bsobj = BeautifulSoup(html,"html5lib")
        return bsobj
    else:
        print("Page Error!")
        sys.exit()
    
def get_house_info_list(url_addr):
    bsobj = access_url(url_addr)
    if not bsobj:
        return None
    #get pages
    global cnt
#     house_page = bsobj.find("div",{"class":"page-box house-lst-page-box"})#bsobj.find("a",{"gahref":"results_totalpage"})
    house_info_page = 100#int(house_page.get_text())
    #print(house_info_page)
    house_list = bsobj.find_all("div", {"class":"info clear"})
    for  house in house_list:
        url_addr = house.find("div",{"class":"title"}).findChildren("a")[0].get("href")
        print (cnt,"  ", url_addr)
        cnt=cnt+1
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
        urllib.request.install_opener(opener)
        page = urllib.request.urlopen(url_addr)
        if page.getcode() == 200:
            html = page.read()
            curr_house = BeautifulSoup(html,"html5lib")
        else:
            print("Page Error!")
        #get house detail information
        house_info_list=get_house_details(curr_house,url_addr,cnt-1)
        #write information to excel file
        write_house_to_table(house_info_list)    
    return curr_house

def get_house_details(curr_house,url_addr,cnt):
    house_info_list=[]
    house_info_list.append({'cnt':cnt})
    house_info_list.append({'url_addr':url_addr})
    price=curr_house.find("div",{"class":"price"}).findChildren("span")
    total_price=price[0].get_text()
    unit_price=price[3].get_text()[:-4]#remove the last 4 character unit
    house_info_list.append({'total_price':total_price})
    house_info_list.append({'unit_price':unit_price})
    house_introContent=curr_house.find("div",{"class":"introContent"}).find_all("div",{"class":"content"})
    house_base=house_introContent[0].find_all("li")
    house_transaction=house_introContent[1].find_all("li")
    for base_info in house_base:
        house_info_list.append({base_info.get_text()[:4].strip().replace("\n",""):base_info.get_text()[4:].strip().replace("\n","")})
    for base_info in house_transaction:
        house_info_list.append({base_info.get_text().strip().split('\n')[0].strip():base_info.get_text().strip().split('\n')[1].strip()})
#     print('**********************')
    #print(house_info_list)
    #print(len(house_info_list))
    return  house_info_list

def  house_mess(url):
    house_info_list =[]
#     get_house_info_list(url)
    for  i in range(1,100):
        new_url = url +'pg'+str(i)
        get_house_info_list(new_url)
#         house_info_list.extend(get_house_info_list(new_url))
            
            #print(new_url)
        #print(house_info_list)
    #print("****************house_info_list*********************")
    #print(house_info_list)

def write_house_to_table(house_info_list):  
    global file_head_flag
    wirte_flag=file_head_flag
#     worksheet=workbook.add_sheet('house')
    if house_info_list:
#         with open("./house.txt", "a") as f:
#             writer = csv.writer(f)
#             fieldnames=house_info_list[0].keys()
#             writer.writerow(fieldnames)
#             if wirte_flag == 0:
#                 for house_info in house_info_list:
#                     for val in house_info.keys():
#                         f.write(val.strip())
#                         f.write('\t')
#                 print('\r\n')
#             for house_info in house_info_list:
#                 for val in house_info.values():
#                     f.write(val.strip())
#                     f.write('\t')
#             print('\r\n')
        with open("./house.csv", "a", newline='',encoding='utf-8-sig') as f:
            csv_write = csv.writer(f,dialect='excel')
            my_list=[]
            if wirte_flag == 0:
                header_list=[]
                for house_info in house_info_list:
                    for val in house_info.keys():
                        header_list.append(val)
                csv_write.writerow(header_list)
            for house_info in house_info_list:
                for val in house_info.values():
                    my_list.append(val)
            csv_write.writerow(my_list)
            
    file_head_flag=1
#house_mess('http://sh.lianjia.com/ershoufang/minhang')

# def  get_city_dict():
#     city_dict = {}
#     with open('./citys.csv', 'r') as  f:
#         reader =csv.reader(f)
#         for  city in reader:
#             if len(city)>0:
#                 city_dict[city[0]] = city[1]
#     return city_dict
# city_dict = get_city_dict()
#print(city_dict)

def get_district_dict(url_addr):
    district_dict = {}
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
    urllib.request.install_opener(opener)
    page = urllib.request.urlopen(url_addr)
    if page.getcode() == 200:
        html = page.read()
        bsobj = BeautifulSoup(html,"html.parser")
    else:
        print("Page Error!")   
    roles = bsobj.find("div", {"data-role":"ershoufang"}).findChildren("a")
    for role in roles:
        district_url = role.get("href")
        district_name = role.get_text()
        district_dict[district_name] = district_url
    return district_dict

def run():
#     city_dict = get_city_dict("https://sh.lianjia.com/")
#     for city in city_dict.keys():
#         print(city,end=' ')
#     print() 
#     key_city= input("Please input city  ")
#     city_url = city_dict.get(key_city)
#     if city_url:
#         print (key_city, city_url)
#     else:
#         print( "Input error")
#         sys.exit()
    global file_head_flag
    file_head_flag=0
    city_url="https://sh.lianjia.com"  
    ershoufang_city_url = city_url + "/ershoufang"
    print(ershoufang_city_url)
    district_dict = get_district_dict(ershoufang_city_url)
    for district in district_dict.keys():
        print (district,end=' ')
    print()
    
    input_district = input("Please input distract:")
    district_url = district_dict.get(input_district)

    if not district_url:
        print ("Input error")
        sys.exit()
    house_info_url = city_url + district_url
    house_mess(house_info_url)    

run()        
#     if url_response.status_code==200:
#         re_set=re.compile('<li.*?class="clear">.*?<a.*?class="img.*?".*?href="(.*?)"')
#         re_get=re.findall(re_set,  url_response.text)
#         print (re_get)
        
# user_in_nub = input('Please input the total page number:')
# for current_url in generate_allurl(user_in_nub):
#     print(current_url)
#     access_url(current_url)
#     print('done!')