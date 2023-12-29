import pandas as pd
def applyEncodingAndReturn(deneme, oto):
    # once ozelliklerin karsilik encoding degerlerini bul ve hepsini degiskene aktar
    # yearBuilt, GarageCars, FullBath gelen degerler aynen yaziyoruz.

    MSZoning = {'RL': 1, 'RM': 2, 'C (all)': 3, 'FV': 4, 'RH': 0}
    for i in range(len(MSZoning)):
        if deneme['MSZoning'] == list(MSZoning.keys())[i]:
            deneme['MSZoning'] = list(MSZoning.values())[i]

    HeatingQC = {'Ex': 0, 'Gd': 2, 'TA': 4, 'Fa': 1, 'Po': 3}
    for i in range(len(HeatingQC)):
        if deneme['HeatingQC'] == list(HeatingQC.keys())[i]:
            deneme['HeatingQC'] = list(HeatingQC.values())[i]

    BldgType = {'1Fam': 0, '2fmCon': 1, 'Duplex': 2, 'TwnhsE': 4, 'Twnhs': 3}
    for i in range(len(BldgType)):
        if deneme['BldgType'] == list(BldgType.keys())[i]:
            deneme['BldgType'] = list(BldgType.values())[i]

    Heating = {'GasA': 1, 'GasW': 2, 'Grav': 3, 'Wall': 5, 'OthW': 4, 'Floor': 0}
    for i in range(len(Heating)):
        if deneme['Heating'] == list(Heating.keys())[i]:
            deneme['Heating'] = list(Heating.values())[i]

    KitchenQual = {'Gd': 2, 'TA': 3, 'Ex': 0, 'Fa': 1}
    for i in range(len(KitchenQual)):
        if deneme['KitchenQual'] == list(KitchenQual.keys())[i]:
            deneme['KitchenQual'] = list(KitchenQual.values())[i]

    SaleType = {'WD': 8, 'New': 6, 'COD': 0, 'ConLD': 3, 'ConLI': 4, 'CWD': 1, 'ConLw': 5, 'Con': 2, 'Oth': 7}
    for i in range(len(SaleType)):
        if deneme['SaleType'] == list(SaleType.keys())[i]:
            deneme['SaleType'] = list(SaleType.values())[i]

    SaleCondition = {'Normal': 4, 'Abnorml': 0, 'Partial': 5, 'AdjLand': 1, 'Alloca': 2, 'Family': 3}
    for i in range(len(SaleCondition)):
        if deneme['SaleCondition'] == list(SaleCondition.keys())[i]:
            deneme['SaleCondition'] = list(SaleCondition.values())[i]


    deneme = pd.Series(deneme).to_frame().T

    deneme_series = deneme.squeeze()
    restOfData_series = oto.squeeze()

    frames = [deneme_series, restOfData_series]
    result = pd.concat(frames)
    print(type(result))
    result = result.to_frame().T
    return result