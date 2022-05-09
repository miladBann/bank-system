from ast import Mod
import json
from datetime import datetime, date
import datetime
from tkinter import *
import tkinter
import time
from tkinter import messagebox
from turtle import width


WHITE_BLUE = "#caf0f8"
LIGHT_BLUE = "#90e0ef"
BLUE = "#00b4d8"
DARKER_BLUE = "#0077b6"
DARKEST_BLUE = "#03045e"

BALANCE = 0
USER_NAME = None
ACCOUNT_NUM = None

account_exists = False
crr_account = None

all_accounts = []

with open("accounts_data.json", mode="r") as datafile:
    data = json.load(datafile)

acc_list = []
for acc in data:
    acc_list.append(acc)

# calculates how many account already exist in the json file
# so when we create a new acc it adds one to whatever the current number is
with open("accounts_data.json", mode="r") as datafile:
    data = json.load(datafile)

count = 0
for acc in data:
    count += 1
accounts_count = count


class Account:
    def __init__(self, full_name, id_num, account_num, pin_code, birth_year):
        self.name = full_name
        self.id = id_num
        self.account_num = account_num
        self.pin = pin_code
        self.birth_year = birth_year
        self.old_enough = False
        self.pin_is_ok = False
        self.movements = []
        self.balance = 0


