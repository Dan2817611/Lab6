import psycopg2

# Підключення до сервера PostgreSQL
conn = psycopg2.connect(
    dbname="library_db",
    user="root",
    password="root",
    host="localhost",  # Адреса сервера PostgreSQL
    port="5432"
)

# Створення курсора для виконання SQL-запитів
cur = conn.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS Books (
        inventory_number INT PRIMARY KEY,
        author VARCHAR(255),
        title VARCHAR(255),
        section VARCHAR(255) CHECK (section IN ('Технічна', 'Художня', 'Економічна')),
        year INT,
        pages INT,
        price DECIMAL(10,2),
        type VARCHAR(255) CHECK (type IN ('Посібник', 'Книга', 'Періодичне видання')),
        copies INT,
        max_loan_period INT
    )
""")


cur.execute("""
    CREATE TABLE IF NOT EXISTS Readers (
        ticket_number INT PRIMARY KEY,
        last_name VARCHAR(255),
        first_name VARCHAR(255),
        phone_number VARCHAR(13),
        address VARCHAR(255),
        course INT CHECK (course >= 1 AND course <= 4),
        group_name VARCHAR(255)
    )
""")


cur.execute("""
    CREATE TABLE IF NOT EXISTS Book_Loans (
        loan_code SERIAL PRIMARY KEY,
        loan_date DATE,
        reader_ticket INT,
        book_inventory_number INT,
        FOREIGN KEY (reader_ticket) REFERENCES Readers(ticket_number),
        FOREIGN KEY (book_inventory_number) REFERENCES Books(inventory_number)
    )
""")

# Збереження змін у базі даних
conn.commit()

# Закриття підключення
cur.close()
conn.close()
