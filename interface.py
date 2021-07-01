import tkinter as tk
from fastagStatementDB import fastagStatementDB
from tollPriceDB import tollPriceDB
from tollScrapperCorporate import tollScrapperCorporate
from tollDiff import tollDiff
from dispute_transaction import dispute_transaction

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

root.geometry('450x300')
root.title('Toll Scrapper Corporate')

# result = tk.Label(text='STEP-1 : ', bg="green", fg="white")
# result.place(x=10,y=10)

tollscapperbutton = tk.Button(text='Download Fastag Statement Data')
tollscapperbutton["command"] = tollScrapperCorporate
tollscapperbutton.place(x=10,y=10)

tollbutton = tk.Button(text='Insert Fastag Statement CSV Data')
tollbutton["command"] = fastagStatementDB
tollbutton.place(x=250, y=10)

tollPricebutton = tk.Button(text='Insert Manually Data(Toll Price)')
tollPricebutton["command"] = tollPriceDB
tollPricebutton.place(x=10, y=50)

tollDiff_Button = tk.Button(text='Find Differences')
tollDiff_Button["command"] = tollDiff
tollDiff_Button.place(x=250,y=50)

dispute_transaction_button = tk.Button(text='Create CSV of Dispute Transactions')
dispute_transaction_button["command"] = dispute_transaction
dispute_transaction_button.place(x=10, y=90)

quit = tk.Button(text="QUIT", fg="red",command=root.destroy)
quit.place(x=200, y=150)

# result = tk.Label(text='RESULT : ', bg="green", fg="white")
# result.place(x=10,y=180)
# result = tk.Label(text='xxxx')
# result.place(x=80,y=180)

root.mainloop()


