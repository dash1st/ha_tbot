import time
import telepot
import os
import json
import subprocess
import requests
import urllib
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
from collections import OrderedDict
from telepot.loop import MessageLoop 
from telepot.loop import OrderedWebhook
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton 



import datetime
from threading import Thread
from queue import Queue

import cv2

class Camera:
    def __init__(self, url , mirror=False):
        self.data = None
        #self.cam = cv2.VideoCapture(0) #로컬 카메라 연결
        self.cam = cv2.VideoCapture(url)

        self.WIDTH = 640
        self.HEIGHT = 480

        self.center_x = self.WIDTH / 2
        self.center_y = self.HEIGHT / 2
        self.touched_zoom = False

        self.scale = 1
        self.__setup()

        self.recording = False

        self.mirror = mirror

    def __setup(self):
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        time.sleep(2)

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()


    def save_picture(self):
        print('aaa')
    # 이미지 저장하는 함수
        ret, img = self.cam.read()
        if ret:
            now = datetime.datetime.now()
            date = now.strftime('%Y%m%d')
            hour = now.strftime('%H%M%S')
            user_id = '00001'
            #filename = './images/cvui_{}_{}_{}.png'.format(date, hour, user_id)
            filename = './images/temp.png'
            cv2.imwrite(filename, img)
            #self.image_queue.put_nowait(filename)



### CCTV CAPTURE CLASS END ###


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

InfoMsg = "아래의 요청 중 하나를 고르고 번호를 입력하세요.\n" \
          "1 : CCTV 화면 캡쳐\n" \
          "2 : 환율 확인\n" \
          "3 : 날씨 확인\n" \
          "4 : 미세먼지 확인\n" \
		  "5 : 인도 코로나 NEWS 확인\n" \
          "6 : 보안 NEWS 확인\n" \
          "/사진보내 : 윤서지현 사진을 보냅니다\n" \
          "9 : 종료"

# 1. 집안 사진
def get_cctv_pic(chat_id, url):
    print(url)
#    os.system('capture.py')
#    subprocess.call('python capture.py') 

    bot.sendMessage(chat_id, '오래걸릴 예정이니 잠시만 기다려주세요')
    cam = Camera(url,mirror=True)
    cam.save_picture()

    filepath = 'D:/python_project/git/telebot/images/temp.png'

    time.sleep(10)
    #bot.sendDocument(id,open(filepath,'rb')) # 모든 파일 가능
    bot.sendPhoto(chat_id, open(filepath,'rb')) # 사진만 가능

# 2. 환율 반환
def get_inr_krw():
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWINR'
    exchange =requests.get(url, headers=headers).json()
    return exchange[0]['basePrice']

# 3. 날씨 확인
apiurl = 'http://api.openweathermap.org/data/2.5/weather?q='
apikey = '&APPID=bc36bd2717c588f98d887f0c0025db13'
city = 'gurgaon'    
def weather(id,city):
    url = urllib.request.urlopen(apiurl + city + apikey)
    apid = url.read()
    data = json.loads(apid)
    cityname = data['name']
    weather = data['weather'][0]['main']
    temp = int(data['main']['temp'] - 273.15)
    weathermsg = cityname+': '+weather+' \nTemp :'+str(temp)+'˚C'
    bot.sendMessage(id, weathermsg)


# 4. 미세먼지 확인
# 스크래핑 : https://aqicn.org/city/india/gurugram/sector-51/
def AQI(id):
    response = urlopen('https://aqicn.org/city/india/gurugram/sector-51/')
    soup = BeautifulSoup(response, 'html.parser')
    aqi = soup.select("[id=aqiwgtvalue]")
    bot.sendMessage(id, aqi[0].text)

## 집안 미세먼지.
#   data=os.bin(./wideq-asdklfjas/python example.py -c KR -l ko-KR mon d286d780-7149-11d3-80f8-203dbd8d44ce)
#    result = subprocess.check_output('D:/python_project/wideq_gugu_patch/example.py', shell=True)
#    proc = subprocess.Popen('D:/python_project/wideq_gugu_patch/example.py', stdout=subprocess.PIPE)
#    out, err = proc.communicate()
#    bot.sendMessage(id, result)

# 5. 삼성전자 뉴스
#https://home.openweathermap.org/ dash1st/tkfkqhwk
# 서치 키워드
search_word = '인도 코로나'

