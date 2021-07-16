import mysql.connector
import dbInfo
import csv
from pathlib import Path

def dispute_transaction():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )
    cursor = db.cursor(buffered=True)
    # field names
    fields = ['Type', 'Subtype', 'Priority', 'Severity', 'Trip Number', 'Dispute Amount', 'Title', 'Description']
    # name of csv file
    csv_file_path = Path("dispute_transaction_temp.csv")
    csv_file = "dispute_transaction_temp.csv"
    if not(csv_file_path.is_file()):
    # open the file in the write mode
        f = open(csv_file, 'w', encoding='UTF8', newline='')

        # create the csv writer
        csvwriter = csv.writer(f)

        # writing the fields
        csvwriter.writerow(fields)

        # data rows of csv file
        qry = "SELECT trip_no, deduct_price from toll_diff WHERE status='Y'"
        cursor.execute(qry)
        result = cursor.fetchall()

        if(cursor.rowcount>0):
            for final_res in result:
               rows = []
               rows.append(dbInfo.type)
               rows.append(dbInfo.subtype)
               rows.append(dbInfo.priority)
               rows.append(dbInfo.severity)
               rows.append(final_res[0])
               rows.append(final_res[1])
               rows.append(dbInfo.title)
               rows.append(dbInfo.description)
               # writing the data rows
               csvwriter.writerow(rows)
               update_qry = "UPDATE `toll_diff` SET `status` = 'L' WHERE trip_no='{}';".format(final_res[0])
               cursor.execute(update_qry)
               db.commit()
        print("Dispute Transaction CSV File is Ready.")
if __name__  ==  "__main__":
    dispute_transaction()
