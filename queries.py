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

# Query 1: Total number of laureates in a category within a year range
def get_total_laureates_by_category_and_year(category, start_year, end_year):
    query = f'@category:{{{category}}} @year:[{start_year} {end_year}]'
    result = r.ft("prizeIdx1").search(query)
    total_laureates = sum([len(prize['$.laureates']) for prize in result.docs])
    print(f"Total laureates in category '{category}' from {start_year} to {end_year}: {total_laureates}")
    return total_laureates


# Query 2: Total laureates with motivation covering a keyword
def get_total_laureates_by_motivation_keyword(keyword):
    query = f'@laureates_motivation:{keyword}'
    result = r.ft("prizeIdx1").search(query)

    total_laureates = 0
    for doc in result.docs:
        laureates = json.loads(doc.json)['laureates']
        total_laureates += len(laureates)

    print(f"Total laureates with motivation containing keyword '{keyword}': {total_laureates}")
    return total_laureates


# Query 3: Get year, category, and motivation given a laureate's first and last name
def get_laureate_info_by_name(first_name, last_name):
    query = f'@laureates_name:{first_name} @laureates_surname:{last_name}'
    result = r.ft("prizeIdx1").search(query)
    
    if len(result.docs) > 0:
        for doc in result.docs:
            doc_data = json.loads(doc.json)
            year = doc_data['year']
            category = doc_data['category']
            for laureate in doc_data['laureates']:
                if laureate['firstname'] == first_name and laureate['surname'] == last_name:
                    motivation = laureate['motivation']
                    print(f"Year: {year}, Category: {category}, Motivation: {motivation}")
                    return year, category, motivation
    else:
        print(f"No laureate found with the name {first_name} {last_name}")
        return None


# Test the client with some queries
if __name__ == "__main__":
    # Query 1: Total number of laureates in 'economics' from 2013 to 2023
    get_total_laureates_by_category_and_year("economics", 2013, 2023)

    # Query 2: Total laureates with motivation covering the keyword 'protein'
    get_total_laureates_by_motivation_keyword("protein")

    # Query 3: Get the information of laureate "David Baker"
    get_laureate_info_by_name("David", "Baker")
