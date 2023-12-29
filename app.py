from convert import applyEncodingAndReturn
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import pandas as pd
from flask_cors import CORS
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor
import joblib


#---------------------------------Datayi cekiyoruz ve modeli olusturuyoruz.--------------------------------

egitim = pd.read_csv('train.csv')
#Burada kullanicidan alacagimiz ve otomatik verecegimiz ozelliklerin sirasini duzenliyorum. Bu islem yapilmazsa modeli egittikten fiyat alirken siralamanin uygumsuzluguyla ilgili hata verecektir.
first = egitim[['Id','MSZoning','BldgType','HeatingQC','YearBuilt',
  'Heating','KitchenQual','GarageCars','FullBath','SaleType','SaleCondition',]]
second = egitim.drop(['MSZoning','BldgType','HeatingQC','YearBuilt',
  'Heating','SaleCondition','KitchenQual','GarageCars','FullBath','SaleType'], axis =1)

egitim = pd.merge(first,second)

#egitim2'yi FrontEnd tarafina ozellik cekmek icin olusturdum.
egitim2 = pd.read_csv('train.csv')

#normal dagilim uygulyoruz.
#egitim['SalePrice'] = np.log1p(egitim['SalePrice'])

#Mesela PoolQC değeri yaklaşık %99 boş veriden oluşuyor  bunu None olarak dolduracağız.
egitim['PoolQC'] = egitim['PoolQC'].fillna('None')

#Özellikler içinde % 50 civarında eksik değer içierenleri None ile dolduracağız.
egitim['MiscFeature'] = egitim['MiscFeature'].fillna('None')
egitim['Alley'] = egitim['Alley'].fillna('None')
egitim['Fence'] = egitim['Fence'].fillna('None')
egitim['FireplaceQu'] = egitim['FireplaceQu'].fillna('None')

# Mahalleye göre gruplandıralım ve tüm değerleri medyan LotFrontage ile eksik değeri doldurun
egitim['LotFrontage'] = egitim.groupby("Neighborhood")["LotFrontage"].transform(
    lambda x: x.fillna(x.median()))

#GarageType, GarageFinish, GarageQual ve GarageCond bunlarıda none ile değiştirelim.
for col in ['GarageType', 'GarageFinish', 'GarageQual', 'GarageCond']:
    egitim[col] = egitim[col].fillna('None')

#GarageYrBlt, GarageArea ve GarageCars bunlarıda sıfır ile değiştirelim
for col in ['GarageYrBlt', 'GarageArea', 'GarageCars']:
    egitim[col] = egitim[col].fillna(int(0))

#BsmtFinType2, BsmtExposure, BsmtFinType1, BsmtCond, BsmtQual None ile değiştirelim
for col in ('BsmtFinType2', 'BsmtExposure', 'BsmtFinType1', 'BsmtCond', 'BsmtQual'):
    egitim[col] = egitim[col].fillna('None')


#MasVnrArea'yı da sıfır ile değiştirelim
egitim['MasVnrArea'] = egitim['MasVnrArea'].fillna(int(0))


  #MasVnrType  sütununu da None ile değiştirelim
egitim['MasVnrType'] = egitim['MasVnrType'].fillna('None')

#Mode Değerlerini ekledik.
egitim['Electrical'] = egitim['Electrical'].fillna(egitim['Electrical']).mode()[0]

#Utilities e de ihtiyacımız yok onuda atalım veri setimizden
egitim = egitim.drop(['Utilities'], axis =1)
egitim = egitim.drop(['Id'], axis =1 )

cols = ('FireplaceQu', 'BsmtQual', 'BsmtCond', 'GarageQual', 'GarageCond',
        'ExterQual', 'ExterCond','HeatingQC', 'PoolQC', 'KitchenQual', 'BsmtFinType1',
        'BsmtFinType2', 'Functional', 'Fence', 'BsmtExposure', 'GarageFinish', 'LandSlope',
        'LotShape', 'PavedDrive', 'Street', 'Alley', 'CentralAir', 'MSSubClass', 'OverallCond',
        'YrSold', 'MoSold', 'MSZoning', 'LandContour', 'LotConfig', 'Neighborhood',
        'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st',
        'Exterior2nd', 'MasVnrType', 'MasVnrArea', 'Foundation', 'GarageType', 'MiscFeature',
        'SaleType', 'SaleCondition', 'Electrical', 'Heating')

for c in cols:
    lbl = LabelEncoder()
    lbl.fit(list(egitim[c].values))
    egitim[c] = lbl.transform(list(egitim[c].values))

#Modelleme tamamlandı. Bundan sonra verileri tahminde bulunmak için hazırlanacak.
#Hedef değişkenimiz olan SalePrice değişkenini yeni bir değişkene yani y'ye atandı.
y = egitim['SalePrice']

#Tahmin edeceğiimiz hedef değişkeni artık veri setimizden sile biliriz
del egitim['SalePrice']

#Şimdi de verilerimizi eğitim ve test verileri olmak üzere ikiye ayırdık. (%80 eğitim, % 20 test)
X_train, X_test, y_train, y_test = train_test_split(egitim, y, test_size = 0.2, random_state = 7)

restOfData = X_test.drop(['MSZoning','BldgType','HeatingQC','YearBuilt',
'Heating','SaleCondition','KitchenQual','GarageCars','FullBath','SaleType',], axis =1)

restOfData = restOfData.iloc[[0]]
#---------------- Yukarida veri on isleme yapildi ve restOfData olusturuldu. ---------------------------


#----------Burada kullanicidan alacagim columnlari ve alt ozelliklerini secip bunlari frontend tarafina yollamak uzere birlestiriyorum--------

#json int64 yapisini serializable edemediginden tum verileri string yaptiyoruz.
egitim2 = egitim2.astype(str)
prop= egitim2[["MSZoning","BldgType","HeatingQC","YearBuilt","Heating",
"KitchenQual","GarageCars","FullBath","SaleType","SaleCondition"]]
properties = []
for i in range(len(prop.columns)):
  properties.append(list(prop[prop.columns[i]].unique()))
allProp = {prop.columns[i]: properties[i] for i in range(len(prop.columns))}


#adaBoost modelimizi .pkl dosyasindan buraya aktardik.
adaBoost_model = joblib.load("adaBoost.pkl")

#----------------------------Modeli olusturduk artik rest api kismina geciyoruz.-----------------------------
app = Flask(__name__)
CORS(app)
api = Api(app)


# secilen columnlari frontend'e yolluyoruz.
@app.route('/')
def getAll():
    return allProp

#Kullanicidan gelen veriler islenip frontend'e ev fiyati yolluyoruz.
@app.route('/', methods=['POST'])
def askForPrice():
    user_data= request.get_json()
    newData = applyEncodingAndReturn(user_data, restOfData)
    price = str(int(adaBoost_model.predict(newData)))
    return jsonify(price[0:3]+"."+price[3:6]+" $")


if __name__ == "__main__":
    app.run()
