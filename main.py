import requests
import itertools
import smtplib

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
email = "edernonato47teste@hotmail.com"
password = "Eder@teste321"
SMTP = "smtp-mail.outlook.com"
PORT = 587

to_email = input("Insert the email that will receive the message:")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key_stock = "DWO3A8YGD0HR1AUE"
OWM_endpoint_stock = "https://www.alphavantage.co/query"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key_stock
}

api_key_news = "7a2ba9c920384241a85ada5238b0e973"
OWM_endpoint_news = "https://newsapi.org/v2/everything"
news_parameters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": api_key_news
}


response = requests.get(OWM_endpoint_stock, stock_parameters)
data = response.json()
daily = data["Time Series (Daily)"]
daily_2_days = dict(itertools.islice(daily.items(), 2))
# Another way to do that using list comprehention to get transform the dict in a list with every value without key:
# yesterday_value = [value for (key, value) in daily.items()]
# print(yesterday_value)
two_last_close_values = []

for item in daily_2_days:
    two_last_close_values.append(float(daily_2_days[item]["4. close"]))


five_percent = two_last_close_values[0] * 0.05
difference_between_values = two_last_close_values[0] - two_last_close_values[1]
difference_in_percent = (difference_between_values * 100) / two_last_close_values[0]

if abs(difference_in_percent) > 1:
    up_down = None
    if difference_in_percent > 0:
        up_down = "⬆"

    else:
        up_down = "⬇"

    news_response = requests.get(OWM_endpoint_news, news_parameters)
    data_news = news_response.json()
    data_news_slicing = data_news["articles"][:3]
    connection = smtplib.SMTP(SMTP, PORT)
    connection.starttls()
    connection.login(user=email, password=password)
    for article in range(len(data_news_slicing)):
        connection.sendmail(from_addr=email, to_addrs=to_email, msg=f"Subject:{COMPANY_NAME}: {up_down}️"
                                                                                  f"{round(difference_in_percent, 2)}%\n\nHeadline: {data_news_slicing[article]['title']}\n\n"
                                                                                  f"{data_news_slicing[article]['description']}".encode('utf-8'))


# Optional: Format the SMS message like this:
"""TSLA: 🔺2% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey have 
gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings 
show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash. 
or "TSLA: 🔻5% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey 
have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F 
filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus 
market crash. """
