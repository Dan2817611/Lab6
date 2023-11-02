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

# Внесення інформації до таблиці Books
cur.execute("""
    INSERT INTO Books (inventory_number, author, title, section, year, pages, price, type, copies, max_loan_period)
    VALUES 
    (1, 'Шарл Діккенс', 'Давид Копперфілд', 'Художня', 1850, 624, 400.00, 'Книга', 5, 30),
    (2, 'Дж. Р. Р. Толкін', 'Володар перснів', 'Технічна', 1954, 1216, 850.00, 'Посібник', 3, 30),
    (3, 'Дж. К. Роулінг', 'Гаррі Поттер і Дари сметрі', 'Художня', 1997, 309, 600.00, 'Книга', 7, 30),
    (4, 'Дж. Д. Селінджер', 'Над обрієм у житті', 'Художня', 1951, 214, 425.00, 'Книга', 10, 30),
    (5, 'Ернест Хемінгуей', 'Старий і море', 'Технічна', 1952, 127, 375.00, 'Посібник', 4, 30),
    (6, 'Джордж Оруелл', '1984', 'Економічна', 1949, 328, 520.00, 'Книга', 6, 30),
    (7, 'Ульяна Громова', 'Початок шляху', 'Художня', 2020, 287, 550.00, 'Книга', 8, 30),
    (8, 'Сергій Жадан', 'Ворошиловград', 'Технічна', 2010, 320, 480.00, 'Посібник', 5, 30),
    (9, 'Агата Крісті', 'Вбивство в Східному експресі', 'Художня', 1934, 315, 370.00, 'Книга', 9, 30),
    (10, 'Антуан де Сент', 'Малий принц', 'Художня', 1943, 96, 255.00, 'Книга', 12, 30),
    (11, 'Френсіс Скотт', 'Великий Гетсбі', 'Економічна', 1925, 180, 330.00, 'Книга', 5, 30),
    (12, 'Герберт Уеллс', 'Війна світів', 'Художня', 1898, 256, 420.00, 'Періодичне видання', 8, 30),
    (13, 'Скотт Орсон Кард', 'Гра Ендера', 'Художня', 1985, 352, 531.25, 'Періодичне видання', 6, 30),
    (14, 'Сьюзен Коллінз', 'Голодні ігри', 'Художня', 2008, 374, 468.75, 'Періодичне видання', 7, 30);
""")

# Внесення інформації до таблиці Readers
cur.execute("""
    INSERT INTO Readers (ticket_number, last_name, first_name, phone_number, address, course, group_name)
    VALUES 
    (101, 'Іванов', 'Іван', '+380951234567', 'вул. Головна, 1', 2, 'Група 101'),
    (102, 'Петров', 'Петро', '+380951234568', 'вул. Петрівська, 2', 1, 'Група 102'),
    (103, 'Сидоров', 'Сергій', '+380951234569', 'вул. Сидорова, 3', 3, 'Група 103'),
    (104, 'Жуков', 'Олег', '+380951234570', 'вул. Жукова, 4', 2, 'Група 101'),
    (105, 'Смирнова', 'Анна', '+380951234571', 'вул. Смирнова, 5', 3, 'Група 102'),
    (106, 'Васильєва', 'Марія', '+380951234572', 'вул. Васильєва, 6', 1, 'Група 103'),
    (107, 'Козлов', 'Андрій', '+380951234573', 'вул. Козлова, 7', 3, 'Група 101'),
    (108, 'Соколов', 'Максим', '+380951234574', 'вул. Соколова, 8', 2, 'Група 102'),
    (109, 'Новіков', 'Ігор', '+380951234575', 'вул. Новікова, 9', 1, 'Група 103');
""")

# Внесення інформації до таблиці Book_Loans
cur.execute("""
    INSERT INTO Book_Loans (loan_code, loan_date, reader_ticket, book_inventory_number)
    VALUES 
    (1, '2023-10-30', 101, 1),
    (2, '2023-10-31', 102, 2),
    (3, '2023-11-01', 103, 3),
    (4, '2023-11-02', 104, 4),
    (5, '2023-11-03', 105, 5),
    (6, '2023-11-04', 106, 6),
    (7, '2023-11-05', 107, 7),
    (8, '2023-11-06', 108, 8),
    (9, '2023-11-07', 109, 9),
    (10, '2023-11-08', 101, 10),
    (11, '2023-11-09', 102, 11);
""")
# Збереження змін у базі даних
conn.commit()

# Закриття підключення
cur.close()
conn.close()