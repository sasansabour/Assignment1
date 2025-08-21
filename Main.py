import os
import redis
import json

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 19095))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Connect to Redis Cloud
r = redis.StrictRedis(
  host=REDIS_HOST,
  port=REDIS_PORT,
  password=REDIS_PASSWORD)


with open('prize.json', 'r') as f:
    data = json.load(f)

# Insert data into Redis Cloud
for idx, prize in enumerate(data['prizes']):
    key = f"prizes:{idx+1}"
    prize['year'] = int(prize['year'])
    r.json().set(key, '.', prize)  # Store each prize as JSON
