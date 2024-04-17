from uuid import uuid4

# from research.elastic_tests import load_data
from research.mongo_tests import insert_document, find_data

N = 10000
# Загрузка данных
data = [{"id": str(uuid4()), "value": f"Example text {i}"} for i in range(N)]

# # Вызов функции для загрузки данных
# load_data(data)


if __name__ == '__main__':
    result_ids, time = insert_document(data=data)
    print(f'Запись {N} строк произведена в МОНГО: \nВремя в сек.: {time}')  #  \ndata: {result_ids}

    found_users, time = find_data(condition={}, multiple=True)
    print(f'Чтение {N} строк произведена из МОНГО: \nВремя в сек: {time}')  #  \ndata: {found_users}
