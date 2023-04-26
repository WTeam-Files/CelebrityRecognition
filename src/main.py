import requests
import re
import requests
import re, flask, json, os
from bs4 import BeautifulSoup


def upload(filename):
    try:
        response = requests.post(
            'https://starbyface.com/Home/LooksLikeByPhoto',
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
                'Accept-Language': 'en-US,en;q=0.5', 'Referer': 'https://starbyface.com/'
            },
            files={
                'file': (filename, open(filename, 'rb'), 'image/*')
            }
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        female = re.findall('data-subtext="([^"]+)', str(soup.find('select', {'id': 'female-pair-select'})))
        male = re.findall('data-subtext="([^"]+)', str(soup.find('select', {'id': 'male-pair-select'})))
        result = {
            "male": male[0],
            "female": female[0],
            'maleu':f'https://starbyface.com/ImgFiles/{male[0]}/1.jpg',
            'femaleu':f'https://starbyface.com/ImgFiles/{female[0]}/1.jpg',
            "time": response.elapsed.total_seconds()
        }

    except FileNotFoundError: r = {}; r['error'] = "Dile not found"
    except requests.exceptions.RequestException: r = {}; r['error'] = "Request failed"
    except IndexError: r = {}; r['error'] = "Celebrity name not found"
    return result




import telebot
# bot token here
bot = telebot.TeleBot("######", num_threads=20, skip_pending=True)

@bot.message_handler(commands=['start'])
def m(message):
  k = '''
👋🏻꒐ اهلا بك في  بوت معرفه المشهور (او معرفه شبيهكك من المشاهير) .
⏺꒐ قم بأرسال صورتك، او صورة صديق لك وسيقوم الذكاء الاصطناعي بتحديد المشهور ..
⎯ ⎯ ⎯ ⎯
  '''
  bot.reply_to(message, k)
@bot.message_handler(content_types=['photo'])
def ph(message):
  bot.reply_to(message, '⏱  يتم الان المعالجة، سوف يتم ارسال نتيجة لرجل ولبنت ..')
  fileid = message.photo[-1].file_id
  path = bot.get_file(fileid).file_path
  d = bot.download_file(path)
  with open("img.jpg", 'wb') as z:
    z.write(d)
  x = upload('img.jpg')
  error = x.get('error')
  if error != None:
    bot.reply_to(message, f'حدث خطأ ..\n{error}')
  else:
    male = x.get("male")
    malee = x.get('maleu')
    female = x.get("female")
    femalee = x.get('femaleu')
    t = int(x.get("time"))
    bot.send_photo(message.chat.id, malee, caption=f'🥷🏻 المشهور: {male} .\n⏱ الوقت المستغرق: {t}s .')
    bot.send_photo(message.chat.id, femalee, caption=f'🥷🏻 المشهورة: {female} .\n⏱ الوقت المستغرق: {t}s .')
bot.infinity_polling()