# 기존에 보냈던 링크를 담아둘 리스트
old_links = []


# 스크래핑 함수 
def extract_links(old_links=[]):
    url = f'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_jum&query={search_word}'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select_one('#news_result_list')
    news_list = search_result.select('.bx > .news_wrap > a')

    links = []
    for news in news_list[:5]:
        link = news['href']
        links.append(link)
    
    new_links=[]
    for link in links:
        if link not in old_links:
            new_links.append(link)
    
    return new_links

# 이전 링크를 매개변수로 받아서, 비교 후 새로운 링크만 출력
# 차후 이 부분을 메시지 전송 코드로 변경하고 매시간 동작하도록 설정
# 새로운 링크가 없다면 빈 리스트 반환
#for i in range(1):
#    new_links = extract_links(old_links)
#    print('===보낼 링크===\n', new_links,'\n')
#    old_links += new_links.copy()
#    old_links = list(set(old_links))

# 텔레그램 메시지 전송 함수
def send_links(id):
    global old_links
    new_links = extract_links(old_links)
    if new_links:
        for link in new_links:
            bot.sendMessage(chat_id=id, text=link)
    else:
        bot.sendMessage(chat_id=id, text='새로운 뉴스 없음')
    old_links += new_links.copy()
    old_links = list(set(old_links))


## 인도 코로나 뉴스 끝 


# 6. 보안 뉴스 스크립트
def Site_ON(id):
    search = parse.urlparse('https://www.boannews.com/search/news_list.asp?search=title&find=%C3%EB%BE%E0%C1%A1')
    query = parse.parse_qs(search.query)
    S_query = parse.urlencode(query, encoding='UTF-8', doseq=True)
    url = "https://www.boannews.com/search/news_list.asp?{}".format(S_query)

    time.sleep(1)

    news_link = []
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', href=True):
        notices_link = link['href']
        if '/media/view.asp?idx=' in notices_link:
            news_link.append(notices_link)

    news_link = list(OrderedDict.fromkeys(news_link))

    time.sleep(1)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    temp = []
    cnt = 0
    with open(os.path.join(BASE_DIR, 'compare.txt'), 'r')as f_read:
        before = f_read.readlines()
        before = [line.rstrip() for line in before] #(\n)strip in list

        f_read.close()
        for i in news_link:
            if i not in before:
                temp.append(i)
                cnt = cnt + 1
                with open(os.path.join(BASE_DIR, 'compare.txt'), 'a') as f_write:
                    f_write.write(i+'\n')
                    f_write.close()
        if cnt > 0:

            NEW = "[+] Security News 'vulu' NEWS no. {}.".format(cnt)
            bot.sendMessage(chat_id=id, text=NEW)
            for n in temp:
                Main_URL = "https://www.boannews.com{}" .format (n.strip())
                bot.sendMessage(chat_id=id, text=Main_URL)

                response = requests.get(Main_URL)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.find_all("div",{"id":"news_title02"})
                contents = soup.find_all("div",{"id":"news_content"})
                date = soup.find_all("div",{"id":"news_util01"})
                photos = soup.find_all("div",{"class":"news_image"})
                for n in contents:
                    text = n.text.strip()
        else:
            bot.sendMessage(chat_id=id, text='새로운 뉴스 없음')



