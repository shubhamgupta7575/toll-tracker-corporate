import mysql.connector
import csv
from datetime import datetime
import dbInfo
import pandas as pd
from pathlib import Path

def fastagStatementDB():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )
    count = 0
    process_count = 0
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor = db.cursor()
    my_file = Path("OnlineStatement.csv")
    if not(my_file.is_file()):
        # file not exists
        data = pd.read_html('../../Downloads/OnlineStatement.xls')
        df  = pd.DataFrame(data=data[0])
        df.to_csv("OnlineStatement.csv",index=False, header=None)
    csv_data = csv.reader(open('OnlineStatement.csv', newline=''))
    next(csv_data)
    print("Processing... Please wait")
    for row in csv_data:
        plazacode = row[6].lstrip('ÿ')
        s = row[10].replace(',', '')
        price = float(s)
        if(row[5]!="ADJUSTMENT" and row[0]!='' and price!=0.0):
            plazaname = row[7].split("Plaza Name:")[1].split()[0].strip('-')
            unique_id1 = row[8].lstrip('ÿ')
            unique_id2 = unique_id1.split("/")
            unique_id = unique_id1.split("/")[0].strip()
            trip_id = unique_id2[1].strip()
            sql = "INSERT INTO fastag_statement (txn_dtm, lic_no, tag_no, plaza_code, plaza_name, rrn, trip_no, deduct_price, created_at) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s', '%s');" % (row[0], row[2], row[3], plazacode, plazaname, unique_id, trip_id, row[10], dt_string)
            try:
               # Execute the SQL command
               process_count += 1
               # print(sql)
               cursor.execute(sql)
               count += cursor.rowcount

               # Commit your changes in the database
               db.commit()
            except:
               # print("Error :",process_count, sys.exc_info()[0])
               # Rollback in case there is any error
               db.rollback()
    f = open("output.txt", "a")
    f.write(dt_string+"- Total Processed Data "+format(process_count)+" and Total "+format(count)+" data inserted successfully!"+"\n")
    f.close()
    print("Total Processed Data {} and Total {} data inserted successfully! ".format(process_count,count))

if __name__ == "__main__":
    fastagStatementDB()
