import json
import pandas as pd

with open('option-chain-indices.json','r',encoding='utf-8') as file:
  data = json.load(file)

records = data['records']['data']
expiry_dates = data['records']['expiryDates']

print('Avaiable Expirires: ',expiry_dates)

desired_expiry = expiry_dates[0]
filtered = [r for r in records if r['expiryDate'] == desired_expiry]

rows = []

for r in filtered:
  strike = r['strikePrice']
  ce = r.get('CE', {})
  pe = r.get('PE', {})

  rows.append ({
    'Strike': strike,
    'Call_OI': ce.get('openInterest'),
    'Call_IV': ce.get('impliedVolatility'),
    'Call_Bid': ce.get('bidprice'),
    'Put_OI': pe.get('openInterest'),
    'Put_IV': pe.get('impliedVolatility'),
    'Put_Bid': pe.get('bidprice')
  })
    

df = pd.DataFrame(rows).sort_values(by='Strike')
print(df)

