
import time
import telepot
import os
import json
import requests
import urllib
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
from collections import OrderedDict

InfoMsg = "아래의 요청 중 하나를 고르고 번호를 입력하세요.\n" \
          "1 : CCTV 화면 캡쳐\n" \
          "2 : 환율 확인\n" \
          "3 : 날씨 확인\n" \
          "4 : 미세먼지 확인\n" \
		  "5 : 삼성전자 NEWS 확인\n" \
          "6 : 보안 NEWS 확인\n" \
          "/사진보내 : 윤서지현 사진을 보냅니다\n" \
          "9 : 종료"

status = True

# 텔레그램 봇 생성

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
genietoken= "1232357351:AAH6fwSyjpvXHC63279YUoLMeKkwEWhFVO8"
bot = telepot.Bot(genietoken)


# 4. 미세먼지 확인
# 스크래핑 : https://aqicn.org/city/india/gurugram/sector-51/
def AQI(id):
    response = urlopen('https://aqicn.org/city/india/gurugram/sector-51/')
    soup = BeautifulSoup(response, 'html.parser')
    aqi = soup.select("[id=aqiwgtvalue]")
    bot.sendMessage(id, aqi[0].text)
## 집안 미세먼지.
    data = example(./wideq-asdklfjas/python example.py -c KR -l ko-KR mon d286d780-7149-11d3-80f8-203dbd8d44ce)
#   print data

def handle(msg):
    content, chat, id = telepot.glance(msg)
#    print(content, chat, id)  # 텔레그램에 입력되는 메세지의 타입, 채팅 타입, 메세지 송신 ID
    city = 'gurgaon'
    if content == 'text':
        if msg['text'] == '1':
            bot.sendMessage(id, '주가를 확인합니다.')
            bot.sendMessage(id, InfoMsg)
        elif msg['text'] == '2':
            bot.sendMessage(id, '인도 환율을 확인합니다.')
            CURRENCY = "오늘의 인도환율 : {}".format(get_inr_krw())
            bot.sendMessage(id, CURRENCY)
            bot.sendMessage(id, InfoMsg)
        elif msg['text'] == '3':
            bot.sendMessage(id, '날씨를 확인합니다.')
            weather(id,city)
            bot.sendMessage(id, InfoMsg)
        elif msg['text'] == '4':
            bot.sendMessage(id, '미세먼지를 확인합니다.')
            AQI(id)
            bot.sendMessage(id, InfoMsg)
        elif msg['text'] == '5':
            bot.sendMessage(id, '삼성전자 NEWS를 확인합니다.')
            send_links(id)
            bot.sendMessage(id, InfoMsg)
        elif msg['text'] == '6':
            bot.sendMessage(id, '보안 NEWS를 확인합니다.')
            Site_ON(id)
            bot.sendMessage(id, InfoMsg)
        elif msg['text'] == '9':
            bot.sendMessage(id, 'Bye~')
            os._exit(1)
        elif msg['text'] == '/사진보내':
            filepath = 'Y:/5_윤서현 윤지현/사진/Camera/20180925_175836.jpg'
            bot.sendMessage(id, '알겠다 오래 걸릴예정 기달려~')
#           bot.sendDocument(id,open(filepath,'rb')) # 모든 파일 가능
            bot.sendPhoto(id, open(filepath,'rb')) # 사진만 가능
            bot.sendMessage(id, InfoMsg)     
        else:
            bot.sendMessage(id, InfoMsg)

bot.message_loop(handle)

while status == True:
    time.sleep(10)