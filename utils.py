import numpy as np
import pandas as pd
import pickle

model=pickle.load(open('rfmodel.pkl','rb'))
scars = pd.read_csv("scrapedcars.csv")
car = pd.read_csv("Cleaned_cardekho.csv")

car_models=sorted(car['model'].unique())
#print(car_models)

smodels = scars.Model
scompanies = scars.Company
syears = scars.year
skm = scars.km
sfueltype = scars.Fueltype
ssellingprice = scars.Sellingprice


#print(smodels)

def maxprice(k):
    prediction = model.predict(pd.DataFrame(columns=['model', 'company', 'year', 'km_driven', 'fuel_type'],
                              data=np.array([smodels[k],scompanies[k],syears[k],skm[k],sfueltype[k]]).reshape(1, 5)))

    return(int(np.round(prediction[0],2)))

mlpindex = []
for i,Model in enumerate(smodels):
    if Model in car_models:
        mlpindex.append(i)

#print(mlpindex)

mlprice = {}
for i in mlpindex:
    mlprice[i]=maxprice(i)

#print(mlprice)

#print(maxp(6),type(maxp(6)))

'''if 'MG Hector Sharp DCT' in car_models:
    print('true')
else:
    print('false')'''