def display(balance, admin_name, acc_number):
    global crr_account

    id_num_lbl.destroy()
    id_entry.destroy()
    pin_lbl.destroy()
    pin_entry.destroy()

    window.attributes('-fullscreen', True)
    window.config(bg=WHITE_BLUE)

    ############################  Functions   ###################################

    def close():
        window.destroy()

    close_btn = Button(text="❌", font=("Arial", 18, "bold"),
                       command=close, bg=WHITE_BLUE)
    close_btn.place(x=1480, y=0)

    ############################  check an acc already exists   #################

    def check_if_acc_exists(crr_acc):
        global account_exists

        with open("accounts_data.json", mode="r") as datafile:
            data2 = json.load(datafile)

            for acc in data2:
                if acc == crr_acc:
                    account_exists = True
                    break

    ############################## display movemnets ############################

    def display_movements():

        with open("accounts_data.json", mode="r") as datafile:
            data = json.load(datafile)

        lista.delete(0, END)

        for acc in data:
            if acc == crr_account:
                movements = data[acc]["movs"]
                for mov in movements:
                    if mov > 0:
                        my_str = f"        Deposit     of     {mov} shekels"
                        lista.insert(0, my_str)
                        spacer = "___________________________________"
                        lista.insert(0, spacer)
                    elif mov < 0:
                        # the new_mov is just the same number but without the negative sign
                        new_mov = abs(mov)
                        my_str = f"        Withdraw of     {new_mov} shekels"
                        lista.insert(0, my_str)
                        spacer = "___________________________________"
                        lista.insert(0, spacer)

    ############################## calculate balance ############################

    def calc_balance():
        global BALANCE, crr_account

        with open("accounts_data.json", mode="r") as datafile:
            data = json.load(datafile)

        for acc in data:
            if acc == crr_account:
                balance = sum(data[acc]["movs"])

                BALANCE = balance
                current_balance.config(text=f"{BALANCE}₪")

                data[acc]["balance"] = BALANCE

                # updating the database with the current balance
                with open("accounts_data.json", mode="w") as datafile:
                    data = json.dump(data, datafile, indent=4)

    ############################## create account ####################

    def create_account():
        global accounts_count, account_exists

        window2 = tkinter.Toplevel(window)
        window2.title("Create an account")
        window2.minsize(height=350, width=550)
        window2.config(bg=WHITE_BLUE)

        name_lbl = Label(window2, text="Full name:", font=(
            "Arial", 20, "bold"), bg=WHITE_BLUE)
        name_lbl.place(x=30, y=20)

        name_entry = Entry(window2, font=("Arial", 20, "bold"))
        name_entry.place(x=200, y=20)

        id_num_lbl = Label(window2, text="ID number:", font=(
            "Arial", 20, "bold"), bg=WHITE_BLUE)
        id_num_lbl.place(x=30, y=80)

        id_num_entry = Entry(window2, font=("Arial", 20, "bold"))
        id_num_entry.place(x=200, y=80)

        pin_lbl = Label(window2, text="Type a Pin:", font=(
            "Arial", 20, "bold"), bg=WHITE_BLUE)
        pin_lbl.place(x=30, y=140)

        pin_entry = Entry(window2, font=("Arial", 20, "bold"))
        pin_entry.place(x=200, y=140)

        birth_year_lbl = Label(window2, text="birth year:",
                               font=("Arial", 20, "bold"), bg=WHITE_BLUE)
        birth_year_lbl.place(x=30, y=200)

        birth_year_entry = Entry(window2, font=("Arial", 20, "bold"))
        birth_year_entry.place(x=200, y=200)

        def submit():
            global accounts_count

            name = name_entry.get()
            id_number = id_num_entry.get()
            birthyear = int(birth_year_entry.get())
            pin = pin_entry.get()
            old_enough = False
            pin_is_ok = False

            check_if_acc_exists(id_number)

            if account_exists == True:
                messagebox.showerror(title="Account already exists",
                                     message=f"An account with the id of {id_number} already exists in the data base.")
            else:
                acc_list.append(id_number)

                age = datetime.datetime.now().year - birthyear
                if age >= 18:
                    old_enough = True
                else:
                    messagebox.showerror(title="Can't create account",
                                         message="You are not old enough!")

                if len(pin) == 4:
                    pin_is_ok = True
                else:
                    messagebox.showerror(title="Can't create account",
                                         message="Pin should only be 4 digits!")

                if old_enough == True and pin_is_ok == True:
                    accounts_count += 1
                    acc_number = accounts_count
                    acc = Account(name, id_number, acc_number, pin, birthyear)
                    all_accounts.append(acc)

                    messagebox.showinfo(title="Account Created Sucessfully!",
                                        message=f"\n\nHere is the new account details:\n\nName: {name},\n\nID number: {id_number},\n\nAge: {age} years old,\n\nPin: {pin}")

                    new_data = {
                        id_number: {
                            "id": id_number,
                            "name": name,
                            "pin": pin,
                            "birth_year": birthyear,
                            "acc_num": acc_number,
                            "balance": 0,
                            "movs": []
                        }
                    }

                    try:
                        with open("accounts_data.json", mode="r") as datafile:
                            data = json.load(datafile)

                    except FileNotFoundError:
                        with open("accounts_data.json", mode="w") as datafile:
                            json.dump(new_data, datafile, indent=4)

                    else:
                        data.update(new_data)
                        with open("accounts_data.json", mode="w") as datafile:
                            json.dump(data, datafile, indent=4)

                    finally:
                        window2.destroy()

        submit_btn = Button(window2, text="Submit", font=(
            "Arial", 20, "bold"), bg=DARKER_BLUE, width=15, command=submit)
        submit_btn.place(x=150, y=260)

        window2.mainloop()

    ############################## delete account ####################

    def delete_account():
        global acc_list, crr_account

        window2 = tkinter.Toplevel(window)
        window2.title("Delete Account")
        window2.minsize(height=350, width=605)
        window2.config(bg=WHITE_BLUE, padx=20, pady=20)

        title_lbl1 = Label(window2, text="*if you want to proceed with deleting the account", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        title_lbl1.place(x=0, y=0)

        title_lbl2 = Label(window2, text=" enter your ID and Pin",
                           font=("Arial", 18, "bold"), bg=WHITE_BLUE)
        title_lbl2.place(x=0, y=30)

        id_lbl = Label(window2, text="ID num:", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        id_lbl.place(x=100, y=100)

        id_entry_1 = Entry(window2, font=("Arial", 18, "bold"))
        id_entry_1.place(x=210, y=100)

        pin_lbl_2 = Label(window2, text="Pin num:", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        pin_lbl_2.place(x=100, y=150)

        pin_entry_1 = Entry(window2, font=("Arial", 18, "bold"))
        pin_entry_1.place(x=210, y=150)

        def submit2():

            id_num = id_entry_1.get()
            pin_num = pin_entry_1.get()

            if id_num == crr_account:
                if id_num not in acc_list:
                    messagebox.showerror(
                        title="Account doesn't exist", message="the entered ID doesn't match any account")
                    id_entry_1.delete(0, END)
                    pin_entry_1.delete(0, END)

                with open("accounts_data.json", mode="r") as datafile:
                    data2 = json.load(datafile)

                for acc in data2:

                    if acc == id_num:
                        if data2[acc]["pin"] == pin_num:

                            # removing the logged in account
                            # and updating the cuurrent database
                            data2.pop(crr_account)
                            messagebox.showinfo(title="Account deleted sucessfuly",
                                                message=f"\n\nthe account with the:\nID number of {id_num}\n\nPin number of {pin_num}\n\nwas deleted sucessfuly")

                            with open("accounts_data.json", mode="w") as datafile:
                                data2 = json.dump(data2, datafile, indent=4)

                            window.destroy()

                            break
            else:
                messagebox.showerror(
                    title="Can't delete account", message="You need to br signed in to the account you want to delete.\n\nthe entered ID doesn't match the logged in account.")

        proceed_btn = Button(window2, text="Proceed", font=(
            "Arial", 18, "bold"), bg=DARKER_BLUE, command=submit2)
        proceed_btn.place(x=240, y=200)

        window2.mainloop()

    ############################## withdraw money ####################

    def withdraw_money():
        global crr_account

        window2 = tkinter.Toplevel(window)
        window2.title("Withdraw money 💸")
        window2.minsize(height=280, width=605)
        window2.config(bg=WHITE_BLUE, padx=20, pady=20)

        msg1 = Label(window2, text="how much would you like to withdraw", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        msg1.place(x=60, y=20)

        amount_lbl = Label(window2, text="amount:                              ₪", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        amount_lbl.place(x=120, y=80)

        amount_entry = Entry(window2, width=15, font=(
            "Arial", 18, "bold"))
        amount_entry.place(x=220, y=80)

        def withdraw():

            amount = int(f"-{amount_entry.get()}")

            if amount < -2500:
                messagebox.showerror(
                    title="Can't Withdraw", message="you can't withdraw more than 2500₪ in a day.")
            else:
                with open("accounts_data.json", mode="r") as datafile:
                    data2 = json.load(datafile)

                    for acc in data2:
                        if acc == crr_account:
                            data2[acc]["movs"].append(amount)

                            with open("accounts_data.json", mode="w") as datafile:
                                data2 = json.dump(data2, datafile, indent=4)

                            lista.delete(0, END)

                            display_movements()
                            calc_balance()

                            window2.destroy()

        withdraw_btn = Button(window2, text="Withdraw", bg=DARKER_BLUE,
                              command=withdraw, font=("Arial", 18, "bold"))
        withdraw_btn.place(x=220, y=140)

        window2.mainloop()

    ############################## deposit money ####################

    def deposit_money():
        global crr_account

        window2 = tkinter.Toplevel(window)
        window2.title("Deposit money 💸")
        window2.minsize(height=280, width=605)
        window2.config(bg=WHITE_BLUE, padx=20, pady=20)

        msg1 = Label(window2, text="how much would you like to Deposit", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        msg1.place(x=60, y=20)

        amount_lbl = Label(window2, text="amount:                              ₪", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        amount_lbl.place(x=120, y=80)

        amount_entry = Entry(window2, width=15, font=(
            "Arial", 18, "bold"))
        amount_entry.place(x=220, y=80)

        def deposit():

            amount = int(amount_entry.get())

            if amount > 10000:
                messagebox.showerror(
                    title="Can't Deposit", message="you can't Deposit more than 10,000₪ in a day.")
            else:
                with open("accounts_data.json", mode="r") as datafile:
                    data2 = json.load(datafile)

                    for acc in data2:
                        if acc == crr_account:
                            data2[acc]["movs"].append(amount)

                            with open("accounts_data.json", mode="w") as datafile:
                                data2 = json.dump(data2, datafile, indent=4)

                            lista.delete(0, END)

                            display_movements()
                            calc_balance()

                            window2.destroy()

        deposit_btn = Button(window2, text="Deposit", bg=DARKER_BLUE,
                             command=deposit, font=("Arial", 18, "bold"))
        deposit_btn.place(x=220, y=140)

        window2.mainloop()

    ############################## transfer money ####################

    def transfer_money():

        window2 = tkinter.Toplevel(window)
        window2.title("Transfer money 📩")
        window2.minsize(height=280, width=605)
        window2.config(bg=WHITE_BLUE, padx=20, pady=20)

        msg1_lbl = Label(window2, text="Enter the ID number and account number",
                         bg=WHITE_BLUE, font=("Arial", 18, "bold"))
        msg2_lbl = Label(window2, text="of the account you want to transfer to",
                         bg=WHITE_BLUE, font=("Arial", 18, "bold"))

        msg1_lbl.place(x=80, y=0)
        msg2_lbl.place(x=60, y=30)

        id_lbl = Label(window2, text="ID num:", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        id_lbl.place(x=120, y=80)

        id_entry = Entry(window2, width=16, font=(
            "Arial", 18, "bold"),)
        id_entry.place(x=240, y=80)

        account_num_lbl = Label(window2, text="Acc num:", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        account_num_lbl.place(x=120, y=120)

        account_num_entey = Entry(window2, width=16, font=(
            "Arial", 18, "bold"))
        account_num_entey.place(x=240, y=120)

        def transfer():
            global crr_account, acc_list

            id_num = id_entry.get()
            account_number = int(account_num_entey.get())

            if id_num not in acc_list:
                messagebox.showerror(
                    title="Can't transfer.", message="the entered ID number doesn't match any account.")
            else:
                with open("accounts_data.json", mode="r") as datafile:
                    data2 = json.load(datafile)

                    for acc in data2:
                        if data2[acc]["acc_num"] == account_number and data2[acc]["id"] == id_num:

                            print("target found")

                            window2.destroy()

                            window3 = tkinter.Toplevel(window)
                            window3.title("Deposit money 💸")
                            window3.minsize(height=280, width=605)
                            window3.config(bg=WHITE_BLUE, padx=20, pady=20)

                            msg1 = Label(window3, text="how much would you like to Transfer", font=(
                                "Arial", 18, "bold"), bg=WHITE_BLUE)
                            msg1.place(x=60, y=20)

                            amount_lbl = Label(window3, text="amount:                              ₪", font=(
                                "Arial", 18, "bold"), bg=WHITE_BLUE)
                            amount_lbl.place(x=120, y=80)

                            amount_entry = Entry(window3, width=15, font=(
                                "Arial", 18, "bold"))
                            amount_entry.place(x=220, y=80)

                            def transfer_accepted():
                                global crr_account

                                # the amount to withdraw from the sender
                                amount = int(f"-{amount_entry.get()}")

                                # the amount to give for the reciever
                                real_amount = int(amount_entry.get())

                                if amount < -6500:
                                    messagebox.showerror(
                                        title="Can't Withdraw", message="you can't Transfer more than 6500₪ in a day.")
                                else:
                                    with open("accounts_data.json", mode="r") as datafile:
                                        data2 = json.load(datafile)

                                        # sending the money to the reciever
                                        data2[id_num]["movs"].append(
                                            real_amount)
                                        with open("accounts_data.json", mode="w") as datafile:
                                            data2 = json.dump(
                                                data2, datafile, indent=4)

                                        # update the sender account info
                                        with open("accounts_data.json", mode="r") as datafile:
                                            data3 = json.load(datafile)

                                        for acc in data3:

                                            if acc == crr_account:
                                                data3[acc]["movs"].append(
                                                    amount)

                                                with open("accounts_data.json", mode="w") as datafile:
                                                    data3 = json.dump(
                                                        data3, datafile, indent=4)

                                                lista.delete(0, END)

                                                display_movements()
                                                calc_balance()

                                                window3.destroy()
                                                break

                            transfer_money_button = Button(window3, text="Transfer", bg=DARKER_BLUE,
                                                           command=transfer_accepted, font=("Arial", 18, "bold"))
                            transfer_money_button.place(x=220, y=140)

                            window3.mainloop()

                        else:
                            print("still searching for traget account....")

        transfer_money_btn = Button(window2, text="Transfer", width=15, font=(
            "Arial", 18, "bold"), bg=DARKER_BLUE, command=transfer)
        transfer_money_btn.place(x=170, y=170)

        window2.mainloop()

    ############################## Request loan ####################

    def request_loan():
        global crr_account

        messagebox.showinfo(title="Before requesting a loan",
                            message="we need to know how many years you worked and how much is your monthly salary so we can check if you are viable to get a loan.")

        window2 = tkinter.Toplevel(window)
        window2.title("Request a loan")
        window2.minsize(height=310, width=605)
        window2.config(bg=WHITE_BLUE, padx=20, pady=20)

        work_years_lbl = Label(window2, text="years working:", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        work_years_lbl.place(x=80, y=20)

        work_entry = Entry(window2, width=16, font=(
            "Arial", 18, "bold"),)
        work_entry.place(x=270, y=20)

        salary_lbl = Label(window2, text="monthly salary:", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        salary_lbl.place(x=80, y=80)

        salary_entey = Entry(window2, width=16, font=(
            "Arial", 18, "bold"))
        salary_entey.place(x=270, y=80)

        amount_lbl = Label(window2, text="loan amount:", font=(
            "Arial", 18, "bold"), bg=WHITE_BLUE)
        amount_lbl.place(x=80, y=140)

        amount_entry = Entry(window2, width=16, font=(
            "Arial", 18, "bold"))
        amount_entry.place(x=270, y=140)

        def check():
            work_years = int(work_entry.get())
            monthly_salary = int(salary_entey.get())
            loan_amount = int(amount_entry.get())

            compensation = work_years * monthly_salary

            repeat = ((loan_amount * 10) / 100)

            final_loan = loan_amount - repeat

            if compensation > loan_amount:
                messagebox.showinfo(
                    title="Request Accepted", message=f"your request for a loan was accepted\n\nyour compesation is: {compensation}\n\nyour loan amount is: {loan_amount}\n\nyour repeat is 10% of the loan amount: {repeat}\n\nyou final loan value is: {final_loan}")

                new_data = {
                    crr_account: {
                        "id": crr_account,
                        "work_years": work_years,
                        "monthly_salary": monthly_salary,
                        "loan_amount": loan_amount,
                        "repeat_value": repeat,
                        "final_loan_value": final_loan
                    }
                }

                try:
                    with open("loan_data.json", mode="r") as datafile:
                        data = json.load(datafile)

                except FileNotFoundError:
                    with open("loan_data.json", mode="w") as datafile:
                        json.dump(new_data, datafile, indent=4)

                else:
                    data.update(new_data)
                    with open("loan_data.json", mode="w") as datafile:
                        json.dump(data, datafile, indent=4)

                # updating the accounts database
                with open("accounts_data.json", mode="r") as datafile2:
                    data2 = json.load(datafile2)

                    data2[crr_account]["movs"].append(final_loan)

                    with open("accounts_data.json", mode="w") as datafile2:
                        data2 = json.dump(data2, datafile2, indent=4)

                    display_movements()
                    calc_balance()

                    window2.destroy()

            else:
                messagebox.showerror(
                    title="Request Denied", message=f"your compensation of {compensation} isn't enough to cover a loan of {loan_amount}")

        check_btn = Button(window2, text="Check", width=15, font=(
            "Arial", 18, "bold"), bg=DARKER_BLUE, command=check)
        check_btn.place(x=170, y=200)

        window2.mainloop()

    ############################  Functions   ###################################

    ######## the list ##################
    my_frame = Frame(window)
    my_frame.place(x=20, y=60)

    lista = Listbox(my_frame, font=("times new roman", 27, "bold"), width=35, height=18, highlightthickness=0,
                    selectbackground="#a6a6a6", activestyle=None, bg=BLUE, fg="black")
    lista.pack(side="left", fill="both")

    my_scrollbar = Scrollbar(my_frame)
    my_scrollbar.pack(side="right", fill="both")

    lista.config(yscrollcommand=my_scrollbar.set)
    my_scrollbar.config(command=lista.yview)

    # this spacer is only for looks and not function
    spacer = "___________________________________"
    lista.insert(0, spacer)

    lista.delete(0, END)
    display_movements()

    ####################################

    ########## user info ################

    spacer1 = Label(text="_____________________________________________________",
                    font=("Arial", 20, "bold"), bg=WHITE_BLUE)
    spacer1.place(x=680, y=30)

    admin_name_lbl = Label(text="User name: ", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    admin_name_lbl.place(x=680, y=80)

    user_name = Label(text=admin_name, font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    user_name.place(x=860, y=80)

    account_number_lbl = Label(text="Acc num: ", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    account_number_lbl.place(x=680, y=150)

    acc_num = Label(text=acc_number, font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    acc_num.place(x=860, y=150)

    crr_date_lbl = Label(text="Date: ", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    crr_date_lbl.place(x=1200, y=80)

    current_date = date.today()
    date_lbl = Label(text=current_date, font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    date_lbl.place(x=1300, y=80)

    crr_time_lbl = Label(text="Time: ", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    crr_time_lbl.place(x=1200, y=150)

    def getTime():
        string = time.strftime('%H:%M:%S %p')
        real_time.config(text=string)
        real_time.after(1000, getTime)

    real_time = Label(text="time", font=("Arial", 22, "bold"), bg=WHITE_BLUE)
    real_time.place(x=1300, y=150)

    getTime()

    spacer2 = Label(text="_____________________________________________________",
                    font=("Arial", 20, "bold"), bg=WHITE_BLUE)
    spacer2.place(x=680, y=180)
    ###########################################

    ####### account info ######################

    account_balance_lbl = Label(text="Account Ballance: ", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    account_balance_lbl.place(x=900, y=225)

    current_balance = Label(text=f"{balance}₪", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    current_balance.place(x=1150, y=225)
    calc_balance()

    spacer3 = Label(text="_____________________________________________________",
                    font=("Arial", 20, "bold"), bg=WHITE_BLUE)
    spacer3.place(x=680, y=253)

    ###########################################

    ######### function buttons ####################

    create_Acc_btn = Button(text="Create Account", font=(
        "Arial", 20, "bold"), bg=DARKER_BLUE, padx=80, pady=40, command=create_account)
    create_Acc_btn.place(x=680, y=320)

    delete_Acc_btn = Button(text="Delete Account", font=(
        "Arial", 20, "bold"), bg=DARKER_BLUE, padx=80, pady=40, command=delete_account)
    delete_Acc_btn.place(x=1100, y=320)

    withdraw_btn = Button(text="Withdraw Money", font=(
        "Arial", 20, "bold"), bg=DARKER_BLUE, padx=75, pady=40, command=withdraw_money)
    withdraw_btn.place(x=680, y=500)

    deposit_btn = Button(text="Deposit Money", font=(
        "Arial", 20, "bold"), bg=DARKER_BLUE, padx=80, pady=40, command=deposit_money)
    deposit_btn.place(x=1100, y=500)

    transfer_btn = Button(text="Transfer Money", font=(
        "Arial", 20, "bold"), bg=DARKER_BLUE, padx=80, pady=40, command=transfer_money)
    transfer_btn.place(x=680, y=680)

    loan_btn = Button(text="Request Loan", font=(
        "Arial", 20, "bold"), bg=DARKER_BLUE, padx=85, pady=40, command=request_loan)
    loan_btn.place(x=1100, y=680)

    ################ switch accounts btn #########################
    def switch():

        window2 = tkinter.Toplevel(window)
        window2.title("Switch between accounts")
        window2.minsize(width=700, height=400)
        window2.config(bg=WHITE_BLUE)

        id_num_lbl = Label(window2, text="ID num:", font=(
            "Arial", 20, "bold"), bg=WHITE_BLUE)
        id_num_lbl.place(x=180, y=100)

        id_entry = Entry(window2, font=("Arial", 20, "bold"), width=15)
        id_entry.place(x=310, y=100)

        pin_lbl = Label(window2, text="Pin num:", font=(
            "Arial", 20, "bold"), bg=WHITE_BLUE)
        pin_lbl.place(x=180, y=160)

        pin_entry = Entry(window2, font=("Arial", 20, "bold"), width=15)
        pin_entry.place(x=310, y=160)

        def submit():
            global crr_account, BALANCE, USER_NAME, ACCOUNT_NUM

            id_num = id_entry.get()
            pin_num = pin_entry.get()

            with open("accounts_data.json", mode="r") as datafile:
                data = json.load(datafile)

            if id_num not in acc_list:
                messagebox.showerror(
                    title="Account doesn't exist", message="the entered ID doesn't match any account")
                id_entry.delete(0, END)
                pin_entry.delete(0, END)

            for acc in data:
                if acc == id_num:

                    if data[acc]["pin"] == pin_num:

                        BALANCE = data[acc]["balance"]
                        USER_NAME = data[acc]["name"]
                        ACCOUNT_NUM = data[acc]["acc_num"]

                        crr_account = data[acc]["id"]

                        user_name.config(text=USER_NAME)
                        acc_num.config(text=ACCOUNT_NUM)
                        current_balance.config(text=BALANCE)

                        # clear everything in the list
                        lista.delete(0, END)
                        # display the movements of the user
                        display_movements()
                        # display the new balance
                        calc_balance()

                        window2.destroy()
                    else:
                        messagebox.showerror(
                            title="Wrong Pin", message="the entered Pin doesn't match the ID number of the account")
                        id_entry.delete(0, END)
                        pin_entry.delete(0, END)

        log_in_btn = Button(window2, text="Log In", font=(
            "Arial", 18, "bold"), width=12, bg=DARKER_BLUE, command=submit)
        log_in_btn.place(x=270, y=230)

    switch_btn = Button(text="🔁", font=("Arial", 19, "bold"),
                        bg=WHITE_BLUE, command=switch)
    switch_btn.place(x=1425, y=0)

    ###########################################
    window.mainloop()


window = Tk()
window.title("Log in ➡")
window.minsize(width=700, height=400)
window.config(bg=WHITE_BLUE)

id_num_lbl = Label(text="ID num:", font=(
    "Arial", 20, "bold"), bg=WHITE_BLUE)
id_num_lbl.place(x=180, y=100)

id_entry = Entry(font=("Arial", 20, "bold"), width=15)
id_entry.place(x=310, y=100)

pin_lbl = Label(text="Pin num:", font=("Arial", 20, "bold"), bg=WHITE_BLUE)
pin_lbl.place(x=180, y=160)

pin_entry = Entry(font=("Arial", 20, "bold"), width=15)
pin_entry.place(x=310, y=160)


def submit():
    global crr_account, BALANCE, USER_NAME, ACCOUNT_NUM

    id_num = id_entry.get()
    pin_num = pin_entry.get()

    with open("accounts_data.json", mode="r") as datafile:
        data = json.load(datafile)

    if id_num not in acc_list:
        messagebox.showerror(title="Account doesn't exist",
                             message="the entered ID doesn't match any account")
        id_entry.delete(0, END)
        pin_entry.delete(0, END)

    for acc in data:
        if acc == id_num:

            if data[acc]["pin"] == pin_num:

                BALANCE = data[acc]["balance"]
                USER_NAME = data[acc]["name"]
                ACCOUNT_NUM = data[acc]["acc_num"]

                crr_account = data[acc]["id"]

                display(BALANCE, USER_NAME, ACCOUNT_NUM)
            else:
                messagebox.showerror(
                    title="Wrong Pin", message="the entered Pin doesn't match the ID number of the account")
                id_entry.delete(0, END)
                pin_entry.delete(0, END)


log_in_btn = Button(text="Log In", font=(
    "Arial", 18, "bold"), width=12, bg=DARKER_BLUE, command=submit)
log_in_btn.place(x=270, y=230)


def register_Acc():
    global accounts_count, account_exists

    window2 = tkinter.Toplevel(window)
    window2.title("Create an account")
    window2.minsize(height=350, width=550)
    window2.config(bg=WHITE_BLUE)

    name_lbl = Label(window2, text="Full name:", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    name_lbl.place(x=30, y=20)

    name_entry = Entry(window2, font=("Arial", 20, "bold"))
    name_entry.place(x=200, y=20)

    id_num_lbl = Label(window2, text="ID number:", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    id_num_lbl.place(x=30, y=80)

    id_num_entry = Entry(window2, font=("Arial", 20, "bold"))
    id_num_entry.place(x=200, y=80)

    pin_lbl = Label(window2, text="Type a Pin:", font=(
        "Arial", 20, "bold"), bg=WHITE_BLUE)
    pin_lbl.place(x=30, y=140)

    pin_entry = Entry(window2, font=("Arial", 20, "bold"))
    pin_entry.place(x=200, y=140)

    birth_year_lbl = Label(window2, text="birth year:",
                           font=("Arial", 20, "bold"), bg=WHITE_BLUE)
    birth_year_lbl.place(x=30, y=200)

    birth_year_entry = Entry(window2, font=("Arial", 20, "bold"))
    birth_year_entry.place(x=200, y=200)

    def check_if_acc_exists(crr_acc):
        global account_exists

        with open("accounts_data.json", mode="r") as datafile:
            data2 = json.load(datafile)

            for acc in data2:
                if acc == crr_acc:
                    account_exists = True
                    break

    def submit():
        global accounts_count

        name = name_entry.get()
        id_number = id_num_entry.get()
        birthyear = int(birth_year_entry.get())
        pin = pin_entry.get()
        old_enough = False
        pin_is_ok = False

        check_if_acc_exists(id_number)

        if account_exists == True:
            messagebox.showerror(title="Account already exists",
                                 message=f"An account with the id of {id_number} already exists in the data base.")
        else:
            acc_list.append(id_number)

            age = datetime.datetime.now().year - birthyear
            if age >= 18:
                old_enough = True
            else:
                messagebox.showerror(title="Can't create account",
                                     message="You are not old enough!")

            if len(pin) == 4:
                pin_is_ok = True
            else:
                messagebox.showerror(title="Can't create account",
                                     message="Pin should only be 4 digits!")

            if old_enough == True and pin_is_ok == True:
                accounts_count += 1
                acc_number = accounts_count
                acc = Account(name, id_number, acc_number, pin, birthyear)
                all_accounts.append(acc)

                messagebox.showinfo(title="Account Created Sucessfully!",
                                    message=f"\n\nHere is the new account details:\n\nName: {name},\n\nID number: {id_number},\n\nAge: {age} years old,\n\nPin: {pin}")

                new_data = {
                    id_number: {
                        "id": id_number,
                        "name": name,
                        "pin": pin,
                        "birth_year": birthyear,
                        "acc_num": acc_number,
                        "balance": 0,
                        "movs": []
                    }
                }

                try:
                    with open("accounts_data.json", mode="r") as datafile:
                        data = json.load(datafile)

                except FileNotFoundError:
                    with open("accounts_data.json", mode="w") as datafile:
                        json.dump(new_data, datafile, indent=4)

                else:
                    data.update(new_data)
                    with open("accounts_data.json", mode="w") as datafile:
                        json.dump(data, datafile, indent=4)

                finally:
                    window2.destroy()

    submit_btn = Button(window2, text="Submit", font=(
        "Arial", 20, "bold"), bg=DARKER_BLUE, width=15, command=submit)
    submit_btn.place(x=150, y=260)

    window2.mainloop()


auto_fill_btn = Button(text="Register", font=(
    "Arial", 18, "bold"), width=12, bg=DARKER_BLUE, command=register_Acc)
auto_fill_btn.place(x=270, y=280)

window.mainloop()
