from bs4 import BeautifulSoup
import requests
import csv
import time
import smtplib
from email.message import EmailMessage

def send_email(from_address,password,to_address,result,name,product_title,product_price,my_price,url):
	message = EmailMessage()
	message['from'] = from_address
	message['to'] = to_address
	if result == 'positive':
		message['subject'] = 'Hooray!, '+name+'- Amazon Price Alerter'
		message.set_content('Hey %s your %s which you wished to be under %s rupees is now at %s rupees.That means now you can buy it, Congratulations !.However now onwards you won\'t recieive my email :( .If you liked Amazon Price Alerter make sure to share it to your Friends! Bye.\n\nYour Product Link: %s'%(name,product_title,my_price,product_price,url))
	elif result == 'negative':
		message['subject'] = 'Better Luck Tommorow '+name+'-Amazon Price Alerter'
		message.set_content('%s ,Sorry your Product ,sadly did not reach your desired price (%s rupees).I wish you better luck Tommorow.May Tommorow will be your lucky day \n\nyour product link: %s'%(name,my_price,url))
	with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.login(from_address, password)
		smtp.send_message(message)
		smtp.quit()


while True:
    remaining_users = []
    with open('database.csv','r') as csv_file:       
        csv_reader = csv.reader(csv_file) 
        for user in csv_reader:
            url = user[3]
            email_address = user[1]
            my_price = user[2]
            name = user[0]
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'}
            r = requests.get(url,headers=headers)
            soup = BeautifulSoup(r.text,'html.parser')         
            try:
                product_title = soup.find('span',{'id':'productTitle'}).text.strip()
                product_price = ''.join(soup.find('div',{'id':'price'}).find_all('span')[2].text.strip()[2:].split(','))
                if float(product_price) <= float(my_price):
                	
                	print(send_email(from_address='akshajvaranacode404@gmail.com',password='eoovlchuqwaaqail',to_address=email_address,result='positive',name=name,product_price=product_price,product_title=product_title,my_price=my_price,url=url))
 
                 
                else:
                	print(send_email(from_address='akshajvaranacode404@gmail.com',password='eoovlchuqwaaqail',to_address=email_address,result='negative',name=name,product_price=product_price,product_title=product_title,my_price=my_price,url=url))
                 
                	remaining_users.append(user)
            except Exception as err:
                print(err)
                print(send_email(from_address='akshajvaranacode404@gmail.com',password='eoovlchuqwaaqail',to_address=email_address,result='negative',name=name,product_price=product_price,product_title=product_title,my_price=my_price,url=url))
    with open('database.csv','w') as csv_file_1:
        csv_writer = csv.writer(csv_file_1)
        csv_writer.writerows(remaining_users)
    time.sleep(20)
