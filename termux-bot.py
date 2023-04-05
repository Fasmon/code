import telebot
import time
import datetime
import multiprocessing
import os
import requests

from bs4 import BeautifulSoup
from telebot import types

CHATID = '1953140562'
HEADERS = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
}
bot = telebot.TeleBot('6175826522:AAFgIqbIAVPSNS_ncCj4Q_aqj2kjhD1A3G8')

def Clear():
	try:
		if len(os.listdir(os.getcwd() + '/Helper/lesson/')) > 6:
			data = datetime.datetime.now().strftime('%Y.%m.%d')
			listdir = os.listdir(os.getcwd() + '/Helper/lesson')
			list_files = ['Monday.txt','Tuesday.txt','Wednesday.txt','Thursday.txt','Friday.txt','list_time.txt']

			for i in listdir:
				if not i in list_files:
					name_files = i.split()[1][:-4]
					if int(data.split('.')[0]) > int(name_files.split('.')[0]) or int(data.split('.')[1]) > int(name_files.split('.')[1]) or int(data.split('.')[2]) > int(name_files.split('.')[2]): os.remove(os.getcwd() + f'/Helper/lesson/replacement {name_files}.txt')

	except Exception as ex: print('Clear:',ex)

def Anime():
	while True:
		try:
			Clear()
			list_anime = [i for i in open(os.getcwd() + '/Helper/anime_shorts/list_anime.txt').read().split('\n')]
			name_anime = [i for i in open(os.getcwd() + '/Helper/anime_shorts/name_anime.txt').read().split('\n')]
			check = open(os.getcwd() + '/Helper/anime_shorts/check.txt').read()
			day = datetime.datetime.now().strftime('%a')

			if day == 'Mon':
				if 'True' in check: 
					open(os.getcwd() + '/Helper/anime_shorts/check.txt','w').write('False')
					open(os.getcwd() + '/Helper/anime_shorts/list_anime.txt','w')
			
			else: open(os.getcwd() + '/Helper/anime_shorts/check.txt','w').write('True')

			r = requests.get('https://anime1.animebesst.org/',headers=HEADERS)
			soup = BeautifulSoup(r.text,'html5lib')
			shorts = soup.find_all('div',class_='shortstory-film')

			for i in shorts:
				name = i.div.p.a.text
				link = i.div.p.a.get('href')
				if name in name_anime:
					if name not in list_anime:
						open(os.getcwd() + '/Helper/anime_shorts/list_anime.txt','a').write(name + '\n')
						message = f'<b><a href="{link}">{name}</a></b>'
						bot.send_message(CHATID,message,parse_mode='HTML')

			time.sleep(10 * 60)

		except Exception as ex: print('Anime:',ex)

def Lesson():
	while True:
		try:
			data = datetime.datetime.now().strftime('%H:%M %a %S').split()
			list_time = [i.split(' - ')[0] for i in open(os.getcwd() + '/Helper/lesson/list_time.txt').read().split('\n')]
			data1 = datetime.datetime.now().strftime('%Y.%m.%d')
			listdir = os.listdir(os.getcwd() + '/Helper/lesson')
			list_files = ['Monday.txt','Tuesday.txt','Wednesday.txt','Thursday.txt','Friday.txt','list_time.txt']
			number = 0
			x = []
			day = datetime.datetime.now().strftime('%a')
			list_lesson = ''

			for i in os.listdir(os.getcwd() + '/Helper/lesson'):
				if not i in list_files:
					name_files = i.split()[1][:-4]
					if data1 == name_files:
						list_lesson = open(os.getcwd() + f'/Helper/lesson/replacement {name_files}.txt').read().split('\n')
						break

					else:
						if data[1] == 'Mon': list_lesson = open(os.getcwd() + '/Helper/lesson/Monday.txt').read().split('\n')
						elif data[1] == 'Tue': list_lesson = open(os.getcwd() + '/Helper/lesson/Tuesday.txt').read().split('\n')
						elif data[1] == 'Wed': list_lesson = open(os.getcwd() + '/Helper/lesson/Wednesday.txt').read().split('\n')
						elif data[1] == 'Thu': list_lesson = open(os.getcwd() + '/Helper/lesson/Thursday.txt').read().split('\n')
						elif data[1] == 'Fri': list_lesson = open(os.getcwd() + '/Helper/lesson/Friday.txt').read().split('\n')

			for i in list_lesson:
				if i == '': list_lesson.remove('')

			if data[1] in ['Sat','Sun']: pass
			else:
				number = 0
				list_lesson = ''

				for _ in list_time:
					if len(list_lesson) >= (number + 1):
						if data[0] == _[0]: bot.send_message(CHATID,f'<b>Урок <u>{list_lesson[number]}</u> Начался!</b>',parse_mode='HTML')
						elif data[0] == _[1]: bot.send_message(CHATID,'<b>Перемена!</b>',parse_mode='HTML')

					number += 1

				time.sleep(60 - int(data[2]))

		except Exception as ex: print('Lesson:',ex)

