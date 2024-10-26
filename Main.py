import redis
import json

# Connect to Redis Cloud
r = redis.StrictRedis(
  host='redis-19095.c259.us-central1-2.gce.redns.redis-cloud.com',
  port=19095,
  password='1TyE0QHjs23zaeIsAoVitZ3WnzmIM3UB')


with open('prize.json', 'r') as f:
    data = json.load(f)

# Insert data into Redis Cloud
for idx, prize in enumerate(data['prizes']):
    key = f"prizes:{idx+1}"
    prize['year'] = int(prize['year'])
    r.json().set(key, '.', prize)  # Store each prize as JSON
