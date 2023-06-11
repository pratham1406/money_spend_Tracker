from tkinter import *
from tkinter import ttk
import sqlite3 as db
import matplotlib.pyplot as plt

from tkcalendar import DateEntry


def init():
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    create table if not exists expenses (
        date string,
        name string,
        title string,
        expense number
        )
    '''
    curr.execute(query)
    connectionObjn.commit()


def submitexpense():
    values = [dateEntry.get(), Name.get(), Title.get(), Expense.get()]
    print(values)
    Etable.insert('', 'end', values=values)

    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    INSERT INTO expenses VALUES 
    (?, ?, ?, ?)
    '''
    curr.execute(query, (dateEntry.get(), Name.get(), Title.get(), Expense.get()))
    connectionObjn.commit()


def viewexpense():
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
     select * from expenses
    '''
    total = '''
    select sum(expense) from expenses
    '''
    curr.execute(query)
    rows = curr.fetchall()
    curr.execute(total)
    amount = curr.fetchall()[0][0]  # Get the first element of the first row (total expense)
    print(rows)
    print(amount)

    l = Label(root, text="Date\t  Name\t  Title\t  Expense", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white")
    l.grid(row=6, column=0, padx=7, pady=7)

    st = ""
    for i in rows:
        for j in i:
            st += str(j) + '\t'
        st += '\n'
    print(st)
    l = Label(root, text=st, font=('arial', 12))
    l.grid(row=7, column=0, padx=7, pady=7)

    # Plotting graph
    categories = []
    expenses = []
    for row in rows:
        categories.append(row[2])  # Assuming the title is stored in the third column (index 2)
        expenses.append(row[3])  # Assuming the expense is stored in the fourth column (index 3)

    plt.bar(categories, expenses)
    plt.xlabel('Categories')
    plt.ylabel('Expense')
    plt.title('Expense Summary')
    plt.xticks(rotation=45)
    plt.show()


def deleteexpense():
    selected_item = Etable.selection()
    if not selected_item:
        return

    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()

    for item in selected_item:
        values = Etable.item(item, 'values')
        curr.execute("DELETE FROM expenses WHERE date=? AND name=? AND title=? AND expense=?",
                     (values[0], values[1], values[2], values[3]))
        Etable.delete(item)

    connectionObjn.commit()


def clearall():
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    curr.execute("DELETE FROM expenses")
    connectionObjn.commit()
    Etable.delete(*Etable.get_children())


init()
root = Tk()
root.title("Money Manager")
root.geometry('800x600')

# Set background color
root.configure(bg="yellow")

dateLabel = Label(root, text="Date", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
dateLabel.grid(row=0, column=0, padx=7, pady=7)

dateEntry = DateEntry(root, width=12, font=('arial', 15, 'bold'))
dateEntry.grid(row=0, column=1, padx=7, pady=7)

Name = StringVar()
nameLabel = Label(root, text="Name", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
nameLabel.grid(row=1, column=0, padx=7, pady=7)

NameEntry = Entry(root, textvariable=Name, font=('arial', 15, 'bold'))
NameEntry.grid(row=1, column=1, padx=7, pady=7)

Title = StringVar()
titleLabel = Label(root, text="Title", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
titleLabel.grid(row=2, column=0, padx=7, pady=7)

titleEntry = Entry(root, textvariable=Title, font=('arial', 15, 'bold'))
titleEntry.grid(row=2, column=1, padx=7, pady=7)

Expense = IntVar()
expenseLabel = Label(root, text="Expense", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
expenseLabel.grid(row=3, column=0, padx=7, pady=7)

expenseEntry = Entry(root, textvariable=Expense, font=('arial', 15, 'bold'))
expenseEntry.grid(row=3, column=1, padx=7, pady=7)

submitbtn = Button(root, command=submitexpense, text="Submit", font=('arial', 15, 'bold'), bg="DodgerBlue2",
                   fg="white", width=12)
submitbtn.grid(row=4, column=0, padx=13, pady=13)

viewtn = Button(root, command=viewexpense, text="View expenses", font=('arial', 15, 'bold'), bg="DodgerBlue2",
                fg="white", width=12)
viewtn.grid(row=4, column=1, padx=13, pady=13)

deletebtn = Button(root, command=deleteexpense, text="Delete", font=('arial', 15, 'bold'), bg="DodgerBlue2",
                   fg="white", width=12)
deletebtn.grid(row=4, column=2, padx=13, pady=13)

clearallbtn = Button(root, command=clearall, text="Clear All", font=('arial', 15, 'bold'), bg="DodgerBlue2",
                     fg="white", width=12)
clearallbtn.grid(row=4, column=3, padx=13, pady=13)

# Set background color for buttons
submitbtn.configure(bg="deep sky blue")
viewtn.configure(bg="deep sky blue")
deletebtn.configure(bg="deep sky blue")
clearallbtn.configure(bg="deep sky blue")

# Set colors for treeview
style = ttk.Style()
style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
style.theme_use("default")

# all saved expenses--------------
Elist = ['Date', 'Name', 'Title', 'Expense']
Etable = ttk.Treeview(root, column=Elist, show='headings', height=7)
for c in Elist:
    Etable.heading(c, text=c.title())
Etable.grid(row=5, column=0, padx=7, pady=7, columnspan=4)

mainloop()
