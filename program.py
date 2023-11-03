import psycopg2

# Підключення до сервера PostgreSQL
conn = psycopg2.connect(
    dbname="library_db",
    user="root",
    password="root",
    host="localhost",
    port="5432"
)

# Створення курсора для виконання SQL-запитів
cur = conn.cursor()

# Функція для виведення даних таблиці з вказаними назвами стовпців
def print_table(table_name, custom_columns):
    # Виведення назв стовпців
    columns = custom_columns

    cur.execute(f"SELECT * FROM {table_name};")
    data = cur.fetchall()

    print(f"\nTable: {table_name}")

    # Визначення максимальної ширини кожного стовпця
    column_widths = [max(len(col), max(len(str(row[i])) for row in data)) for i, col in enumerate(columns)]

    # Виведення назв стовпців
    print("|".join(columns[i].ljust(column_widths[i]) for i in range(len(columns))))

    # Додавання лінії після заголовків
    print("+".join("-" * (column_widths[i]) for i in range(len(columns))) + "-")

    # Виведення рядків
    for row in data:
        print("|".join(str(row[i]).ljust(column_widths[i]) for i in range(len(row))))

# Введення назв стовпців для кожної таблиці
columns_books = ["Інвентарний номер", "Автор", "Назва", "Розділ", "Рік", "Сторінки", "Ціна", "Тип", "Кількість копій", "Термін позики"]
columns_readers = ["Номер квитка", "Прізвище", "Ім'я", "Номер телефону", "Адреса", "Курс", "Група"]
columns_book_loans = ["Код видачі", "Дата видачі", "Інвентарний номер книги", "Номер квитка читача"]

# Виведення таблиць
print_table("books", columns_books)
print_table("readers", columns_readers)
print_table("book_loans", columns_book_loans)

#Запити
def print_query_result(query_name, columns_translation, result):
    if not result:
        print(f"\nРезультат запиту '{query_name}' порожній.")
        return

    columns = [desc[0] for desc in cur.description]
    columns_ukr = [columns_translation.get(col, col) for col in columns]
    column_widths = [max(len(col), max(len(str(row[i])) for row in result)) for i, col in enumerate(columns_ukr)]

    print(f"\nРезультат запиту '{query_name}':")
    for i, col in enumerate(columns_ukr):
        print(col.ljust(column_widths[i]), end="|")
    print()
    print("+".join("-" * width for width in column_widths))

    for row in result:
        for i, cell in enumerate(row):
            print(str(cell).ljust(column_widths[i]), end="|")
        print()



# Запит 1: Відобразити всі книги, які були видані після 2001 року. Відсортувати назви за алфавітом.
cur.execute("""
    SELECT * FROM Books
    WHERE year > 2001
    ORDER BY title;
""")
result = cur.fetchall()
columns_translation = {
    "inventory_number": "Інвентарний номер",
    "author": "Автор",
    "title": "Назва",
    "section": "Розділ",
    "year": "Рік",
    "pages": "Сторінки",
    "price": "Ціна",
    "type": "Тип",
    "copies": "Кількість копій",
    "max_loan_period": "Термін позики"
}
print_query_result("Запит 1", columns_translation, result)

# Запит 2: Порахувати кількість книг кожного виду (підсумковий запит)
cur.execute("""
    SELECT type, COUNT(*) as total_books
    FROM Books
    GROUP BY type;
""")
result = cur.fetchall()
columns_translation = {
    "type": "Тип",
    "total_books": "Загальна кількість"
}
print_query_result("Запит 2", columns_translation, result)

# Запит 3: Відобразити всіх читачів, які брали посібники в бібліотеці. Відсортувати прізвища за алфавітом.
cur.execute("""
SELECT 
    r.*, 
    bl.loan_code 
FROM 
    Readers r 
JOIN 
    Book_Loans bl 
ON 
    r.ticket_number = bl.reader_ticket 
WHERE 
    bl.book_inventory_number IN (SELECT DISTINCT inventory_number FROM Books WHERE type = 'Посібник') 
ORDER BY 
    r.last_name;
""")

result = cur.fetchall()
columns_translation = {
    "ticket_number": "Номер квитка",
    "last_name": "Прізвище",
    "first_name": "Ім'я",
    "phone_number": "Номер телефону",
    "address": "Адреса",
    "course": "Курс",
    "group_name": "Група",
    "loan_code": "Код позики"  # Додана нова назва
}
print_query_result("Запит 3", columns_translation, result)

# Запит 4: Відобразити всі книги за указаним розділом (запит з параметром)
section = 'Технічна'  # Параметр: розділ
cur.execute("""
    SELECT * FROM Books
    WHERE section = %s;
""", (section,))
result = cur.fetchall()
columns_translation = {
    "inventory_number": "Інвентарний номер",
    "author": "Автор",
    "title": "Назва",
    "section": "Розділ",
    "year": "Рік",
    "pages": "Сторінки",
    "price": "Ціна",
    "type": "Тип",
    "copies": "Кількість копій",
    "max_loan_period": "Термін позики"
}
print_query_result(f"Запит 4 (Розділ: {section})", columns_translation, result)

# Запит 5: Для кожної книги, яка була видана читачу, порахувати кінцевий термін її повернення в бібліотеку (запит з обчислювальним полем)
cur.execute("""
    SELECT Book_Loans.loan_code, Books.title, Book_Loans.loan_date as return_date, Book_Loans.loan_date + Books.max_loan_period as return_date_calc
    FROM Book_Loans
    JOIN Books ON Book_Loans.book_inventory_number = Books.inventory_number;
""")
result = cur.fetchall()
columns_translation = {
    "loan_code": "Код позики",
    "title": "Назва книги",
    "return_date": "Дата видачі",
    "return_date_calc": "Розрахункова дата повернення"
}
print_query_result("Запит 5", columns_translation, result)


# Запит 6: Порахувати кількість посібників, книг та періодичних видань в кожному розділі (перехресний запит)
cur.execute("""
    SELECT section, 
           SUM(CASE WHEN type = 'Посібник' THEN 1 ELSE 0 END) as total_manuals,
           SUM(CASE WHEN type = 'Книга' THEN 1 ELSE 0 END) as total_books,
           SUM(CASE WHEN type = 'Періодичне видання' THEN 1 ELSE 0 END) as total_periodicals
    FROM Books
    GROUP BY section;
""")

result = cur.fetchall()

columns_translation = {
    "section": "Розділ",
    "total_manuals": "Посібники",
    "total_books": "Книги",
    "total_periodicals": "Періодичні видання"
}

print_query_result("Запит 6", columns_translation, result)


# Закриття підключення
cur.close()
conn.close()
