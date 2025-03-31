from bs4 import BeautifulSoup
import requests
from csv import writer

url = ["https://www.onlinecourserank.com/best-online-course-platforms/",
       "https://www.bitdegree.org/online-learning-platforms",
       "https://www.onlinecoursereport.com/best-online-course-providers/",
       "https://www.learnworlds.com/online-learning-platforms/"]

page1 = requests.get(url[0])
page2 = requests.get(url[1])
page3 = requests.get(url[2])
page4 = requests.get(url[3])
soup1 = BeautifulSoup(page1.content,'html.parser')
soup2 = BeautifulSoup(page2.content,'html.parser')
soup3 = BeautifulSoup(page3.content,'html.parser')
soup4 = BeautifulSoup(page4.content,'html.parser')
lists1 = soup1.find_all('h3')
lists2 = soup2.find_all('div', class_="table-row row m-0 align-items-center")
lists3 = soup3.find_all('h3')
lists4 = soup4.find_all('h3', class_="title-italic")


header=["Rank","Site","Weight"]

#with open('file1.csv', 'w', encoding='utf-8', newline='') as f1:
#    thewriter1 = writer(f1)
#    thewriter1.writerow(header)
#    for list in lists1:
#        rank = lists1.index(list)+1
#        platform_name = list.text.replace('\n','')
#        weight = 1/rank
#        info = [rank,platform_name,weight]
#        thewriter1.writerow(info)

with open('file3.csv','w',encoding="utf-8", newline="") as f2:
    thewriter2 = writer(f2)
    thewriter2.writerow(header)
    for list in lists2:
        rank2 = lists2.index(list)+1
        platform_name2 = list.find(name='a', class_="read-review border-0").text.replace({'\n':'',' Review':''})
        weight2 = 1/(rank2)
        info2 = [rank2,platform_name2,weight2]
        thewriter2.writerow(info2)

#with open('file3.csv','w',encoding='utf-8',newline='') as f3:
#    thewriter3 = writer(f3)
#    thewriter3.writerow(header)
#    for list in lists3:
#        rank3 = lists3.index(list)+1
#        platform_name3 = list.text.replace('\n','')
#        weight3 = 1/rank3
#        info3 = [rank3,platform_name3,weight3]
#        thewriter3.writerow(info3)

#with open('file4.csv','w',encoding='utf-8',newline='') as f4:
#    thewriter4 = writer(f4)
#    thewriter4.writerow(header)
#    for list in lists4:
#        rank4 = lists4.index(list)+1
#        platform_name4 = list.text.replace('\n','')
#        weight4 = 1/rank4
#        info4 = [rank4,platform_name4,weight4]
#        thewriter4.writerow(info4)