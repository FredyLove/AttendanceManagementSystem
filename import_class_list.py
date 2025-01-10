def import_class_list(file_path):
    try:
        if file_path.endswith(".txt"):
            with open(file_path, "r") as file:
                names = [line.strip() for line in file.readlines()]
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            names = df["Name"].tolist()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        for name in names:
            cursor.execute("INSERT OR IGNORE INTO students (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
