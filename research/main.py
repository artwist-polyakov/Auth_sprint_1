from uuid import uuid4

from research.elastic_tests import load_data
from research.mongo_tests import find_data, insert_document

ITERATIONS = 10
N_ROW = 1000


if __name__ == '__main__':
    time_mongo_load = 0
    for i in range(ITERATIONS):
        data = [{"id": str(uuid4()), "value": f"Example text {i}"} for i in range(N_ROW)]
        load_data_mongo, time = insert_document(data=data)
        time_mongo_load += time
    print(f'Среднее время записи данных в МОНГО в сак.'
          f'({N_ROW} - строк | {ITERATIONS} - итераций): '
          f'{time_mongo_load / ITERATIONS}')

    time_mongo_found = 0
    for i in range(ITERATIONS):
        found_data_mongo, time = find_data(condition={}, multiple=True)
        time_mongo_found += time
    print(f'Среднее время чтения данных из МОНГО в сак.'
          f'({N_ROW} - строк | {ITERATIONS} - итераций): '
          f'{time_mongo_found / ITERATIONS}')

    # time_elastic_load = 0
    # for i in range(ITERATIONS):
    #     data = [{"id": str(uuid4()), "value": f"Example text {i}"} for i in range(N_ROW)]
    #     time = load_data(data)
    #     time_elastic_load += time
    # print(f'Среднее время записи данных в ELASTIC в сак.'
    #       f'({N_ROW} - строк | {ITERATIONS} - итераций): '
    #       f'{time_elastic_load / ITERATIONS}')
    #
    # time_elastic_read = 0
    # for i in range(ITERATIONS):
    #     time = 0.1
    #     time_elastic_read += time
    # print(f'Среднее время чтения данных из ELASTIC в сак.'
    #       f'({N_ROW} - строк | {ITERATIONS} - итераций): '
    #       f'{time_elastic_read / ITERATIONS}')
