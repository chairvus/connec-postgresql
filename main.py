from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert


# create database engine
DATABASE_URL = "postgresql+psycopg2://developer:secretpassword@localhost:5432/companydb"
engine = create_engine(DATABASE_URL)

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String),
    Column("last_name", String),
)

metadata.create_all(engine)

data_user = [
    {"first_name": "Evans", "last_name": "Sudarsono"},
    {"first_name": "John", "last_name": "Sutiyoso"},
    {"first_name": "Indah", "last_name": "Cahya"},
]

# database connected
with engine.connect() as connection:
    try:
        print("Database connected")
        insert_statement = insert(user_table).values(data_user)
        connection.execute(insert_statement)

        connection.commit()
        print("Successful add data")
    except Exception as e:
        print(f"Noob: {e}")
