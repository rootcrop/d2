import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import pandas as pd
import requests


def get_stock_data(tickers, start_date, end_date):
    """
    Получаем данные о ценах акций для заданных тикеров.

    :param tickers:     Список тикеров акций
    :param start_date:  Дата начала (строка в формате 'YYYY-MM-DD')
    :param end_date:    Дата окончания (строка в формате 'YYYY-MM-DD')
    :return:            DataFrame с данными о ценах акций
    """
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Close']


def get_stock_volume(tickers, start_date, end_date):
    """
    Получаем данные о объемах продаж акций для заданных тикеров.

    :param tickers: Список тикеров акций
    :param start_date: Дата начала (строка в формате 'YYYY-MM-DD')
    :param end_date: Дата окончания (строка в формате 'YYYY-MM-DD')
    :return: DataFrame с данными об объемах акций
    """
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Volume']


def plot_line_stock(stock_data):
    """
    Seaborn:         линейный график (line plot)

    :param stock_data:  DataFrame с данными о ценах акций и их тикерами
    :return:            линейный график (line plot)
    """
    data = stock_data.reset_index()  # сбрасываем индекс, чтобы сделать "Дату" столбцом
    data = pd.melt(data, id_vars=['Date'], var_name='Stock', value_name='Price')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='Date', y='Price', hue='Stock')
    plt.title('Цены на акции')
    plt.xlabel('Дата')
    plt.ylabel('цена закрытия')
    plt.legend(title='Акции')
    plt.savefig('img/002seaborn1lineplot.png')
    plt.show()
    plt.close()


def distribution_of_stock(stock_data):
    """
    Seaborn:         распределение цен (ящик с усами)

    :param stock_data:  DataFrame с данными о ценах акций и их тикерами
    :return:            график распределение цен (boxplot)
    """
    data = stock_data
    data = data.reset_index()  # Reset index to make 'Date' a column
    data = pd.melt(data, id_vars=['Date'], var_name='Stock', value_name='Price')  # Reshape for Seaborn

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x='Stock', y='Price')
    plt.title('Распределение цен')
    plt.xlabel('Акция')
    plt.ylabel('Цена закрытия')
    plt.savefig('img/002seaborn2distribution.png')
    plt.show()
    plt.close()


def correlation_of_stock(stock_data):
    data = stock_data.reset_index()  # Reset index to make 'Date' a column
    data = pd.melt(data, id_vars=['Date'], var_name='Stock', value_name='Price')  # Reshape for Seaborn
    correlation_matrix = data.pivot(index='Date', columns='Stock', values='Price').corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Корреляция между акциями')
    plt.savefig('img/002seaborn3correlation.png')
    plt.show()
    plt.close()


def fetch_coin_price_data(coin_name, days=30):
    """
    функция извлекает исторические данные о цене монеты (coin_name) из API CoinGecko.
    за указанное количество дней (days)

    :param coin_name    название монеты
    :param days:        за сколько дней загружать цену
    :return:            данные возвращаются в виде фрейма данных pandas,
                        содержащего два столбца: "Временная метка" и "цена"
    """

    url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:  # try extract prices
        prices = data['prices']
    except Exception:
        print('error on get price of coin name: ' + coin_name)
        exit()

    df = pd.DataFrame(prices, columns=['timestamp', 'price'])  # конвертируем в дата_фрэйм
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


def lineplot_bitcoin(coin_df, coin, days):
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=coin_df, x='timestamp', y='price', marker='o')
    plt.title('цена ' + coin + ' за последние ( ' + str(days) + ' дней)')
    plt.xlabel('Дата')
    plt.ylabel('Цена (USD)')
    plt.grid(True)
    plt.savefig('img/002seaborn4linePlotCoin.png')
    plt.show()


# Задаем тикеры и даты
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'BLK']
start_date = '2024-09-01'
end_date = '2024-12-01'

# Получаем данные по цене и объему
get_stock_prices = get_stock_data(tickers, start_date, end_date)
volume_data = get_stock_volume(tickers, start_date, end_date)
correlation_of_stock(get_stock_prices)
plot_line_stock(get_stock_prices)
distribution_of_stock(get_stock_prices)

coin = 'bitcoin'
days = 40
coin_df = fetch_coin_price_data(coin, days)  # Fetch bitcoin data
lineplot_bitcoin(coin_df, coin, days)

'''
Seaborn     функции Seaborn "ориентированы на данные", т.е. они понимают структуру вашего набора данных 
            и могут автоматически извлекать метки осей, легенды и другие элементы графика. 
            В Matplotlib эти элементы необходимо явно определять.
            Встроенная поддержка доверительных интервалов автоматически рассчитывается и 
            отображаются доверительные интервалы для многих типов графиков,
            например, регрессионных линий, линейных графиков, столбчатых графиков, 
            что в Matplotlib потребовало бы ручного расчета и построения. 
            
Matplotlib  производительность обычно быстрее для простых графиков из-за своего низкоуровневого характера.
            Seaborn может быть медленнее для больших наборов данных из-за своих высокоуровневых 
            абстракций и дополнительных вычислений.
'''
