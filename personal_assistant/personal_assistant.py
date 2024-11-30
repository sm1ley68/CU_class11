import json
import os
import csv
from datetime import datetime
import logging

def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Сохранение данных в файл
def save_data(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Импорт и экспорт данных CSV
def export_to_csv(data, file_name, fields):
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
        print(f"Данные успешно экспортированы в {file_name}")
    except Exception as e:
        logging.error(f"Ошибка при экспорте данных в {file_name}: {e}")
        print("Произошла ошибка при экспорте данных.")

def import_from_csv(file_name, fields, model_class):
    try:
        data = []
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(model_class(**{field: row[field] for field in fields}))
        return data
    except Exception as e:
        logging.error(f"Ошибка при импорте данных из {file_name}: {e}")
        print("Произошла ошибка при импорте данных.")
        return []

# Заметки
class Note:
    def __init__(self, title, content):
        self.id = None
        self.title = title
        self.content = content
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }

def create_note():
    title = input("Введите заголовок заметки: ")
    content = input("Введите содержимое заметки: ")
    note = Note(title, content)
    notes = load_data('notes.json')
    note.id = len(notes) + 1
    notes.append(note.to_dict())
    save_data('notes.json', notes)
    print("Заметка успешно добавлена!")

def list_notes():
    notes = load_data('notes.json')
    if notes:
        for note in notes:
            print(f"ID: {note['id']} | Заголовок: {note['title']} | Дата: {note['timestamp']}")
    else:
        print("Нет сохранённых заметок.")

def view_note():
    note_id = int(input("Введите ID заметки: "))
    notes = load_data('notes.json')
    note = next((note for note in notes if note['id'] == note_id), None)
    if note:
        print(f"Заголовок: {note['title']}\nСодержимое: {note['content']}\nДата: {note['timestamp']}")
    else:
        print("Заметка не найдена.")

def edit_note():
    note_id = int(input("Введите ID заметки для редактирования: "))
    notes = load_data('notes.json')
    note = next((note for note in notes if note['id'] == note_id), None)
    if note:
        note['title'] = input("Введите новый заголовок: ")
        note['content'] = input("Введите новое содержимое: ")
        note['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        save_data('notes.json', notes)
        print("Заметка успешно обновлена!")
    else:
        print("Заметка не найдена.")

def delete_note():
    note_id = int(input("Введите ID заметки для удаления: "))
    notes = load_data('notes.json')
    notes = [note for note in notes if note['id'] != note_id]
    save_data('notes.json', notes)
    print("Заметка удалена.")

# Задачи
class Task:
    def __init__(self, title, description, priority, due_date):
        self.id = None
        self.title = title
        self.description = description
        self.done = False
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date
        }

def create_task():
    title = input("Введите краткое описание задачи: ")
    description = input("Введите подробное описание задачи: ")
    priority = input("Введите приоритет (Высокий, Средний, Низкий): ")
    due_date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")
    task = Task(title, description, priority, due_date)
    tasks = load_data('tasks.json')
    task.id = len(tasks) + 1
    tasks.append(task.to_dict())
    save_data('tasks.json', tasks)
    print("Задача успешно добавлена!")

def list_tasks():
    tasks = load_data('tasks.json')
    if tasks:
        for task in tasks:
            print(f"ID: {task['id']} | Название: {task['title']} | Приоритет: {task['priority']} | Дата выполнения: {task['due_date']} | Статус: {'Выполнена' if task['done'] else 'Не выполнена'}")
    else:
        print("Нет сохранённых задач.")

def mark_task_done():
    task_id = int(input("Введите ID задачи, чтобы отметить как выполненную: "))
    tasks = load_data('tasks.json')
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['done'] = True
        save_data('tasks.json', tasks)
        print("Задача отмечена как выполненная!")
    else:
        print("Задача не найдена.")

