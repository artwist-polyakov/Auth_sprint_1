from uuid import uuid4

# from research.elastic_tests import load_data
from research.mongo_tests import insert_document, find_data
ITERATIONS = 10
N = 10000


if __name__ == '__main__':
    time_mongo_load = 0
    for i in range(ITERATIONS):
        data = [{"id": str(uuid4()), "value": f"Example text {i}"} for i in range(N)]
        load_data_mongo, time = insert_document(data=data)
        time_mongo_load += time
    print(f'Среднее время записи данных ({ITERATIONS} - итераций) в МОНГО в сак.: {time_mongo_load / ITERATIONS}')

    time_mongo_found = 0
    for i in range(ITERATIONS):
        found_data_mongo, time = find_data(condition={}, multiple=True)
        time_mongo_found += time
    print(f'Среднее время чтения данных ({ITERATIONS} - итераций) из МОНГО в сак.: {time_mongo_load / ITERATIONS}')


    # time = load_data(data)
    # print(f'Запись {N} строк произведена в Эластик: \nВремя в сек.: {time}')

    # read_data, time = find_data(condition={}, multiple=True)
    # print(f'Чтение {N} строк произведена из МОНГО: \nВремя в сек: {time}')  #  \ndata: {found_users}

