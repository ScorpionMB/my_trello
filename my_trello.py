# from trello import TrelloApi

# api_key = '6247f05b0e98c620165ffca9048210f5'
# token = '715f33088c7ac6f870c20300ca47528f3e631bfb30eb174f29088ef8b6de9c34'
# trello = TrelloApi(api_key, token)
# response = trello.boards.new('Created with API')
# board_id = response['id']
# # print(response)
# # print(board_id)

# for column in trello.boards.get_list(board_id):
#     if 'Нужно' in column['name']:
#         list_id = column['id']
#         print(trello.lists.get_card(list_id))

# card = trello.cards.new('Научиться использовать Trello API', list_id)
# print(card)
import sys
import requests
import json

auth_params = {
    'key': "6247f05b0e98c620165ffca9048210f5",
    'token': "715f33088c7ac6f870c20300ca47528f3e631bfb30eb174f29088ef8b6de9c34"
}

base_url = "https://api.trello.com/1/{}" 
board_id = "fBJ6jo2L" 

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json() 

# Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])

def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

#Функция удаления задачи
def delete_task(name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        # if column['name'] == column_name:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()       
        for task in task_data:
            # print(task)
            if task['name'] == name:
                print(task['name'], task['id'])      
                # Удалим задачу с именем _name_ в найденной колонке
                requests.delete(base_url.format('cards') + '/' + task['id'], params=auth_params)
                break

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
            
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                break    
        if task_id:
            break
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break    

if __name__ == "__main__":
    if len(sys.argv) <= 2:      
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'delete_task':
        delete_task(sys.argv[2])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])


