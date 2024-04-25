from uuid import uuid4

from elastic_tests import load_data, read_data
from mongo_tests import find_data, insert_documents_in_batches

ITERATIONS = 10
N_ROW = 10000


if __name__ == '__main__':

    print('MONGO')

    time_mongo_load = 0
    for i in range(ITERATIONS):
        data = [{"id": str(uuid4()), "value": f"Example text {i}"} for i in range(N_ROW)]
        load_data_mongo, time = insert_documents_in_batches(
            data=data,
            batch_size=int(N_ROW / ITERATIONS)
        )
        time_mongo_load += time
    print(f'Среднее время записи в сек.'
          f'({N_ROW} - строк | {ITERATIONS} - итераций): '
          f'{time_mongo_load / ITERATIONS}')

    time_mongo_found = 0
    found_data_mongo, time = find_data(condition={}, multiple=True)
    time_mongo_found += time
    print(f'Среднее время чтения в сек.'
          f'({N_ROW * ITERATIONS} - строк): '
          f'{time_mongo_found / ITERATIONS}')

    print('ELASTIC')

    time_elastic_load = 0
    for i in range(ITERATIONS):
        data = [{"id": str(uuid4()), "value": f"Example text {i}"} for i in range(N_ROW)]
        time = load_data(data, batch_size=int(N_ROW / ITERATIONS))
        time_elastic_load += time
    print(f'Среднее время записи в сек.'
          f'({N_ROW} - строк | {ITERATIONS} - итераций): '
          f'{time_elastic_load / ITERATIONS}')

    time_elastic_read = 0
    read_data_elastic, time = read_data()
    time_elastic_read += time
    print(f'Среднее время чтения в сек.'
          f'({N_ROW * ITERATIONS} - строк): '
          f'{time_elastic_read / ITERATIONS}')
