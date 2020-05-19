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
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

InfoMsg = "아래의 요청 중 하나를 고르고 번호를 입력하세요.\n" \
          "1 : CCTV 화면 캡쳐\n" \
          "2 : 환율 확인\n" \
          "3 : 날씨 확인\n" \
          "4 : 미세먼지 확인\n" \
		  "5 : 인도 코로나 NEWS 확인\n" \
          "6 : 보안 NEWS 확인\n" \
          "/사진보내 : 윤서지현 사진을 보냅니다\n" \
          "9 : 종료"
InfoMsg2 = "어느 방의 CCTV를 볼까요?.\n" \
          "1 : 거실\n" \
          "2 : 안방\n" \
          "3 : 날씨 확인\n" \
          "4 : 미세먼지 확인\n" \
		  "5 : 인도 코로나 NEWS 확인\n" \
          "6 : 보안 NEWS 확인\n" \
          "/사진보내 : 윤서지현 사진을 보냅니다\n" \
          "9 : 취소"
status = True
updater = Updater(genietoken)
# 1. 집안 사진
def get_cctv_pic(id):
    
    os.system('capture.py')

    filepath = 'D:/python_project/images/temp.png'
    bot.sendMessage(id, '알겠다 거실사진 보낼께 오래 걸릴예정 기달려~')
    time.sleep(10)
    #bot.sendDocument(id,open(filepath,'rb')) # 모든 파일 가능
    bot.sendPhoto(id, open(filepath,'rb')) # 사진만 가능

# 2. 환율 반환
def get_inr_krw():
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWINR'
    exchange =requests.get(url, headers=headers).json()
    return exchange[0]['basePrice']

# 3. 날씨 확인
apiurl = 'http://api.openweathermap.org/data/2.5/weather?q='
apikey = '&APPID=bc36bd2717c588f98d887f0c0025db13'
    
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

# 텔레그램 봇 생성

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
genietoken= "1232357351:AAH6fwSyjpvXHC63279YUoLMeKkwEWhFVO8"
bot = telepot.Bot(genietoken)

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

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def cctv_command(bot, update):
    print("ddd")
    show_list = []
    show_list.append(InlineKeyboardButton("1.거실", callback_data="url1"))
    show_list.append(InlineKeyboardButton("2.안방", callback_data="url2")) 
    show_list.append(InlineKeyboardButton("취소", callback_data="cancel")) # add cancel button
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup

    update.message.reply_text("어떤 방 cctv를 볼까요?", reply_markup=show_markup)


def callback_get(bot, update):
    print("callback")
    if update.callback_query.data == "좋아":
        bot.edit_message_text(text="진짜? 내 추천 좋지?! 오늘 술 잘 마시고 지나친 음주는 몸에 안 좋은 거 알지?!" + "\n" + "다음에 또 놀러와!",
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id)

    if update.callback_query.data == '별로야' :
        bot.edit_message_text(text= "솔직한 의견 고마워" + "\n" + "다음에 또 놀러와!",
                        chat_id = update.callback_query.message.chat_id,
                        message_id = update.callback_query.message.message_id)def callback_get(bot, update):
    

#대화 시작
def handle(msg):
    content, chat, id = telepot.glance(msg)
#    print(content, chat, id)  # 텔레그램에 입력되는 메세지의 타입, 채팅 타입, 메세지 송신 ID
    city = 'gurgaon'
    if content == 'text':
        if msg['text'] == '1':
#            bot.sendMessage(id, '집안사진를 확인합니다.')
        
            bot.sendMessage(id, InfoMsg2)
            if msg['text'] == '7':
                bot.sendMessage(id, 'aaa')
                bot.sendMessage(id, '거실 사진') 
                get_cctv_pic(id)
                bot.sendMessage(id, InfoMsg)
            elif msg['text'] == '8':
                bot.sendMessage(id, 'bbb')
                bot.sendMessage(id, '안방')
            else:
                bot.sendMessage(id, 'ccc')
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
            bot.sendMessage(id, '인도 코로나 NEWS를 확인합니다.')
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
#미정 chat id
bot.sendMessage('910651690', 'BOT 이 시작했습니다.')

#영선 chat id
#bot.sendMessage('438787080', 'BOT 이 시작했습니다.')

bot.message_loop(handle)

while status == True:

    time.sleep(10)