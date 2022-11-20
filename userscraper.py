from flask import Flask,request,jsonify,render_template
import utils
import userscraper
app = Flask(__name__,template_folder='template')
import numpy as np
import pandas as pd
import pickle
from flask_cors import CORS,cross_origin
import requests,bs4
from bs4 import BeautifulSoup

model=pickle.load(open('RandomForestModel.pkl','rb'))
car = pd.read_csv("Cleaned_cardekho.csv")

car_models=sorted(car['model'].unique())


def getcontainers(car):
    url="https://www.cardekho.com/used-{}+cars+in+mumbai".format(car)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    r = requests.get(url,headers=headers)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent,'html.parser')
    container = soup.find_all('div',{'class':'NewUcExCard posR'})
    #carpix = soup.find_all('div',{'class':'imagebox hover'})
    #carkm = soup.find_all('div',{'class':'dotsDetails'})
    return container

def getcarpix(car):
    url="https://www.cardekho.com/used-{}+cars+in+mumbai".format(car)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    r = requests.get(url,headers=headers)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent,'html.parser')
    #container = soup.find_all('div',{'class':'NewUcExCard posR'})
    carpix = soup.find_all('div',{'class':'imagebox hover'})
    #carkm = soup.find_all('div',{'class':'dotsDetails'})
    return carpix

def getcarkms(car):
    url="https://www.cardekho.com/used-{}+cars+in+mumbai".format(car)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    r = requests.get(url,headers=headers)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent,'html.parser')
    #container = soup.find_all('div',{'class':'NewUcExCard posR'})
    #carpix = soup.find_all('div',{'class':'imagebox hover'})
    carkm = soup.find_all('div',{'class':'dotsDetails'})
    return carkm

def getuscarpix(carpix):
    uscarpix=[]
    for i in range(len(carpix)):
        uscarpix.append(carpix[i].find('img')['src'])
    return uscarpix

def getusyear(container):
    usyear=[]
    for i in range(len(container)):
        usyear.append(int(container[i].get_text()[:4]))
    return usyear

def getuscompany(container):
    uscompany=[]
    for i in range(len(container)):
        co=''
        for k in container[i].find('a')['title'][5:]:
            if k==' ':
                break
            else:
                co+=k
        uscompany.append(co)
    return uscompany

def getusmodel(container):
    usmodel=[]
    for i in range(len(container)):
        usmodel.append(container[i].find('a')['title'][5:])
    return usmodel

def getusprice(container):
    usprice=[]
    for i in range(len(container)):
        x=container[i].find('p').get_text().strip()
        p=''
        for i in x:
              if i=='₹' or i==' ':
                pass
              else:
                p+=i
        fp=''
        if 'Lakh' in p:
            for j in p:
                if j=='L':
                    break
                else:
                    fp+=j
        if fp=='':
            pass
        else:
            fp = float(fp)*100000
        try:
            usprice.append(int(fp))
        except:
            usprice.append('n/a')
    return usprice

def getusfuel(container):
    usfuel=[]
    for i in range(len(container)):
        fuel=''
        if 'Petrol' in container[i].get_text():
            fuel='Petrol'
        elif 'Diesel' in container[i].get_text():
            fuel='Diesel'
        elif 'CNG' in container[i].get_text():
            fuel='CNG'
        usfuel.append(fuel)     
    return usfuel

def getuskm(carkm):
  uscarkm=[]
  for i in range(len(carkm)):
    kms=''
    for i in carkm[i].get_text():
        if i==',':
            pass
        elif i==' ':
            break
        else:
            kms+=i
    uscarkm.append((int(kms)))
  return uscarkm

def getusmlpindex(usmodel):
    usmlpindex = []
    for i,Model in enumerate(usmodel):
        if Model in car_models:
            usmlpindex.append(i)
    return usmlpindex

def getusmlprice(uscompany,usmodel,usfuel,uskm,usmlpindex,usyear):
    usmlprice = {}
    for i in usmlpindex:
        prediction = model.predict(pd.DataFrame(columns=['model', 'company', 'year', 'km_driven', 'fuel_type'],
                              data=np.array([usmodel[i],uscompany[i],usyear[i],uskm[i],usfuel[i]]).reshape(1, 5)))
        usmlprice[i]=int(np.round(prediction[0],2))
    return usmlprice