def edit_task():
    task_id = int(input("Введите ID задачи для редактирования: "))
    tasks = load_data('tasks.json')
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['title'] = input("Введите новое описание задачи: ")
        task['description'] = input("Введите новое подробное описание задачи: ")
        task['priority'] = input("Введите новый приоритет (Высокий, Средний, Низкий): ")
        task['due_date'] = input("Введите новый срок выполнения (ДД-ММ-ГГГГ): ")
        save_data('tasks.json', tasks)
        print("Задача успешно обновлена!")
    else:
        print("Задача не найдена.")

def delete_task():
    task_id = int(input("Введите ID задачи для удаления: "))
    tasks = load_data('tasks.json')
    tasks = [task for task in tasks if task['id'] != task_id]
    save_data('tasks.json', tasks)
    print("Задача удалена.")

# Контакты
class Contact:
    def __init__(self, name, phone, email):
        self.id = None
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

def create_contact():
    name = input("Введите имя контакта: ")
    phone = input("Введите номер телефона: ")
    email = input("Введите email: ")
    contact = Contact(name, phone, email)
    contacts = load_data('contacts.json')
    contact.id = len(contacts) + 1
    contacts.append(contact.to_dict())
    save_data('contacts.json', contacts)
    print("Контакт успешно добавлен!")

def list_contacts():
    contacts = load_data('contacts.json')
    if contacts:
        for contact in contacts:
            print(f"ID: {contact['id']} | Имя: {contact['name']} | Телефон: {contact['phone']} | Email: {contact['email']}")
    else:
        print("Нет сохранённых контактов.")

def search_contact():
    search_term = input("Введите имя или номер телефона для поиска: ")
    contacts = load_data('contacts.json')
    results = [contact for contact in contacts if search_term in contact['name'] or search_term in contact['phone']]
    if results:
        for contact in results:
            print(f"ID: {contact['id']} | Имя: {contact['name']} | Телефон: {contact['phone']} | Email: {contact['email']}")
    else:
        print("Контакт не найден.")

def edit_contact():
    contact_id = int(input("Введите ID контакта для редактирования: "))
    contacts = load_data('contacts.json')
    contact = next((contact for contact in contacts if contact['id'] == contact_id), None)
    if contact:
        contact['name'] = input("Введите новое имя: ")
        contact['phone'] = input("Введите новый телефон: ")
        contact['email'] = input("Введите новый email: ")
        save_data('contacts.json', contacts)
        print("Контакт успешно обновлён!")
    else:
        print("Контакт не найден.")

def delete_contact():
    contact_id = int(input("Введите ID контакта для удаления: "))
    contacts = load_data('contacts.json')
    contacts = [contact for contact in contacts if contact['id'] != contact_id]
    save_data('contacts.json', contacts)
    print("Контакт удалён.")

# Финансовые записи
class FinanceRecord:
    def __init__(self, amount, category, date, description):
        self.id = None
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

def create_finance_record():
    amount = float(input("Введите сумму операции: "))
    category = input("Введите категорию (например, Еда, Транспорт, Зарплата): ")
    date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
    description = input("Введите описание операции: ")
    record = FinanceRecord(amount, category, date, description)
    finance_records = load_data('finance.json')
    record.id = len(finance_records) + 1
    finance_records.append(record.to_dict())
    save_data('finance.json', finance_records)
    print("Финансовая запись успешно добавлена!")

def list_finance_records():
    finance_records = load_data('finance.json')
    if finance_records:
        for record in finance_records:
            print(f"ID: {record['id']} | Сумма: {record['amount']} | Категория: {record['category']} | Дата: {record['date']} | Описание: {record['description']}")
    else:
        print("Нет сохранённых финансовых записей.")

def calculate_balance():
    finance_records = load_data('finance.json')
    balance = sum(record['amount'] for record in finance_records)
    print(f"Общий баланс: {balance}")

def filter_finance_by_category():
    category = input("Введите категорию для фильтрации: ")
    finance_records = load_data('finance.json')
    filtered = [record for record in finance_records if record['category'] == category]
    if filtered:
        for record in filtered:
            print(f"ID: {record['id']} | Сумма: {record['amount']} | Категория: {record['category']} | Дата: {record['date']} | Описание: {record['description']}")
    else:
        print("Нет записей по этой категории.")

