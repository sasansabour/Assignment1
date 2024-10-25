import redis
#from redis.commands.json.path import Path
#import requests
import json

# Connect to Redis Cloud
r = redis.StrictRedis(
  host='redis-19095.c259.us-central1-2.gce.redns.redis-cloud.com',
  port=19095,
  password='1TyE0QHjs23zaeIsAoVitZ3WnzmIM3UB')


# Load the JSON data (you may load it from the file prize.json)
with open('/Users/sasan/Downloads/University/PhD/Term10/Programming On the Cloud/Assignment1/prize.json', 'r') as f:
    data = json.load(f)

# Insert data into Redis Cloud
for idx, prize in enumerate(data['prizes']):
    key = f"prizes:{idx+1}"
    prize['year'] = int(prize['year'])
    #for laureate in enumerate(prize['laureates']):
    #    laureate['id']=int(laureate[id]['id'])
    #    laureate['share']=int(laureate[id]['share'])
    r.json().set(key, '.', prize)  # Store each prize as JSON
    #print(f"Inserted {key}")


# Fetch Nobel Prize data
#response = requests.get('https://api.nobelprize.org/v1/prize.json')
#data = response.json()
#print(data)
#r.set('prizes', json.dumps(data))

# Insert each prize into Redis
#for prize in data['prizes']:
#    print(prize)
#    prize_id = f"{prize['year']}_{prize['category']}"  # Unique key based on year and category
#    r.set(f'prizes:{prize_id}', '.', json.dumps(prize))  # Store the prize data as JSON
#r.set('d2', json.dumps(jane))


# Load data into Redis
#for prize in data['prizes']:
#    r.json().set(f'prizes:{prize["id"]}', '.', prize)    

