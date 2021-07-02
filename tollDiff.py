import mysql.connector
import dbInfo
from datetime import datetime
import sys
def tollDiff():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )
    cursor = db.cursor(buffered=True)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    process_count = 0
    total_diff = 0
    status = 'Y'
    qry = "SELECT txn_dtm, rrn, trip_no, plaza_name, deduct_price from fastag_statement"
    cursor.execute(qry)
    result = cursor.fetchall()

    for x in result:
       process_count += 1
       txn_dtm = x[0]
       rrn = x[1]
       trip_no = x[2]
       plaza_name = x[3]
       ded_price = x[4].replace(',', '')
       deduct_price = float(ded_price)
       query = 'SELECT toll_name, toll_price FROM toll_prices WHERE toll_name="{}";'.format(plaza_name)
       cursor.execute(query)
       result2 = cursor.fetchall()
       if(cursor.rowcount>0):
           for final_res in result2:
               lst = []
               lst.append(final_res)
               actual_price = float(lst[0][1])
               # print("Act Price- ", lst[0][1])
               toll_name = lst[0][0]
               difference = abs(actual_price-deduct_price)
               cursor1 = db.cursor(buffered=True)
               if(difference>0.0):
                   print("Difference Found- ", actual_price, deduct_price, difference, toll_name)
                   total_diff +=1
                   insert_qry = "INSERT INTO toll_diff (txn_dtm, plaza_name, rrn, trip_no, actual_price, deduct_price, difference, status, created_at) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (txn_dtm, plaza_name, rrn, trip_no, actual_price, deduct_price, difference, status, dt_string)
                   try:
                       cursor1.execute(insert_qry)
                       db.commit()
                   except:
                       print("Error : ",process_count,", Duplicate Entry")
                       # print("Error :",process_count, sys.exc_info()[0])
                       # Rollback in case there is any error
                       db.rollback()


    f = open("output.txt", "a")
    f.write(dt_string+"- Total Process: "+ format(process_count)+ ",Total Found Differences: "+ format(total_diff)+"\n")
    f.close()
    print("Total Process: ", process_count, ",Total Found Differences: ", total_diff)
if __name__  ==  "__main__":
    tollDiff()
