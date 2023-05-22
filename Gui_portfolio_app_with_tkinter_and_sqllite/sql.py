from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap("folder.ico")

con = sqlite3.connect("coin.db")
cursorObj = con.cursor()
# cursorObj.execute("create table if not exists coin(id integer primary key, symbol text, amount integer, price real)")
# con.commit()

# cursorObj.execute("insert into coin values(2, 'ETH', 3, 3503.76)")
# con.commit()

# cursorObj.execute("insert into coin values(3, 'USDC', 100, 1.00)")
# con.commit()

# cursorObj.execute("insert into coin values(4, 'USDT', 30, 1.00)")
# con.commit()

# cursorObj.execute("insert into coin values(5, 'BNB', 5, 452.18)")
# con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
    app_nav()    
    my_portfolio()
    app_header()
    
def app_nav():
    def clear_all():
        cursorObj.execute("Delete From Coin")
        con.commit()
        
        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Add New Coins")
        reset()
        
    def close_app():
        pycrypto.destroy()
            
    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label = "Clear Portfolio", command = clear_all)
    file_item.add_command(label = "Close App", command = close_app)
    menu.add_cascade(label = "File", menu = file_item)
    pycrypto.config(menu = menu)
    
def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5&convert=USD&CMC_PRO_API_KEY=af3fc09d-5fac-4b5b-9250-4f12a414e0f4")
    api = json.loads(api_request.content)

    cursorObj.execute("select * from coin")
    coins = cursorObj.fetchall()
    
    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"
    
    def insert_coin():
        cursorObj.execute("insert into coin(symbol, price, amount) values(?, ?, ?)", (symbol_txt.get(), price_txt.get(), amount_txt.get()))
        con.commit()   
       
        reset()
        messagebox.showinfo("Portfolio Notification", "Coin Added to Portfolio Successfully!")
        
    def update_coin():
        cursorObj.execute("update coin set symbol=?, price=?, amount=? where id=?", (symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get()))
        con.commit()  
        
        messagebox.showinfo("Portfolio Notification", "Coin Updated Successfully!")
        reset()
        
    def delete_coin():
        cursorObj.execute("delete from coin where id=?", (portid_delete.get(),))
        con.commit() 
        
        messagebox.showinfo("Portfolio Notification", "Coin Deleted From Portfolio Successfully!")
        reset()
        
    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0
    
    for i in range(0, 5):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]: 
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]
                
                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid
                
                # print(api["data"][i]["name"] + " - " + api["data"][i]["symbol"]) 
                # print("Price - ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Number of Coin:", coin[2])
                # print("Total Amount Paid:", "${0:.2f}".format(total_paid))
                # print("Current Value:", "${0:.2f}".format(current_value))
                # print("P/L Per Coin:", "${0:.2f}".format(pl_percoin))
                # print("Total P/L With Coin:", "${0:.2f}".format(total_pl_coin))
                # print("------------")

                portfolio_id = Label(pycrypto, text = coin[0], bg = "white", fg = "black", font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
                portfolio_id.grid(row = coin_row , column = 0, sticky = N+S+E+W)

                name = Label(pycrypto, text = api["data"][i]["symbol"], bg = "white", fg = "black", font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
                name.grid(row = coin_row , column = 1, sticky = N+S+E+W)

                price = Label(pycrypto, text = "${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg = "white", fg = "black", font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
                price.grid(row = coin_row , column = 2, sticky = N+S+E+W)

                no_coins = Label(pycrypto, text = coin[2], bg = "white", fg = "black", font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
                no_coins.grid(row = coin_row , column = 3, sticky = N+S+E+W)

                amount_paid = Label(pycrypto, text = "${0:.2f}".format(total_paid), bg = "white", fg = "black", font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
                amount_paid.grid(row = coin_row , column = 4, sticky = N+S+E+W)

                current_val = Label(pycrypto, text = "${0:.2f}".format(current_value), bg = "white", fg = "black", font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
                current_val.grid(row = coin_row , column = 5, sticky = N+S+E+W)

                pl_coin = Label(pycrypto, text = "${0:.2f}".format(pl_percoin), bg = "white", fg = font_color(float("{0:.2f}".format(pl_percoin))), font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
                pl_coin.grid(row = coin_row , column = 6, sticky = N+S+E+W)

                totalpl = Label(pycrypto, text = "${0:.2f}".format(total_pl_coin), bg = "white", fg = font_color(float("{0:.2f}".format(total_pl_coin))), font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
                totalpl.grid(row = coin_row , column = 7, sticky = N+S+E+W)
                
                coin_row += 1
    
    #insert data
    symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_txt.grid(row = coin_row + 1, column = 1)
    
    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row = coin_row + 1, column = 2)
    
    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row = coin_row + 1, column = 3)
    
    add_coin = Button(pycrypto, text = "ADD COIN", bg = "purple", fg = "white", command = insert_coin, font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
    add_coin.grid(row = coin_row + 1 , column = 4, sticky = N+S+E+W)
    
    #update data
    portid_update = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_update.grid(row = coin_row + 2, column = 0)
    
    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row = coin_row + 2, column = 1)
    
    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row = coin_row + 2, column = 2)
    
    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row = coin_row + 2, column = 3)
    
    update_coin_txt = Button(pycrypto, text = "UPDATE COIN", bg = "sky blue", fg = "white", command = update_coin, font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
    update_coin_txt.grid(row = coin_row + 2 , column = 4, sticky = N+S+E+W)
    
    #delete coin
    portid_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_delete.grid(row = coin_row + 3, column = 0)
    
    delete_coin_txt = Button(pycrypto, text = "DELETE COIN", bg = "dark green", fg = "white", command = delete_coin, font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
    delete_coin_txt.grid(row = coin_row + 3 , column = 4, sticky = N+S+E+W)
    
    totalap = Label(pycrypto, text = "${0:.2f}".format(total_amount_paid), bg = "yellow", fg = "white", font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
    totalap.grid(row = coin_row , column = 4, sticky = N+S+E+W)
                
    totalcv = Label(pycrypto, text = "${0:.2f}".format(total_current_value), bg = "blue", fg = "white", font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
    totalcv.grid(row = coin_row , column = 5, sticky = N+S+E+W)
    
    totalpl = Label(pycrypto, text = "${0:.2f}".format(total_pl), bg = "blue", fg = font_color(float("{0:.2f}".format(total_pl))), font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
    totalpl.grid(row = coin_row , column = 7, sticky = N+S+E+W)
    
    api = ""
    
    refresh = Button(pycrypto, text = "REFRESH", bg = "black", fg = "white", command=reset, font="Calibri 12 bold", padx="2", pady="2", borderwidth=2, relief="groove")
    refresh.grid(row = coin_row + 1 , column = 7, sticky = N+S+E+W)

    print("Total P/L For Portfolio:", "${0:.2f}".format(total_pl))

def app_header():
    portfolio_id = Label(pycrypto, text = "Portfolio ID", bg = "red", fg = "white", font="Calibri 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    portfolio_id.grid(row = 0, column = 0, sticky = N+S+E+W)
    
    name = Label(pycrypto, text = "Coin Name", bg = "red", fg = "white", font="Calibri 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row = 0, column = 1, sticky = N+S+E+W)

    price = Label(pycrypto, text = "Price", bg = "red", fg = "white", font="Calibri 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    price.grid(row = 0, column = 2, sticky = N+S+E+W)

    no_coins = Label(pycrypto, text = "Coin Owned", bg = "red", fg = "white", font="Calibri 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    no_coins.grid(row = 0, column = 3, sticky = N+S+E+W)

    amount_paid = Label(pycrypto, text = "Total Amount Paid", bg = "red", fg = "white", font="Calibri 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    amount_paid.grid(row = 0, column = 4, sticky = N+S+E+W)

    current_val = Label(pycrypto, text = "Current Value", bg = "red", fg = "white", font="Calibri 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    current_val.grid(row = 0, column = 5, sticky = N+S+E+W)

    pl_coin = Label(pycrypto, text = "P/L Per Coin", bg = "red", fg = "white", font="Calibri 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    pl_coin.grid(row = 0, column = 6, sticky = N+S+E+W)

    totalpl = Label(pycrypto, text = "Total P/L With Coin", bg = "red", fg = "white", font="Calibri 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    totalpl.grid(row = 0, column = 7, sticky = N+S+E+W)

app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()

cursorObj.close()
con.close()
