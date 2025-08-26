######## Version 1

# import sqlite3
# from datetime import datetime

# def log_decision(product, week, forecast, actual, deviation, action, explanation):
#     conn = sqlite3.connect("memory/ems_log.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS ems_log (
#             product TEXT,
#             week INTEGER,
#             forecast INTEGER,
#             actual INTEGER,
#             deviation REAL,
#             action TEXT,
#             explanation TEXT
#         )
#     """)

#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     cursor.execute("INSERT INTO ems_log VALUES (?, ?, ?, ?, ?, ?, ?)", 
#                    (product, week, forecast, actual, deviation, action, explanation))
#     conn.commit()
#     conn.close()



###### Version2 : for sales, revenue.profit and inventory
import sqlite3
from datetime import datetime

def log_decision(product, week, forecast, actual, deviation, action, explanation,
                 revenue, profit, inventory):
    conn = sqlite3.connect("memory/ems_log.db")
    cursor = conn.cursor()

    # Create table with new fields if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ems_log (
            product TEXT,
            week INTEGER,
            forecast INTEGER,
            actual INTEGER,
            deviation REAL,
            action TEXT,
            explanation TEXT,
            revenue INTEGER,
            profit INTEGER,
            inventory INTEGER,
            timestamp TEXT
        )
    """)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO ems_log (
            product, week, forecast, actual, deviation,
            action, explanation, revenue, profit, inventory, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product, week, forecast, actual, deviation,
        action, explanation, revenue, profit, inventory, timestamp
    ))

    conn.commit()
    conn.close()


