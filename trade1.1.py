import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period='365d'):
    stock = yf.Ticker(ticker) #gets ticker object for entered ticker from yahoo api
    hist = stock.history(period=period) #retrieves stock historical EOD prices for selected time period
    return hist.reset_index() # returns stock data and pushed datetime to a regular column

def predict_future_prices(data, days_ahead):
    data['Date_ordinal'] = data['Date'].map(datetime.toordinal) #converts dates to int for linear regression
    
    dates = [[d] for d in data['Date_ordinal']]  #converts [ , , ] array to [[],[],[]] 2d array of int dates (needed for scikit)
    prices = list(data['Close']) #puts close prices in a list for linear regression

    model = LinearRegression() #creates a linear regression model
    model.fit(dates, prices) #feeds dependant and independant variables to model (date/price)

    last_date = data['Date'].iloc[-1]  #gets most recent close price 
    future_dates = [last_date + timedelta(days=i) for i in range(0, days_ahead)] # creates list of n future dates
    future_ordinals = [[d.toordinal()] for d in future_dates] # converts future dates to int 
    future_preds = model.predict(future_ordinals) #uses model to predict future prices

    return future_dates, future_preds, model

def plot_data(data, future_dates, future_preds, model):
    #combines known and predicted dates
    all_ordinals = [ [d.toordinal()] for d in list(data['Date']) + future_dates ] 
    all_dates = list(data['Date']) + future_dates 
    predicted_prices = model.predict(all_ordinals)

    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Close'], 'bo-', label='Close Prices') #plots known prices in blue
    plt.plot(all_dates, predicted_prices, 'r--', label='Trendline') #plots trend line in red
    plt.plot(future_dates, future_preds, 'go', label='Projected Prices') #plots predicted prices in green
    plt.xlabel("Date")
    plt.ylabel("Price USD")
    plt.title("Trade1 Prediction")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    ticker = input("Enter stock ticker : ")
    try:
        days = int(input("How many future days to predict? : "))
    except ValueError:
        print("Invalid input, defaulted to 5 days.")
        days = 5

    data = fetch_stock_data(ticker) # gets all knwon data
    future_dates, future_preds, model = predict_future_prices(data, days) #creates prediction
    plot_data(data, future_dates, future_preds, model) #plots all data

if __name__ == "__main__":
    main()
