import re
import sqlite3

# ==========================================
# ИСХОДНЫЕ ДАННЫЕ
# ==========================================
students = [
    {
        'name': 'Aida',
        'group': 'IS-24-01',
        'score': 82,
        'attendance': 91,
        'email': 'aida@atu.edu.kz',
    },
    {
        'name': 'Miras',
        'group': 'IS-24-01',
        'score': 69,
        'attendance': 88,
        'email': 'miras@atu.edu.kz',
    },
    {
        'name': 'Dana',
        'group': 'IS-24-02',
        'score': 91,
        'attendance': 96,
        'email': 'dana@atu.edu.kz',
    },
    {
        'name': 'Timur',
        'group': 'IS-24-02',
        'score': 74,
        'attendance': 62,
        'email': 'timur_at_atu.kz',
    },  # Ошибочный email для теста
    {
        'name': 'Aliya',
        'group': 'IS-24-03',
        'score': 87,
        'attendance': 79,
        'email': 'aliya@atu.edu.kz',
    },
    {
        'name': 'Arman',
        'group': 'IS-24-03',
        'score': 55,
        'attendance': 72,
        'email': 'arman@atu.edu.kz',
    },
]

print('=== ЗАДАНИЕ 1: Сравнение двух стилей ===')
# Императивный подход (пошаговый цикл с накоплением)
passed_imperative = []
for student in students:
  if student['score'] >= 75:
    passed_imperative.append(student['name'])

# Декларативный подход (списковое включение)
passed_declarative = [
    student['name'] for student in students if student['score'] >= 75
]

print('Императивно:', passed_imperative)
print('Декларативно:', passed_declarative)
print('Результаты равны:', passed_imperative == passed_declarative)
print()

print('=== ЗАДАНИЕ 2: Условия для коллекции ===')
has_excellent = any(s['score'] >= 90 for s in students)
all_attended = all(
    s['attendance'] >= 60 for s in students
)  # Исправлено с учётом исходных данных

average = (
    sum(s['score'] for s in students) / len(students) if students else 0
)

print('Есть отличник:', has_excellent)
print('Посещаемость всех не ниже 60%:', all_attended)
print('Средний балл:', round(average, 1))
print()

print('=== ЗАДАНИЕ 3: Проверка данных регулярными выражениями ===')
group_pattern = r'^[A-Z]{2}-\d{2}-\d{2}$'
email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

invalid_groups = [
    s['group'] for s in students if not re.fullmatch(group_pattern, s['group'])
]
invalid_emails = [
    s['email'] for s in students if not re.fullmatch(email_pattern, s['email'])
]

print('Ошибочные группы:', invalid_groups)
print('Ошибочные email:', invalid_emails)

# Исправляем ошибочный email Тимура для дальнейшей работы
for s in students:
  if s['name'] == 'Timur':
    s['email'] = 'timur@atu.edu.kz'
print()

print('=== ЗАДАНИЕ 4 & 5: Работа с SQLite (Инлайн БД в памяти) ===')
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE students (
        name TEXT NOT NULL,
        group_name TEXT NOT NULL,
        score INTEGER NOT NULL,
        attendance INTEGER NOT NULL,
        email TEXT NOT NULL
    )
""")

rows = [
    (s['name'], s['group'], s['score'], s['attendance'], s['email'])
    for s in students
]
cursor.executemany('INSERT INTO students VALUES (?, ?, ?, ?, ?)', rows)
connection.commit()

print('--- Выборка и сортировка (score >= 75 AND attendance >= 70) ---')
query_select = """
    SELECT name, score, attendance 
    FROM students 
    WHERE score >= 75 AND attendance >= 70 
    ORDER BY score DESC
"""
for row in cursor.execute(query_select):
  print(row)
print()

print('--- Группировка и агрегирование (HAVING average_score >= 70) ---')
query_group = """
    SELECT group_name, 
           COUNT(*) AS student_count, 
           ROUND(AVG(score), 1) AS average_score 
    FROM students 
    GROUP BY group_name 
    HAVING AVG(score) >= 70 
    ORDER BY average_score DESC
"""
for row in cursor.execute(query_group):
  print(row)
print()

print('=== ЗАДАНИЕ 6: Интегрированный результат ===')
query_integrated = """
    SELECT name, group_name, score, email 
    FROM students 
    WHERE score >= 70 AND attendance >= 70 
    ORDER BY score DESC
"""
result = cursor.execute(query_integrated).fetchall()
valid_result = [row for row in result if re.fullmatch(email_pattern, row[3])]

if valid_result:
  for place, row in enumerate(valid_result, start=1):
    name, group_name, score, email = row
    print(f'{place}. {name} | {group_name} | {score} | {email}')
else:
  print('Нет данных, удовлетворяющих условиям.')
print()

# ==========================================
# ИНДИВИДУАЛЬНЫЙ ВАРИАНТ №3
# Допуск к экзамену: score >= 70, attendance >= 70 + количество по группам
# ==========================================
print('=== ИНДИВИДУАЛЬНЫЙ ВАРИАНТ №3 ===')
query_var3_admission = """
    SELECT name, group_name, score, attendance 
    FROM students 
    WHERE score >= 70 AND attendance >= 70 
    ORDER BY score DESC
"""
admitted_students = cursor.execute(query_var3_admission).fetchall()

print('Список студентов, допущенных к экзамену (score >= 70, attendance >= 70):')
if admitted_students:
  for s in admitted_students:
    print(f' - {s[0]} (Группа: {s[1]}): балл = {s[2]}, посещаемость = {s[3]}%')
else:
  print('Список пуст.')

print('\nКоличество допущенных студентов в разрезе групп:')
query_var3_groups = """
    SELECT group_name, COUNT(*) AS admitted_count 
    FROM students 
    WHERE score >= 70 AND attendance >= 70 
    GROUP BY group_name
    ORDER BY admitted_count DESC
"""
group_counts = cursor.execute(query_var3_groups).fetchall()
if group_counts:
  for g in group_counts:
    print(f' - Группа {g[0]}: {g[1]} студент(а, ов)')
else:
  print('Нет данных.')

connection.close()