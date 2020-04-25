import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import xlsxwriter
import sqlite3

#Function which converts image data into BinaryData

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

#Function which gives the INSERT instruction to Database
def insertBLOB(name,photo,pt):
    try:
        empPhoto = convertToBinaryData(photo)
        print("Connected to SQLite")
        cursor.execute(''' INSERT INTO new_employee (name,photo,pt) VALUES ( ? , ? , ? )''',(name,empPhoto,pt,))
        sqliteConnection.commit()
        print("Image inserted successfully as a BLOB into a table")

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)

#Function which downloads the pictures of the personalities to directore /image
def u_to_j(url,file_path,filename):
	filename = "{}.jpg".format(filename)
	full_path = '{}{}'.format(file_path,filename)
	urllib.request.urlretrieve(url,full_path)

	print('{} saved.'.format(filename))

	return None

Aries = 'dynamic, freedom-lovin spontaneous, adventurous and able to take initiatives, inspires others'
Taurus = 'friendly, high bearing capacity, strong willpower, developed sense of aesthetics'
Gemini = 'talkative, joyful, full of knowledge,intellectual, logical, quick grasping'
Cancer = 'empathy, motherhood, protective, sacrificing and receptive to other people’s needs'
Leo = ' noble, expanded thinking, generous, self confident, inspiring, artistic'
Virgo = 'brave, sincere, dynamic, freedom loving, spontaneous, adventurous, childlike enthusiasm'
Libra = 'adventurous, takes initiatives, inspiring, childlike enthusiasm'
Scorpio = 'power to transform themselves, deep perception, intuition, bearing and determined'
Sagittarius = 'open to new things, understanding, generous, philosophical, optimistic, faithful in God'
Capricorn = 'withstands difficulties, trustworthy, patient, determined'
Aquarius = 'humane, visionary, progressive, objective, rational and scientific, good at socializing'
Pisces = ' sensitive, compassionate, strong imagination, artistic inspiration, creative'

FILE_PATH='images/'#change this if you've named images folder as anything else

def zodiac_sign(day, month):
	day = int(day)
	month = int(month)
	# print("entered function", day,month)
	if month == 12:
		astro_sign = Sagittarius if(day<22) else Capricorn
	elif month == 1:
		astro_sign = Capricorn if(day<20) else Aquarius
	elif month == 2:
		astro_sign=Aquarius if(day<19) else Pisces
	elif month == 3:
		astro_sign = Pisces if(day<21) else Aries
	elif month==4:
		astro_sign = Aries if(day<20) else Taurus
	elif month==5:
		astro_sign=Taurus if(day<21) else Gemini
	elif month==6:
		astro_sign=Gemini if(day<21) else Cancer
	elif month==7:
		astro_sign=Cancer if(day<23) else Leo
	elif month==8:
		astro_sign=Leo if(day<23) else Virgo
	elif month==9:
		astro_sign=Virgo if(day<23) else Libra
	elif month==10:
		astro_sign=Libra if(day<23) else Scorpio
	elif month==11:
		astro_sign=Scorpio if(day<22) else Sagittarius
	return astro_sign

url = 'https://en.wikipedia.org/wiki/List_of_Indian_film_actors'
un= (r"D:\Mallik\Progs\images\unavailable.jpg")#This binds the unavailable picture to the program, change this before running the code 
row = 0
column = 0
workbook = xlsxwriter.Workbook("celebrities.xlsx")#excel file name where the output is stored it is created
worksheet = workbook.add_worksheet("first sheet")
exist = workbook.get_worksheet_by_name("first sheet")
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup.find_all('ul')
exist.write(row,column,"NAME")
column = column+3
exist.write(row,column,"PICTURE LINK")
column = column+5
exist.write(row,column,"PERSONALITY TRAITS")
row = 1
column=0
sqliteConnection = sqlite3.connect('celebrities_database.db')#Database creation
cursor = sqliteConnection.cursor()
cursor.executescript('''DROP TABLE IF EXISTS new_employee;
	CREATE TABLE new_employee (name TEXT NOT NULL, photo BLOB,pt TEXT);''')

#Actors extraction
u = []
for i in range(1,24):
	u.append(tags[i])

title_names_actor = []
href_actor = []	
for ta in u:
	for li in ta.find_all('li'):
		for anchor in li.find_all('a'):
			title_names_actor.append(anchor.get('title',None))
			href_actor.append(anchor.get('href',None))

