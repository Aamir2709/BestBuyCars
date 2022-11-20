from flask import Flask,request,render_template
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

scars = pd.read_csv("scrapedcars.csv")




@app.route('/')
def hello_world():
    smodels = scars.Model
    scompanies = scars.Company
    syears = scars.year
    skm = scars.km
    sfueltype = scars.Fueltype
    ssellingprice = scars.Sellingprice
    scarpics = scars.carpics
    ml=utils.mlprice


    car_models=sorted(car['model'].unique())
    mli = utils.mlpindex

    return render_template('index.html',companies=scompanies, models=smodels, years=syears,fueltype=sfueltype,sellingprice=ssellingprice,kms=skm,carpix=scarpics,car_models=car_models,mlprices=ml,mlindex=mli)
    



@app.route('/sell_car',methods=['GET','POST'])
def sell_car():
    companies=sorted(car['company'].unique())
    car_models=sorted(car['model'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('sell.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type)


@app.route('/predict',methods=['POST'])
#@cross_origin()
def predict():

    company=request.form.get('company')

    car_model=request.form.get('car_model')
    year=int(request.form.get('year'))
    fuel_type=request.form.get('fuel')
    km_driven=int(request.form.get('km'))

    prediction=model.predict(pd.DataFrame(columns=['model', 'company', 'year', 'km_driven', 'fuel_type'],
                              data=np.array([car_model,company,year,km_driven,fuel_type]).reshape(1, 5)))
    #print(prediction)

    return str(np.round(prediction[0],2))


'''@app.route('/buy_car',methods=['GET','POST'])
def buy_car():
    #ml=pickle.load(open('RandomForestModel.pkl','rb'))
    #maxp = utils.maxprice()
    smodels = scars.Model
    scompanies = scars.Company
    syears = scars.year
    skm = scars.km
    sfueltype = scars.Fueltype
    ssellingprice = scars.Sellingprice
    scarpics = scars.carpics
    ml=utils.mlprice


    car_models=sorted(car['model'].unique())
    mli = utils.mlpindex

    return render_template('buy.html',companies=scompanies, models=smodels, years=syears,fueltype=sfueltype,sellingprice=ssellingprice,kms=skm,carpix=scarpics,car_models=car_models,mlprices=ml,mlindex=mli)'''


@app.route('/cars',methods=['GET','POST'])
def cars():
    carsearch = ['hyundai','honda','audi','bmw','chevrolet','datsun','fiat','ford','jaguar','jeep','kia','mg','mercedes-benz','mini','maruti','mahindra','nissan','renault','skoda','tata','toyota','volkswagen','volvo',]
    carsearch.sort()
    smodels = scars.Model
    scompanies = scars.Company
    syears = scars.year
    skm = scars.km
    sfueltype = scars.Fueltype
    ssellingprice = scars.Sellingprice
    scarpics = scars.carpics
    ml=utils.mlprice
    


    car_models=sorted(car['model'].unique())
    mli = utils.mlpindex

   

    return render_template('cars.html',companies=scompanies, models=smodels, years=syears,fueltype=sfueltype,sellingprice=ssellingprice,kms=skm,carpix=scarpics,car_models=car_models,mlprices=ml,mlindex=mli,carsearch=carsearch)

@app.route('/userscraped',methods=['POST'])
def userscraped():
    selected_car=request.form.get('caroption')
    container = userscraper.getcontainers(selected_car)
    carpix = userscraper.getcarpix(selected_car)
    carkm = userscraper.getcarkms(selected_car)

    uscarpix =userscraper.getuscarpix(carpix)
    usyear=userscraper.getusyear(container)
    uscompany=userscraper.getuscompany(container)
    usmodel=userscraper.getusmodel(container)
    usprice=userscraper.getusprice(container)
    usfuel=userscraper.getusfuel(container)
    uscarkm=userscraper.getuskm(carkm)
    usmlpindex=userscraper.getusmlpindex(usmodel)
    usmlprice=userscraper.getusmlprice(uscompany,usmodel,usfuel,uscarkm,usmlpindex,usyear)
    

    car_models=sorted(car['model'].unique())
    

    return render_template('userscraper.html',companies=uscompany, models=usmodel, years=usyear,fueltype=usfuel,sellingprice=usprice,kms=uscarkm,carpix=uscarpix,car_models=car_models,mlprices=usmlprice,mlindex=usmlpindex,selected_car=selected_car)





@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__=="__main__":
    app.run()