import grpc
from concurrent import futures
import redis
import noblePrize_pb2
import noblePrize_pb2_grpc
import json

# Redis client setup
r = redis.StrictRedis(
  host='redis-19095.c259.us-central1-2.gce.redns.redis-cloud.com',
  port=19095,
  password='1TyE0QHjs23zaeIsAoVitZ3WnzmIM3UB')

class NobelPrizesServiceServicer(noblePrize_pb2_grpc.NobelPrizesServiceServicer):
    
    def GetLaureatesByCategoryAndYear(self, request, context):
        # Redis query logic to count laureates in a category between years
        # Assuming Redis has appropriate data indexed from Task 1
        category = request.category
        start_year = request.start_year
        end_year = request.end_year
        count = r.ft('prizeIdx1').search(f'@category:{category} @year:[{start_year} {end_year}]').total
        
        return noblePrize_pb2.LaureateCountResponse(count=count)
    
    def GetLaureatesByMotivationKeyword(self, request, context):
        keyword = request.keyword
        count = r.ft('prizeIdx1').search(f'@laureates_motivation:*{keyword}*').total
        
        return noblePrize_pb2.LaureateCountResponse(count=count)
    
    def GetLaureateInfoByName(self, request, context):
        first_name = request.first_name
        last_name = request.last_name
        # Perform Redis query for first and last name to retrieve laureate details
        query_result = r.ft('prizeIdx1').search(f'@laureates_name:{first_name} @laureates_surname:{last_name}')
       
        if query_result.total == 0:
            return noblePrize_pb2.LaureateInfoResponse()
        
        laureate = json.loads(query_result.docs[0].json)
        return noblePrize_pb2.LaureateInfoResponse(
            year=laureate['year'],
            category=laureate['category'],
            motivation=laureate['laureates'][0]['motivation']
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    noblePrize_pb2_grpc.add_NobelPrizesServiceServicer_to_server(NobelPrizesServiceServicer(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