# Калькулятор
def calculator():
    while True:
        try:
            expression = input("Введите выражение (например, 5 + 3) или 'выход' для выхода: ")
            if expression.lower() == 'выход':
                break
            result = eval(expression)
            print(f"Результат: {result}")
        except Exception as e:
            print(f"Ошибка: {e}")

# Главное меню
def main_menu():
    while True:
        print("""
        Добро пожаловать в Персональный помощник!
        Выберите действие:
        1. Управление заметками
        2. Управление задачами
        3. Управление контактами
        4. Управление финансовыми записями
        5. Калькулятор
        6. Экспорт заметок в CSV
        7. Импорт заметок из CSV
        8. Выход
                """)
        choice = input("Введите номер действия: ")
        try:
            if choice == '1':
                notes_menu()
            elif choice == '2':
                task_menu()
            elif choice == '3':
                contacts_menu()
            elif choice == '4':
                finance_menu()
            elif choice == '5':
                calculator()
            elif choice == '6':
                export_to_csv()
            elif choice == '7':
                import_from_csv()
            elif choice == '8':
                print("Выход из программы...")
                break
            else:
                print("Неверный выбор, попробуйте снова.")
        except Exception as e:
            logging.error(f"Ошибка в главном меню: {e}")
            print("Произошла ошибка. Попробуйте снова.")

# Меню для работы с заметками
def note_menu():
    while True:
        print("""
        1. Создать заметку
        2. Просмотр заметок
        3. Просмотр заметки
        4. Редактировать заметку
        5. Удалить заметку
        6. Назад в главное меню
        """)
        choice = input("Выберите действие: ")
        try:
            if choice == '1':
                create_note()
            elif choice == '2':
                list_notes()
            elif choice == '3':
                view_note()
            elif choice == '4':
                edit_note()
            elif choice == '5':
                delete_note()
            elif choice == '6':
                break
            else:
                print("Неверный выбор, попробуйте снова.")

        except Exception as e:
            logging.error(f"Ошибка в меню заметок: {e}")
            print("Произошла ошибка в меню заметок.")


# Меню для работы с задачами
def task_menu():
    while True:
        print("""
        1. Создать задачу
        2. Просмотр задач
        3. Отметить задачу как выполненную
        4. Редактировать задачу
        5. Удалить задачу
        6. Назад в главное меню
        """)
        choice = input("Выберите действие: ")
        if choice == '1':
            create_task()
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            mark_task_done()
        elif choice == '4':
            edit_task()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            break
        else:
            print("Неверный выбор, попробуйте снова.")

# Меню для работы с контактами
def contact_menu():
    while True:
        print("""
        1. Создать контакт
        2. Просмотр контактов
        3. Поиск контакта
        4. Редактировать контакт
        5. Удалить контакт
        6. Назад в главное меню
        """)
        choice = input("Выберите действие: ")
        if choice == '1':
            create_contact()
        elif choice == '2':
            list_contacts()
        elif choice == '3':
            search_contact()
        elif choice == '4':
            edit_contact()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            break
        else:
            print("Неверный выбор, попробуйте снова.")

# Меню для работы с финансовыми записями
def finance_menu():
    while True:
        print("""
        1. Добавить финансовую запись
        2. Просмотр финансовых записей
        3. Подсчитать общий баланс
        4. Фильтровать по категории
        5. Назад в главное меню
        """)
        choice = input("Выберите действие: ")
        if choice == '1':
            create_finance_record()
        elif choice == '2':
            list_finance_records()
        elif choice == '3':
            calculate_balance()
        elif choice == '4':
            filter_finance_by_category()
        elif choice == '5':
            break
        else:
            print("Неверный выбор, попробуйте снова.")

# Запуск приложения
if __name__ == "__main__":
    main_menu()
