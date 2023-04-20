import re
import requests
from lxml import etree

urls = "http://book.sbkk8.com/gudai/gudaiyishu/bencaogangmu/2.html"
str1 = "http://book.sbkk8.com/gudai/gudaiyishu/bencaogangmu/"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"}

url = []
for i in range(757, 2, -1):
    url.append(str1 + str(i) + ".html")

response = []
result = []
Note = open('data/CMM.txt', mode='w', encoding='UTF-8')
for i in range(len(url)):
    response.append(i)
    response[i] = requests.get(url[i]).content.decode("GBK")
    html = etree.HTML(response[i])
    result.append(html.xpath('//div[@id="maincontent1"]/h1/text() | //div[@id="maincontent1"]/div//p/text()'))
    result[i][0] = ''.join(re.findall('[^(\xa0)]', result[i][0]))
    result[i][len(result[i]) - 1] = "".join(re.findall('[^(\xa0)]', result[i][len(result[i]) - 1]))
    str2 = ''.join(result[i])
    Note.write(str2 + '\n')

Note.close()
print("successful!")

