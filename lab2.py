import requests
import boto3
import matplotlib.pyplot as plt

api_url = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=desc&json"
api_url2 = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=desc&json"
result1 = requests.get(api_url).json()
result2 = requests.get(api_url2).json()
s3 = boto3.client('s3')
bucket = 'lab2.zabolotnyi'

files = []
for result in [result1, result2]:
    file_data = ",".join(str(header) for header in result[0].keys()) + "\n"
    for data in result:
        file_data += ",".join(str(row) for row in data.values()) + "\n"
    files.append(file_data)
s3.put_object(Bucket=bucket, Key='usd.csv', Body=files[0])
s3.put_object(Bucket=bucket, Key='eur.csv', Body=files[1])
for file in ['usd', 'eur']:
    data = s3.get_object(Bucket=bucket, Key=f'{file}.csv')['Body'].read().decode()
    data = str(data).split('\n')
    date = []
    rate = []
    for i in range(1, len(data) - 1):
        row = data[i].split(',')
        date.append(row[0])
        rate.append(float(row[5]))
    plt.plot(date, rate, label=file)

plt.xlabel('Date')
plt.ylabel('Rate')

plt.legend()
plt.savefig('rate.png', format='png')
plt.show()

with open('rate.png', 'rb') as f:
    file = f.read()
    s3.put_object(Bucket=bucket, Key='rate.png', Body=file)
    f.close()
