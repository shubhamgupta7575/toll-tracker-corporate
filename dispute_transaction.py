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
        rec_count = 0 ;
        # data rows of csv file
        qry = "SELECT trip_no, deduct_price from toll_diff WHERE status='Y'"
        cursor.execute(qry)
        result = cursor.fetchall()

        if(cursor.rowcount>0):
            for final_res in result:
               rows = []
               ded_price = final_res[1]
               act_price = final_res[2]
               if (float(ded_price)/float(act_price)==2.0):
                    sub_type = "DOUBLE DEBIT"
               else:
                    sub_type = dbInfo.subtype
               rows.append(dbInfo.type)
               rows.append(sub_type)
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
               f.flush()
               rec_count+=1
        f.close()
        print("No of Disputeed Transaction CSV Logged:.", rec_count)
        print("Program completed.")
        print("Dispute Transaction CSV File is Ready.")
if __name__  ==  "__main__":
    dispute_transaction()
