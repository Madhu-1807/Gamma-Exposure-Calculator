import json
import pandas as pd
from math import log, sqrt, exp
from scipy.stats import norm
from datetime import datetime

# Load data

with open('option-chain-indices.json','r' ,encoding='utf-8') as file:
  data = json.load(file)

records = data['records']['data']
spot_price = float(data['records']['underlyingValue'])
expiry_dates = data['records']['expiryDates']
today = datetime.strptime(data['records']['timestamp'].split(' ')[0], '%d-%b-%Y')
expiry = datetime.strptime(expiry_dates[0], '%d-%b-%Y')

# Time to expiry in years

T = (expiry - today).days / 365

# Constants
risk_free_rate = 0.06
q = 0.00
lot_size = 75


# Extract and filter option chain data
filtered = [record for record in records if record['expiryDate'] == expiry_dates[0]]

#Compute Gamma Exposure
rows = []

for record in filtered:
  strike = record['strikePrice']
  ce = record.get('CE')
  if not ce:
    continue

  IV = ce.get('impliedVolatility')
  OI = ce.get('openInterest')
  if IV is None or OI is None:
    continue

  sigma = IV / 100

  try:
    d1 = (log(spot_price / strike) + (risk_free_rate + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    gamma = exp(-q * T) * norm.pdf(d1) / (spot_price * sigma * sqrt(T))
    gex = gamma * OI * lot_size * 100

    rows.append({
      'Strike': strike,
      'Call_IV': IV,
      'Call_OI': OI,
      'Gamma': gamma,
      'Gamma_Exposure': gex
    })
  except:
    continue

# Display Result

df = pd.DataFrame(rows)
print(df)
