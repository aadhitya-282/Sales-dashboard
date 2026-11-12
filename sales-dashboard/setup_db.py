from database import initialize_database, load_sales

initialize_database()

df = load_sales()

print("Database created successfully!")
print("Total sales records:", len(df))
print(df.head())