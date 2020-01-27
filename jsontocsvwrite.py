import pandas as pd
df = pd.read_json('realselfhundredrecenttweets.json')
df.to_csv('op.csv')
