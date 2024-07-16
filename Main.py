import os
import tkinter as tk
from tkinter import *
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# get API key from env variable
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

# get top gainers and losers API
def get_gainers_losers():
    url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    return data

# get specific stock data API
def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    print(data)
    return data


# blank chart in start up window
def blank_chart(window):
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.set_title("Blank Chart")
    ax.plot([], [], linestyle='-', color='b', label="Closing Price")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# take data and plot closing points
def plot_data(window,symbol):
    data = get_stock_data(symbol)
    week_data = data['Weekly Adjusted Time Series']
    dates = list(week_data.keys())
    closing_prices = [float (week_data[date]['4. close'])for date in dates]

    recent_dates = dates[:7]
    recent_prices = closing_prices[:7]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(recent_dates,recent_prices,marker='o',linestyle='-',color='b',label='closing price')
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.set_title(f"{symbol} stock chart")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# use API to display top losers and gainers
def show_gain_loss(frame):
    data = get_gainers_losers()
    top_gainers = data.get('top_gainers', [])

    row = 0
    for gainer in top_gainers:
        ticker = gainer.get('ticker')
        price = gainer.get('price')
        change_amount = gainer.get('change_amount')
        change_percentage = gainer.get('change_percentage')

        gainer_info = f"{ticker}: {price} ({change_amount}, {change_percentage})"

        label = Label(frame, text=gainer_info, bg='lightblue', anchor='e',font=('Arial', 12, 'bold'))
        label.grid(row=row, column=0, padx=20, pady=2, sticky='nsew')
        row += 2

    top_losers = data.get('top_losers', [])

    rowLoser = 0
    for loser in top_losers:
        tickerL = loser.get('ticker')
        priceL = loser.get('price')
        change_amountL = loser.get('change_amount')
        change_percentageL = loser.get('change_percentage')

        loser_info = f"{tickerL}: {priceL} ({change_amountL}, {change_percentageL})"

        labelL = Label(frame, text=loser_info, bg='lightblue',anchor='w',font=('Arial',12,'bold'))
        labelL.grid(row=rowLoser, column=1, padx=150, pady=3, sticky='nsew')
        rowLoser += 2

# Show most traded  using API
def show_most_traded(bottom_frame):
    data = get_gainers_losers()
    row_active = 100
    most_active_traded = data.get('most_actively_traded', [])[:8]
    for info in most_active_traded:
        ticker_active = info.get('ticker')
        price_active = info.get('price')
        change_amount_active = info.get('change_amount')
        change_percentage_active = info.get('change_percentage')

        active_info = f"{ticker_active}: {price_active} ({change_amount_active}, {change_percentage_active})"
        label_active = Label(bottom_frame, text=active_info, bg='lightblue', anchor='e', font=('Arial', 14, 'bold'))
        label_active.grid(row=row_active, column=1, padx=150, pady=3, sticky='e')
        row_active += 1

#getting data from chart into words
def show_chart_data(frame, symbol):
    data = get_stock_data(symbol)
    chart_data = data.get('Weekly Adjusted Time Series',{})

    for widget in frame.winfo_children():
        widget.destroy()

    row = 0
    for date, info in chart_data.items():
            open_price = info.get('1. open')
            high = info.get('2. high')
            low = info.get('3. low')
            close = info.get('4. close')
            volume = info.get('6. volume')
            div = info.get('7. dividend amount')

            info_format = f"Most Recent Data: {symbol}: Open: {open_price}, High: {high}, Low: {low}, Close: {close}, Volume: {volume}, Dividend: {div}"

            label = Label(frame, text=info_format, bg='lightblue', anchor='e', font=('Arial', 12, 'bold'))
            label.grid(row=row, column=0, padx=10, pady=5, sticky='nsew')
            row+=1
            if row == 0:
                break


#display info
def interface():
    global searchBox, plot_frame, window, volume_frame
    window = Tk()
    window.geometry("800x800")
    window.title("Stock Market Tracker")
    window.config(background="gray")

    window.grid_rowconfigure(0, weight=0)
    window.grid_rowconfigure(1,weight=0)
    window.grid_columnconfigure(0, weight=0)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_rowconfigure(4, weight=1)
    window.grid_columnconfigure(3, weight=1)
    window.grid_columnconfigure(2, weight=1)


    searchBox = tk.Entry(window, font=('Bold', 20), width=25)
    searchBox.grid(row=0, column=0, pady=5, padx=244, sticky="nw")
    searchButton = tk.Button(window,text="Search for stock symbol", command=on_search, font=("Bold", 15), fg="black")
    searchButton.grid(row=0, column=0, pady=5, padx=4, sticky="nw")

    plot_frame = Frame(window,bg='white')
    plot_frame.grid(row=1, column=0, columnspan=1, padx=4, pady=4, sticky="nsew")
    blank_chart(plot_frame)

    side_frame = Frame(window, bg='lightblue', width=500)
    side_frame.grid(row=1, column=1, rowspan=3, columnspan=3, padx=5, pady=70, sticky="nsew")
    side_frame.grid_columnconfigure(0, weight=1)
    side_frame.grid_columnconfigure(1, weight=1)
    side_frame.grid_columnconfigure(2, weight=1)
    side_frame.grid_rowconfigure(1, weight=1)
    get_gainers_losers()

    top_gainers_label = Label(window, text="Top Gainers        &         Top Losers", bg='lightblue', font=('Arial', 14, 'bold'))
    top_gainers_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    format_label = Label(window, text='Format: Symbol: price (change amount, percent change)',bg='lightblue', font=('Arial',14,'bold'),width=60)
    format_label.grid(row=1, column=1, padx=150, pady=10, sticky='n')
    show_gain_loss(side_frame)


    bottom_frame = Frame(window, bg='lightblue', width=500)
    bottom_frame.grid(row=4, column=1, columnspan=4, padx=20, pady=10, sticky="nsew")
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)
    most_traded = Label(bottom_frame, text='This weeks most traded: ', bg='lightblue',font=('Arial', 14, 'bold'))
    most_traded.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    show_most_traded(bottom_frame)


    volume_frame = Frame(window, bg='lightblue', width=200)
    volume_frame.grid(row=4, column=0, columnspan=1, padx=5, pady=10,sticky='nsew')
    chart_info = Label(volume_frame, text='Chart Information:', bg='lightblue',font=('Arial', 14, 'bold'))
    chart_info.grid(row=0, column=0, padx=5, pady=5, sticky='w')


    window.mainloop()

# plot data with search box data
def on_search():
    if searchBox.get() != " ":
        get_stock_data(searchBox.get())
        for widget in plot_frame.winfo_children():
            widget.destroy()
        plot_data(plot_frame, searchBox.get())
        show_chart_data(volume_frame, searchBox.get())




if __name__ == "__main__":
    interface()

