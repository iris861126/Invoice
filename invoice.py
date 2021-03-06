# coding=utf8
from __future__ import unicode_literals, print_function
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import numpy as np

# Part 1: 由財政部官網爬取本期及上期之發票中獎號碼並印出
pages = ["index.html","lastNumber.html"]  # 本期及上期分頁

for i in range(2):
    # 財政部官網
    request_url = 'http://invoice.etax.nat.gov.tw/{}'.format(pages[i]) 
    
    # 取得HTML
    htmlContent = urllib.request.urlopen(request_url).read()
    soup = BeautifulSoup(htmlContent, "html.parser")
    
    results = soup.find_all("p", class_="etw-tbiggest")
    for j in range(len(results)):
        results[j] = results[j].text.strip()
            
    if i==0:
        month_now = soup.find_all('a', {'class':"etw-on", 'href':pages[i]})[0].text
        num_now = {
            "特別獎": results[0],
            "特獎": results[1],
            "頭獎": results[2:5]
        }
        print ("本期統一發票開獎號碼 ({0})：".format(month_now[:-5]))
        print(num_now)
    
    else:
        month_last = soup.find_all('a', {'class':"etw-on", 'href':pages[i]})[0].text
        num_last = {
            "特別獎": results[0],
            "特獎": results[1],
            "頭獎": results[2:5]
        }
        print ("上期統一發票開獎號碼 ({0})：".format(month_last[:-5]))
        print(num_last)

#%% Part 2: 對發票
conti = 'y'
while conti == 'y':
    # 選擇期數
    mon = '0'
    del mon
    mon = input('選擇欲查詢之月份(請輸入1或2): \n1){0}(本期); 2){1}(上期)\n'.format(month_now[:-5],month_last[:-5]))
    while (mon.isdigit()==False or len(mon)!=1 or (int(mon)!=1 and int(mon)!=2)):
        mon = input("輸入錯誤！選擇欲查詢之月份(請輸入1或2): \n1){0}(本期); 2){1}(上期)\n".format(month_now[:-5],month_last[:-5]))
    
    if (mon.isdigit() and len(mon)==1 and (int(mon)==1 or int(mon)==2)):
        if (int(mon) == 1):
            print("您欲查詢之月份為：{0}{1}".format(month_now[:-5],' (本期)'))
        else:
            print("您欲查詢之月份為：{0}{1}".format(month_last[:-5],' (上期)'))
    
    conti_mon = 'y' # 繼續該期查詢
    while conti_mon == 'y':
        # 輸入欲查詢之發票號碼
        num = '0'
        del num
        num = input("請輸入欲查詢之發票號碼(共8碼)：\n")    
        while (num.isdigit()==False or len(num)!=8):
            num = input("輸入錯誤！請輸入欲查詢之發票號碼(共8碼)：\n")
        
        if (num.isdigit() and len(num)==8):
            print("您欲查詢之發票號碼為：{}".format(num))
        
        # 發票獎項查詢
        if int(mon) == 1: # 本期
            others = True  # 其餘獎項
            if num == num_now['特別獎']:
                print("恭喜中了特別獎!")
            elif num == num_now['特獎']:
                print("恭喜中了特獎!")
            elif num in num_now['頭獎']:
                print("恭喜中了頭獎!")
            elif others:  # 其餘獎項
                prize = ['二獎','三獎','四獎','五獎','六獎']
                for i in range(5):
                    wins = num_now['頭獎'].copy()
                    for j in range((len(wins))):
                        wins[j] = wins[j][i+1:]
                    if num[i+1:] in wins:
                        print("恭喜中了{}!".format(prize[i]))  
                        break
                    if i == 4:
                        print("沒中!") 
                        
        elif int(mon) == 2: # 上期
            others = True  # 其餘獎項
            if num == num_last['特別獎']:
                print("恭喜中了特別獎!")
            elif num == num_last['特獎']:
                print("恭喜中了特獎!")
            elif num in num_last['頭獎']:
                print("恭喜中了頭獎!")
            elif others: # 其餘獎項
                prize = ['二獎','三獎','四獎','五獎','六獎']
                for i in range(5):
                    wins = num_last['頭獎'].copy()
                    for j in range((len(wins))):
                        wins[j] = wins[j][i+1:]
                    if num[i+1:] in wins:
                        print("恭喜中了{}!".format(prize[i]))
                        break
                    if i == 4:
                        print("沒中!") 

        conti_mon = input("是否繼續\"該期\"查詢？ (y/n)\n")
    conti = input("是否繼續查詢？ (y/n)\n")
