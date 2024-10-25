import grpc
import noblePrize_pb2
import noblePrize_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = noblePrize_pb2_grpc.NobelPrizesServiceStub(channel)
        
        # Query 1: Laureates by category and year
        category_year_request = noblePrize_pb2.CategoryYearRequest(category="economics", start_year=2013, end_year=2023)
        response = stub.GetLaureatesByCategoryAndYear(category_year_request)
        print(f"Total laureates in economics (2013-2023): {response.count}")
        
        # Query 2: Laureates by motivation keyword
        keyword_request = noblePrize_pb2.KeywordRequest(keyword="protein")
        response = stub.GetLaureatesByMotivationKeyword(keyword_request)
        print(f"Total laureates with 'protein' in motivation: {response.count}")
        
        # Query 3: Laureate info by name
        name_request = noblePrize_pb2.NameRequest(first_name="David", last_name="Baker")
        response = stub.GetLaureateInfoByName(name_request)
        print(f"Year: {response.year}, Category: {response.category}, Motivation: {response.motivation}")

if __name__ == '__main__':
    run()