@bot.message_handler(commands=['replacement'])
def a(message):
	if message.text == '/replacement':
		bot.send_message(CHATID,'<b>Для Указание Замены Нужно вести дату разделитель и Замена\nНапример: 2023.04.03 : Урок1,Урок2,Урок3</b>',parse_mode='HTML')

	else:
		command = message.text
		data = command.split(' : ')[0]
		lesson = command.split(' : ')[1].split(',')
		x = '\n'.join(lesson)

		open(os.getcwd() + f'/Helper/lesson/{data}.txt','w').write(x)

@bot.message_handler(commands=['help','start'])
def a(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	weather_btn = types.KeyboardButton("Погода")
	anime_btn = types.KeyboardButton("Аниме")
	lesson = types.KeyboardButton("Расписание")
	markup.add(weather_btn,anime_btn,lesson)
	bot.send_message(CHATID,text='Жду команду',reply_markup=markup)
	bot.send_message(CHATID,'<b>Для того чтобы записать новое расписание нужно вести команду <u>/list</u> день недель после стави разделитель (:) Расписание между уроков ставте кому Например:\n/list Monday : Урок1,Урок2,Урок3</b>',parse_mode='HTML')
	bot.send_message(CHATID,'для того чтобы указать замену уроков нужно ввести команду /replacement')

@bot.message_handler(commands=['list'])
def a(message):
	if message.text == '/list':
		bot.send_message(CHATID,'<b>Для того чтобы записать новое расписание нужно вести команду <u>/list</u> день недель после стави разделитель (:) Расписание между уроков ставте кому Например:\n/list Monday : Урок1,Урок2,Урок3</b>',parse_mode='HTML')
	
	else:
		command = message.text.replace('/list ','')
		day = command.split(' : ')[0]
		list_lesson = command.split(' : ')[1].split(',')
		x = '\n'.join(list_lesson)
		if 'Monday' in day or 'monday' in day or 'Понедельник' in day or 'понедельник' in day: open(os.getcwd() + '/Helper/lesson/Monday.txt','w').write(x)
		elif 'Tuesday' in day or 'tuesday' in day or 'Вторник' in day or 'вторник' in day: open(os.getcwd() + '/Helper/lesson/Tuesday.txt','w').write(x)
		elif 'Wednesday' in day or 'wednesday' in day or 'Середа' in day or 'середа' in day: open(os.getcwd() + '/Helper/lesson/Wednesday.txt','w').write(x)
		elif 'Thursday' in day or 'thursday' in day or 'Четверг' in day or 'четверг' in day: open(os.getcwd() + '/Helper/lesson/Thursday.txt','w').write(x)
		elif 'Friday' in day or 'friday' in day or 'Пятница' in day or 'пятница' in day: open(os.getcwd() + '/Helper/lesson/Friday.txt','w').write(x)

@bot.message_handler(content_types=['text'])
def a(message):
	message = message.text
	if message == 'Погода':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		village = types.KeyboardButton("Спаское")
		izmail = types.KeyboardButton("Измаил")
		tatarbunary = types.KeyboardButton("Татарбунары")
		back = types.KeyboardButton("Назад")
		markup.add(village,izmail,tatarbunary,back)
		bot.send_message(CHATID,text='Жду команду',reply_markup=markup)

	elif message == 'Спаское':
		# Показует Погоду в Спаском
		r = requests.get('https://www.gismeteo.ua/weather-spaske-91072/now/',headers=HEADERS)
		soup = BeautifulSoup(r.text,'html5lib')
		Now_temperature = soup.find('span',class_='unit unit_temperature_c')
		Weather = soup.find('div',class_='now-desc')
		Humidity = soup.find_all('div',class_='item-value')[2]
		x = f'<a href="https://www.gismeteo.ua/weather-spaske-91072/now/">ПОГОДА В СПАСКОЕ</a>\nТемпература:  <u><b>{Now_temperature.text}</b></u> C\nПогода:  <u><b>{Weather.text}</b></u>\nВлажность:  <u><b>{Humidity.text}%</b></u>'
		bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Измаил':
		# Показует Погоду в Измаиле
		r = requests.get('https://www.gismeteo.ua/weather-izmail-4986/now/',headers=HEADERS)
		soup = BeautifulSoup(r.text,'html5lib')
		Now_temperature = soup.find('span',class_='unit unit_temperature_c')
		Weather = soup.find('div',class_='now-desc')
		Humidity = soup.find_all('div',class_='item-value')[2]
		x = f'<a href="https://www.gismeteo.ua/weather-izmail-4986/now/">ПОГОДА В ИЗМАИЛЕ</a>\nТемпература:  <u><b>{Now_temperature.text}</b></u> C\nПогода:  <u><b>{Weather.text}</b></u>\nВлажность:  <u><b>{Humidity.text}%</b></u>'
		bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Татарбунары':
		# Показует Погоду в Татарбунар
		r = requests.get('https://www.gismeteo.ua/weather-tatarbunary-12183/now/',headers=HEADERS)
		soup = BeautifulSoup(r.text,'html5lib')
		Now_temperature =soup.find('span',class_='unit unit_temperature_c')
		Weather = soup.find('div',class_='now-desc')
		Humidity = soup.find_all('div',class_='item-value')[2]
		x = f'<a href="https://www.gismeteo.ua/weather-tatarbunary-12183/now/">ПОГОДА В ТАТАРБУНАРЫ</a>\nТемпература:  <u><b>{Now_temperature.text}</b></u> C\nПогода:  <u><b>{Weather.text}</b></u>\nВлажность:  <u><b>{Humidity.text}%</b></u>'
		bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Назад':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		weather_btn = types.KeyboardButton("Погода")
		anime_btn = types.KeyboardButton("Аниме")
		lesson = types.KeyboardButton("Расписание")
		markup.add(weather_btn,anime_btn,lesson)
		bot.send_message(CHATID,text='Жду команду',reply_markup=markup)

	elif message == 'Аниме':
		list_anime = [i for i in open(os.getcwd() + '/Helper/anime_shorts/list_anime.txt').read().split('\n')]
		name_anime = [i for i in open(os.getcwd() + '/Helper/anime_shorts/name_anime.txt').read().split('\n')]

		r = requests.get('https://anime1.animebesst.org/',headers=HEADERS)
		soup = BeautifulSoup(r.text,'html5lib')

		shorts = soup.find_all('div',class_='shortstory-film')
		for i in shorts:
			name = i.div.p.a.text
			link = i.div.p.a.get('href')
			if name in name_anime:
				x = f'<b><a href="{link}">{name}</a></b>'
				bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Расписание':
		markup = types.ReplyKeyboardMarkup(row_width=4)
		btn1 = types.KeyboardButton("Уроков на Сегодня")
		btn2 = types.KeyboardButton("Уроков на Завтра")
		btn3 = types.KeyboardButton("На день недель")
		btn4 = types.KeyboardButton("Назад")
		markup.add(btn1,btn2,btn3,btn4)
		bot.send_message(CHATID,text='Жду команду',reply_markup=markup)

	elif message == 'На день недель':
		markup = types.ReplyKeyboardMarkup(row_width=3)
		btn1 = types.KeyboardButton("Понедельник")
		btn2 = types.KeyboardButton("Вторник")
		btn3 = types.KeyboardButton("Середа")
		btn4 = types.KeyboardButton("Четверг")
		btn5 = types.KeyboardButton("Пятница")
		btn6 = types.KeyboardButton("Назад")
		markup.add(btn1,btn2,btn3,btn4,btn5,btn6)
		bot.send_message(CHATID,text='Жду команду',reply_markup=markup)

	elif message == 'Уроков на Сегодня':
		list_time = [i.split(' - ')[0] for i in open(os.getcwd() + '/Helper/lesson/list_time.txt').read().split('\n')]
		data = datetime.datetime.now().strftime('%Y.%m.%d')
		list_files = ['Monday.txt','Tuesday.txt','Wednesday.txt','Thursday.txt','Friday.txt','list_time.txt']
		number = 0
		x = []
		day = datetime.datetime.now().strftime('%a')

		for i in os.listdir(os.getcwd() + '/Helper/lesson'):
			if not i in list_files:
				if i.split()[1][:-4] == data:
					list_lesson = open(os.getcwd() + f'/Helper/lesson/{i}').read().split('\n')
					break
			else:
				if day == 'Mon': list_lesson = open(os.getcwd() + '/Helper/lesson/Monday.txt').read().split('\n')
				elif day == 'Tue': list_lesson = open(os.getcwd() + '/Helper/lesson/Tuesday.txt').read().split('\n')
				elif day == 'Wed': list_lesson = open(os.getcwd() + '/Helper/lesson/Wednesday.txt').read().split('\n')
				elif day == 'Thu': list_lesson = open(os.getcwd() + '/Helper/lesson/Thursday.txt').read().split('\n')
				elif day == 'Fri': list_lesson = open(os.getcwd() + '/Helper/lesson/Friday.txt').read().split('\n')
				elif day in ['Sat','Sun']: list_lesson = open(os.getcwd() + '/Helper/lesson/Monday.txt').read().split('\n')

		for i in list_lesson:
			if i == '': list_lesson.remove('')

		for i in list_lesson:
			if len(list_lesson) >= number:
				x.append(f'<b>{number + 1} - {list_lesson[number]} в {list_time[number]}</b>')
			number += 1

		x = '\n'.join(x)
		bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Уроков на Завтра':
		list_time = [i.split(' - ')[0] for i in open(os.getcwd() + '/Helper/lesson/list_time.txt').read().split('\n')]
		day = datetime.datetime.now().strftime('%a')
		number = 0
		x = []

		if day == 'Mon': list_lesson = open(os.getcwd() + '/Helper/lesson/Tuesday.txt').read().split('\n')
		elif day == 'Tue': list_lesson = open(os.getcwd() + '/Helper/lesson/Wednesday.txt').read().split('\n')
		elif day == 'Wed': list_lesson = open(os.getcwd() + '/Helper/lesson/Thursday.txt').read().split('\n')
		elif day == 'Thu': list_lesson = open(os.getcwd() + '/Helper/lesson/Friday.txt').read().split('\n')
		elif day == 'Fri': list_lesson = open(os.getcwd() + '/Helper/lesson/Monday.txt').read().split('\n')
		elif day in ['Sat','Sun']: list_lesson = open(os.getcwd() + '/Helper/lesson/Monday.txt').read().split('\n')

		for i in list_lesson:
			if i == '': list_lesson.remove('')

		for i in list_lesson:
			if len(list_lesson) >= number:
				x.append(f'<b>{number + 1} - {list_lesson[number]} в {list_time[number]}</b>')
			number += 1

		x = '\n'.join(x)
		bot.send_message(CHATID,x,parse_mode='HTML')


	elif message == 'Понедельник':
		list_time = [i.split(' - ')[0] for i in open(os.getcwd() + '/Helper/lesson/list_time.txt').read().split('\n')]
		day = datetime.datetime.now().strftime('%a')
		list_lesson = open(os.getcwd() + '/Helper/lesson/Monday.txt').read().split('\n')
		number = 0
		x = []

		for i in list_lesson:
			if i == '': list_lesson.remove('')

		for i in list_lesson:
			if len(list_lesson) >= number:
				x.append(f'<b>{number + 1} - {list_lesson[number]} в {list_time[number]}</b>')
			number += 1

		x = '\n'.join(x)
		bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Вторник':
		list_time = [i.split(' - ')[0] for i in open(os.getcwd() + '/Helper/lesson/list_time.txt').read().split('\n')]
		day = datetime.datetime.now().strftime('%a')
		list_lesson = open(os.getcwd() + '/Helper/lesson/Tuesday.txt').read().split('\n')
		number = 0
		x = []

		for i in list_lesson:
			if i == '': list_lesson.remove('')

		for i in list_lesson:
			if len(list_lesson) >= number:
				x.append(f'<b>{number + 1} - {list_lesson[number]} в {list_time[number]}</b>')
			number += 1

		x = '\n'.join(x)
		bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Середа':
		list_time = [i.split(' - ')[0] for i in open(os.getcwd() + '/Helper/lesson/list_time.txt').read().split('\n')]
		day = datetime.datetime.now().strftime('%a')
		list_lesson = open(os.getcwd() + '/Helper/lesson/Wednesday.txt').read().split('\n')
		number = 0
		x = []

		for i in list_lesson:
			if i == '': list_lesson.remove('')

		for i in list_lesson:
			if len(list_lesson) >= number:
				x.append(f'<b>{number + 1} - {list_lesson[number]} в {list_time[number]}</b>')
			number += 1

		x = '\n'.join(x)
		bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Четверг':
		list_time = [i.split(' - ')[0] for i in open(os.getcwd() + '/Helper/lesson/list_time.txt').read().split('\n')]
		day = datetime.datetime.now().strftime('%a')
		list_lesson = open(os.getcwd() + '/Helper/lesson/Thursday.txt').read().split('\n')
		number = 0
		x = []

		for i in list_lesson:
			if i == '': list_lesson.remove('')

		for i in list_lesson:
			if len(list_lesson) >= number:
				x.append(f'<b>{number + 1} - {list_lesson[number]} в {list_time[number]}</b>')
			number += 1

		x = '\n'.join(x)
		bot.send_message(CHATID,x,parse_mode='HTML')

	elif message == 'Пятница':
		list_time = [i.split(' - ')[0] for i in open(os.getcwd() + '/Helper/lesson/list_time.txt').read().split('\n')]
		day = datetime.datetime.now().strftime('%a')
		list_lesson = open(os.getcwd() + '/Helper/lesson/Friday.txt').read().split('\n')
		number = 0
		x = []

		for i in list_lesson:
			if i == '': list_lesson.remove('')

		for i in list_lesson:
			if len(list_lesson) >= number:
				x.append(f'<b>{number + 1} - {list_lesson[number]} в {list_time[number]}</b>')
			number += 1

		x = '\n'.join(x)
		bot.send_message(CHATID,x,parse_mode='HTML')


if __name__ == '__main__':
	multiprocessing.Process(target=Lesson).start()
	multiprocessing.Process(target=Anime).start()
	while True:
		try:
			bot.polling(non_stop=True)
		except: pass