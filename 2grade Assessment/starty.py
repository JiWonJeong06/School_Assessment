import urllib.request, serial
from bs4 import BeautifulSoup
from urllib import parse
from dust import speak

s = serial.Serial("COM7", 128000)

air = input('어느 지역의 미세먼지를 알아 보고 싶나요?: ')
hdr = {'User-Agent' : 'Mozilla/5.0'}
url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query='+ parse.quote_plus(air +' 미세먼지')
req = urllib.request.Request(url, headers=hdr)
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')
try:
    air_num = soup.find("span",class_="num _value").get_text()
    for i in range(1,5):
        try:
            ultra_num = soup.find("div",class_="state_info _ultrafine_dust _info_layer").find("div", class_=f"grade level{i} _level").find("span", class_="num _value").get_text()
            aiair = air_num ; aiultra = ultra_num
            s.write((air_num+"\n").encode())
            s.write((ultra_num+"\n").encode())
            print(f'{air}: 미세먼지: {aiair}, 초미세먼지: {aiultra}')
            speak(f'{air} 미세먼지는 {aiair}, 초미세먼지: {aiultra}')
        except: 
            continue
    
except:
    print(f'"{air}"에 대한 정보가 없습니다.') 

