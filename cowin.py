import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv
import json
from  datetime import date
import time
import logging
logging.basicConfig(filename='cowin.log', encoding='utf-8', level=logging.INFO)
today = (date.today()).strftime("%d-%m-%y")
print(today)
pincodes = ['400011', '400013', '400008']
names = ['Wockhadt', "Nair"]
load_dotenv('creds.env')
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
queries = 0
a=time.time()
done=[]
start=time.time()

while True:
    try:
        good=[]
        for pin in pincodes:
            
            ret = requests.get(f'https://cowin.gov.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={today}&vaccine=COVISHIELD')
            # print(ret.text)
            queries+=1
                
            d=json.loads(ret.text)
            for i in d['centers']:
                a=i['sessions'][0]
                if a['available_capacity']>=20 and a['min_age_limit']>=45:
                    good.append([i['name'], a['available_capacity'], a['date']])
        # print(good)
        if len(good)>0:
            for hosp in good:
                if [hosp[0],hosp[2]] in done: continue
                done.append([hosp[0],hosp[2]])
                mes = f'name : {hosp[0]}\ncapacity : {hosp[1]}\ndate : {hosp[2]}\n link : https://www.cowin.gov.in/home'
                message = client.messages.create(
                                            body=mes,
                                            from_='whatsapp:+14155238886',
                                            to='whatsapp:+919930004400'
                                        )
                message = client.messages.create(
                                            body=mes,
                                            from_='whatsapp:+14155238886',
                                            to='whatsapp:+919967578000'
                                        )
        
        # a=int('?')
        time.sleep(6)
        if queries==99:
 
            end=time.time()-start
            logging.info(end)
            # if end<5*60:
            #     time.sleep(5*60-end)
    except Exception as e:
        logging.info(e)  

        
    

    
        
    