for splittest in title_names_actor:
	exist.write(row,column,splittest)
	test = []
	test = (str(splittest).replace(" ","_"))
	print(test)
	for testo in href_actor:
		if testo == '/wiki/'+test:
			inh = urllib.request.urlopen('https://en.wikipedia.org'+testo).read()
			print(testo)
			so = BeautifulSoup(inh,'html.parser')
			im = so.find('table',{'class':'infobox biography vcard'})
			column = column+2
			exist.write(row,column,"  ")
			column = column+1
			try:
				igm = im.find('img')
				al = igm.get('src',None)
				u_to_j("https:"+al,FILE_PATH,test)
				#Images access path, change it according to your system
				img_path = "D:\Mallik\Progs\images\\"+test+".jpg"
				exist.write(row,column,al)
				column = column+4
				exist.write(row,column,"  ")
				try:
					bd = im.find('span',{'class':'bday'})
					dob = []
					dob = bd.get_text().split('-')
					day = dob[2]
					month = dob[1]
					zsw = zodiac_sign(day,month)
					column = column+1
					exist.write(row,column,zsw)
					insertBLOB(splittest,img_path,zsw)
					column =0
					row = row+1
				except:
					column = column+1
					exist.write(row,column,'Doesnt exist')
					insertBLOB(splittest,img_path,'unavailable')
					column = 0 
					row = row+1
			except:
				exist.write(row,column,'Doesnt exist')
				column= column+4
				exist.write(row,column,"  ")
				try:
					bd = im.find('span',{'class':'bday'})
					dob = []
					dob = bd.get_text().split('-')
					day = dob[2]
					month = dob[1]
					zsw = zodiac_sign(day,month)
					insertBLOB(splittest,un,zsw)
					column = column+1
					exist.write(row,column,zsw)
					column =0
					row = row+1
				except:
					column = column+1
					exist.write(row,column,'Doesnt exist')
					insertBLOB(splittest,un,'unavailable')
					column = 0 
					row = row+1
				continue
print("written actors successfully..")

#Actresses Extraction
column = 0
url2 = 'https://en.wikipedia.org/wiki/List_of_Indian_film_actresses'
html2 = urllib.request.urlopen(url2).read()
soup2 = BeautifulSoup(html2,'html.parser')
tags2 = soup2.find_all('ul')
fe = []
for x in range(1,25):
	fe.append(tags2[x])

title_names_actress = []
href_actress = []
for ts in fe:
	for ila in ts.find_all('li'):
		for anchora in ila.find_all('a'):
			title_names_actress.append(anchora.get('title',None))
			href_actress.append(anchora.get('href',None))

for replacetest in title_names_actress:
	exist.write(row,column,replacetest)
	acctes = []
	acctest = (str(replacetest).replace(" ","_"))
	print(acctest)
	for testa in href_actress:
		if testa == '/wiki/'+acctest:
			acch = urllib.request.urlopen('https://en.wikipedia.org'+testa).read()
			print(testa)
			soa = BeautifulSoup(acch,'html.parser')
			ima = soa.find('table',{'class':'infobox biography vcard'})
			column = column+2
			exist.write(row,column,"  ")
			column = column+1
			try:
				gmi = ima.find('img')
				la = gmi.get('src',None)
				exist.write(row,column,la)
				u_to_j("https:"+la,FILE_PATH,acctest)
				#Images access path, change it according to your system
				imga_path = "D:\Mallik\Progs\images\\"+acctest+".jpg"
				column = column+4
				exist.write(row,column,"  ")

				try:
					bda = ima.find('span',{'class':'bday'})
					doba = []
					doba = bda.get_text().split('-')
					daya = doba[2]
					montha = doba[1]
					zs = zodiac_sign(daya,montha)
					insertBLOB(replacetest,imga_path,zs)
					column = column+1
					exist.write(row,column,zs)
					column=0
					row=row+1
				except:
					column = column+1
					exist.write(row,column,'Doesnt exist')
					insertBLOB(replacetest,imga_path,'unavailable')
					column = 0 
					row = row+1
			except:
				exist.write(row,column,'Doesnt exist')
				column= column+4
				exist.write(row,column,"  ")
				try:
					bda = ima.find('span',{'class':'bday'})
					doba = []
					doba = bda.get_text().split('-')
					daya = doba[2]
					montha = doba[1]
					zs = zodiac_sign(daya,montha)
					insertBLOB(replacetest,un,zs)
					column = column+1
					exist.write(row,column,zs)
					column=0
					row=row+1
				except:
					column = column+1
					exist.write(row,column,'Doesnt exist')
					insertBLOB(replacetest,un,'unavailable')
					column = 0 
					row = row+1
				continue
print("written actresses successfully..")

workbook.close()
if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")
