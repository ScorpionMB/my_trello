import sys
import requests

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
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + ' | количество задач: ' + str(len(task_data)))     
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'] + ' | id: ' + task['id'])

def create_list(name):
    boards = requests.get(base_url.format('members') + '/' + 'user90428665' + '/boards', params=auth_params).json()
    requests.post(base_url.format('lists'), data={'name': name, 'pos': 'bottom','idBoard': boards[0]['id'], **auth_params})
    print('Колонка создана')

def create_task(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:
        if column['name'] == column_name:          
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            print('Задача создана')
            return
    # Создадим несуществующую колонку
    create_list(column_name)
    # Создадим задачу в созданной колонке
    create_task(name, column_name)
    

#Функция удаления задачи
def delete_task(name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None    
    list_task = []
    dict_task = {}
    key = 1
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()       
        for task in task_data:
            if task['name'] == name:
                task_id = task['id']
                dict_task[key] = task_id
                list_task.append('Задача: {} | Список: {} | id: {}'.format(task['name'], column['name'], key))
                key += 1
    if len(list_task) > 1:
        for i in list_task:
            print(i)
        id_input = input('Выберите id задачи: ')
        task_id = dict_task[int(id_input)]
        # Удалим задачу с именем _name_
    requests.delete(base_url.format('cards') + '/' + task_id, params=auth_params)
    print('Задача удалена')
            
def move_task(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
            
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    list_task = []
    dict_task = {}
    key = 1
    for column in column_data:    
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in task_data:
            if task['name'] == name:
                task_id = task['id']
                list_task.append('Задача: {} | Список: {} | id: {}'.format(task['name'], column['name'], key))
                key += 1
    if len(list_task) > 1:
        for i in list_task:
            print(i)
        id_input = input('Выберите id задачи: ')
        task_id = dict_task[int(id_input)]             
 
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            print('Задача перемещена')    

if __name__ == "__main__":
    if len(sys.argv) <= 2:      
        read()
    elif sys.argv[1] == 'create_task':
        create_task(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'delete_task':
        delete_task(sys.argv[2])
    elif sys.argv[1] == 'move_task':
        move_task(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_list':
        create_list(sys.argv[2])




