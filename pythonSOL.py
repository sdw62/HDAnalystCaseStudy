import pandas as pd 
import numpy as np
import math

# IMPORT DATA 

data = pd.ExcelFile("C:/Users/Samue/iCloudDrive/Home Depot Problem/ASC.xlsx")
hammerInfo = data.parse(0)
prodInfo = data.parse(1)
shippingRates = data.parse(2)
histOrders = data.parse(3)

# VARIABLE DEFINITIONS 

numWeeks = 52
yearIndex = 1
yearlyIncrease = 0.1
yearScaler = (1 + yearlyIncrease) ** (yearIndex)
hammerCostA = hammerInfo.iat[0,0]
hammerCostB = hammerInfo.iat[1,0]

# Since the price of shipment with carrier Y varies with weight we can calculate a cutoff weight for which carrier X becomes more profitable than carrier Y.   

r1CutOff = shippingRates.iat[0,3] / shippingRates.iat[4,3] 
r2CutOff = shippingRates.iat[1,3] / shippingRates.iat[5,3]
r3CutOff = shippingRates.iat[2,3] / shippingRates.iat[6,3]
r4CutOff = shippingRates.iat[3,3] / shippingRates.iat[7,3]

prod1Weight = prodInfo.iat[0,3]
prod2Weight = prodInfo.iat[1,3]
prod3Weight = prodInfo.iat[2,3]
prod4Weight = prodInfo.iat[3,3]

numHammers = 0
transportSumA = 0

# This loops over the weeks and calculates the shipment weight for each supplier/store pair. The cutoff values are used to choose the carrier for each pair. 
# Once the carrier is chosen, the transportation cost are calculated and are added to the annual transportation sum. The total hammer quantity is calculated 
# using the fact that hammer production is equal to wrench production. This for loop is for model A (hammers are produced via supplier A).

for weekIndex in range(1, numWeeks + 1):
    orderQuantity = histOrders[(weekIndex - 1) * 6 : weekIndex * 6]
    r1 = (prod1Weight * orderQuantity.iat[0,4] + prod2Weight * orderQuantity.iat[1,4] + prod4Weight * orderQuantity.iat[0,4]) * yearScaler
    r2 = (prod1Weight * orderQuantity.iat[2,4] + prod2Weight * orderQuantity.iat[3,4] + prod4Weight * orderQuantity.iat[2,4]) * yearScaler
    r3 = (prod3Weight * orderQuantity.iat[4,4]) * yearScaler
    r4 = (prod3Weight * orderQuantity.iat[5,4]) * yearScaler
    numHammers += math.ceil((orderQuantity.iat[0,4] + orderQuantity.iat[2,4]) * yearScaler)

    if (0 <= r1 <= r1CutOff):
        transportSumA += r1 * shippingRates.iat[4,3]
    else: 
        transportSumA += shippingRates.iat[0,3]

    if (0 <= r2 <= r2CutOff):
        transportSumA += r2 * shippingRates.iat[5,3]
    else: 
        transportSumA += shippingRates.iat[1,3]
    
    if (0 <= r3 <= r3CutOff):
        transportSumA += r3 * shippingRates.iat[6,3]
    else: 
        transportSumA += shippingRates.iat[2,3]

    if (0 <= r4 <= r4CutOff):
        transportSumA += r4 * shippingRates.iat[7,3]
    else: 
        transportSumA += shippingRates.iat[3,3]

hammerProdCostA = hammerCostA * numHammers
hammerProdCostB = hammerCostB * numHammers
totalCostA = transportSumA + hammerProdCostA
transportSumB = 0

# This for loop is for model B (hammers are produced via supplier B).

for weekIndex in range(1, numWeeks + 1):
    orderQuantity = histOrders[(weekIndex - 1) * 6 : weekIndex * 6]
    r1 = (prod1Weight * orderQuantity.iat[0,4] + prod2Weight * orderQuantity.iat[1,4]) * yearScaler
    r2 = (prod1Weight * orderQuantity.iat[2,4] + prod2Weight * orderQuantity.iat[3,4]) * yearScaler
    r3 = (prod3Weight * orderQuantity.iat[4,4] + prod4Weight * orderQuantity.iat[0,4]) * yearScaler
    r4 = (prod3Weight * orderQuantity.iat[5,4] + prod4Weight * orderQuantity.iat[2,4]) * yearScaler

    if (0 <= r1 <= r1CutOff):
        transportSumB += r1 * shippingRates.iat[4,3]
    else: 
        transportSumB += shippingRates.iat[0,3]

    if (0 <= r2 <= r2CutOff):
        transportSumB += r2 * shippingRates.iat[5,3]
    else: 
        transportSumB += shippingRates.iat[1,3]
    
    if (0 <= r3 <= r3CutOff):
        transportSumB += r3 * shippingRates.iat[6,3]
    else: 
        transportSumB += shippingRates.iat[2,3]

    if (0 <= r4 <= r4CutOff):
        transportSumB += r4 * shippingRates.iat[7,3]
    else: 
        transportSumB += shippingRates.iat[3,3]

totalCostB = transportSumB + hammerProdCostB

results = np.array([[transportSumA, hammerProdCostA, totalCostA], [transportSumB, hammerProdCostB, totalCostB]])
columnLabels = ["Transport Cost", "Production Cost", "Total Cost"]
rowLabels = ["Supplier A", "Supplier B"]
res = pd.DataFrame(results, rowLabels, columnLabels)
print(res)

