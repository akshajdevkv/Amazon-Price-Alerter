from bs4 import BeautifulSoup
import requests
import csv
import smtplib
from email.message import EmailMessage

def send_email(from_address,password,to_address,name,product_title,product_price,my_price,url):
	message = EmailMessage()
	message['from'] = from_address
	message['to'] = to_address
	message['subject'] = 'Hooray!, '+name+'- Amazon Price Alerter'
	message.set_content('Hey %s your %s which you wished to be under %s rupees is now at %s rupees.That means now you can buy it, Congratulations !.However now onwards you won\'t recieive my email :( .If you liked Amazon Price Alerter make sure to share it to your Friends! Bye.\n\nYour Product Link: %s'%(name,product_title,my_price,product_price,url))
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
            headers = {'User-Agent': 'Your User-Agent'}
            r = requests.get(url,headers=headers)
            soup = BeautifulSoup(r.text,'html.parser')         
            try:
                product_title = soup.find('span',{'id':'productTitle'}).text.strip()
                product_price = ''.join(soup.find('div',{'id':'price'}).find_all('span')[2].text.strip()[2:].split(','))
                if float(product_price) <= float(my_price):                	
                	print(send_email(from_address='youremail@gmail.com',password='password',to_address=email_address,name=name,product_price=product_price,product_title=product_title,my_price=my_price,url=url))                 
                else:
                	remaining_users.append(user)
            except Exception as err:
                print(err)                
    with open('database.csv','w') as csv_file_1:
        csv_writer = csv.writer(csv_file_1)
        csv_writer.writerows(remaining_users)
    time.sleep(86400)