def on_chat_message(msg):  
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, 'start.')
    if content_type == 'text':
        if msg['text'] == '1':
            bot.sendMessage(chat_id, '집안사진를 확인합니다.')


            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                           [InlineKeyboardButton(text='거실-쇼파앞', callback_data='url1')],
                           [InlineKeyboardButton(text='부엌', callback_data='url2')],
                           [InlineKeyboardButton(text='안방', callback_data='url3')],
                           [InlineKeyboardButton(text='현관', callback_data='url4')],
                           [InlineKeyboardButton(text='아야', callback_data='url5')],
                           [InlineKeyboardButton(text='놀이방', callback_data='url6')],
                           [InlineKeyboardButton(text='DEN', callback_data='url7')],
                           [InlineKeyboardButton(text='로비', callback_data='url8')],
                           [InlineKeyboardButton(text='거실-쇼파뒤', callback_data='url9')]
                       ])

            bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)
        elif msg['text'] == '2':
            bot.sendMessage(chat_id, '인도 환율을 확인합니다.')
            CURRENCY = "오늘의 인도환율 : {}".format(get_inr_krw())
            bot.sendMessage(chat_id, CURRENCY)
            bot.sendMessage(chat_id, InfoMsg)
        elif msg['text'] == '3':
            bot.sendMessage(chat_id, '날씨를 확인합니다.')
            weather(chat_id,city)
            bot.sendMessage(chat_id, InfoMsg)
        elif msg['text'] == '4':
            bot.sendMessage(chat_id, '미세먼지를 확인합니다.')
            AQI(chat_id)
            bot.sendMessage(chat_id, InfoMsg)
        elif msg['text'] == '5':
            bot.sendMessage(chat_id, '인도 코로나 NEWS를 확인합니다.')
            send_links(chat_id)
            bot.sendMessage(chat_id, InfoMsg)
        elif msg['text'] == '6':
            bot.sendMessage(chat_id, '보안 NEWS를 확인합니다.')
            Site_ON(chat_id)
            bot.sendMessage(chat_id, InfoMsg)
        elif msg['text'] == '9':
            bot.sendMessage(chat_id, 'Bye~')
            os._exit(1)
        elif msg['text'] == '/사진보내':
            filepath = 'Y:/5_윤서현 윤지현/사진/Camera/20180925_175836.jpg'
            bot.sendMessage(chat_id, '알겠다 오래 걸릴예정 기달려~')
#           bot.sendDocument(id,open(filepath,'rb')) # 모든 파일 가능
            bot.sendPhoto(chat_id, open(filepath,'rb')) # 사진만 가능
            bot.sendMessage(chat_id, InfoMsg)             
        else:
            bot.sendMessage(chat_id, InfoMsg)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')
    if query_data == 'url1':
        bot.sendMessage(from_id,'거실-쇼파앞 사진을 보냅니다.')
        url = "rtsp://admin:YLWMWP@192.168.0.6:554/h264_stream"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 
    elif query_data == 'url2':
        bot.sendMessage(from_id,'부엌 사진을 보냅니다.')
        url = "rtsp://admin:CTMMRN@192.168.0.4:554/h264_stream"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 
    elif query_data == 'url3':
        bot.sendMessage(from_id,'안방 사진을 보냅니다.')
        url = "rtsp://admin:UVSOFQ@192.168.0.2:554/h264_stream"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 
    elif query_data == 'url4':
        bot.sendMessage(from_id,'현관 사진을 보냅니다.')
        url = "rtsp://admin:GILSMS@192.168.0.5:554/h264_stream"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 
    elif query_data == 'url5':
        bot.sendMessage(from_id,'아야현관 사진을 보냅니다.')
        url = "rtsp://admin:FQQFRP@192.168.1.33:554/h264_stream"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 
    elif query_data == 'url6':
        bot.sendMessage(from_id,'놀이방 사진을 보냅니다.')
        url = "rtsp://admin:VXJMGX@192.168.0.8:554/h264_stream"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 
    elif query_data == 'url7':
        bot.sendMessage(from_id,'DEN 사진을 보냅니다.')
        url = "rtsp://admin:GVBMFH@192.168.0.11:554/h264_stream"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 
    elif query_data == 'url8':
        bot.sendMessage(from_id,'로비 사진을 보냅니다.')
        url = "rtsp://admin:alwjd713@192.168.0.21"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 
    else: 
        bot.sendMessage(from_id,'거실-쇼파뒤 사진을 보냅니다.')
        url = "rtsp://admin:GBVNVA@192.168.0.10:554/h264_stream"
        get_cctv_pic(from_id, url)
        bot.sendMessage(from_id, InfoMsg) 

TOKEN = "1232357351:AAH6fwSyjpvXHC63279YUoLMeKkwEWhFVO8"


bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

#webhook = OrderedWebhook(bot, handle).run_as_thread()
print('LISTENING')

## 초기 봇 시작 환영 메시지
#미정 chat id   nfgfbgngb
bot.sendMessage('910651690', 'BOT 이 시작했습니다.')
bot.sendMessage('910651690', InfoMsg)
#영선 chat id
#bot.sendMessage('438787080', 'BOT 이 시작했습니다.')
#bot.sendMessage('438787080', InfoMsg)
while 1: 
    time.sleep(10)