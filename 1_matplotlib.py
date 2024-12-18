import yfinance as yf
import matplotlib.pyplot as plt


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


def line_plot_stocks(stock_data, *args):
    """
    MatPlotLib:     линейный график (line plot)

    :param stock_data:  yf DataFrame с данными о ценах акций
    :param args:        тикеры акций
    :return:            линейный график (line plot)
    """
    plt.figure(figsize=(14, 7))
    for ticker in args:
        plt.plot(stock_data[ticker], label=ticker)

    plt.title('Цены акций')
    plt.xlabel('Дата')
    plt.ylabel('Цена ($)')
    plt.legend()
    plt.grid()
    plt.savefig('img/001matplotlib_1plot.png')
    plt.show()
    plt.close()


def plot_volume_chart(volume_data, *args):
    """
    MatPlotLib:     столбчатая диаграмма объемов продаж

    :param volume_data  yf DataFrame с данными об объемах продаж акций
    :param args:        тикеры акций
    :return:            график объема
    """
    plt.figure(figsize=(12, 6))
    for ticker in args:
        plt.bar(volume_data.index, volume_data[ticker], label=ticker, alpha=0.3)
    plt.title('График объема торговли')
    plt.xlabel('Дата')
    plt.ylabel('Объем торговли')
    plt.legend()
    plt.grid(True)
    plt.savefig('img/001matplotlib_2volume_plot.png')
    plt.show()
    plt.close()


def scatter_plot(stock_data, stock1, stock2):
    """
    Строим диаграмму рассеяния для двух акций.

    :param stock_data:  DataFrame с данными о ценах акций
    :param stock1:      Тикер первой акции
    :param stock2:      Тикер второй акции
    :return:            диаграмму рассеяния
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(stock_data[stock1], stock_data[stock2], alpha=0.3)
    plt.title(f'Диаграмма рассеяния: {stock1} vs {stock2}')
    plt.xlabel(stock1)
    plt.ylabel(stock2)
    plt.grid()
    plt.savefig('img/001matplotlib_3scatter_plot.png')
    plt.show()
    plt.close()


def plot_correlation_stock(stock_data, *args):  # +1 indicates a perfect positive linear relationship
    """
    Строим диаграмму корреляций акций

    :param stock_data:  DataFrame с данными о ценах акций
    :param *args:       список тикеров акции
    :return:            диаграмму корреляций
    """
    correlation = stock_data.corr();
    plt.figure(figsize=(8, 6))
    plt.imshow(correlation, cmap='coolwarm', interpolation='none');
    plt.colorbar()
    plt.xticks(range(len(tickers)), tickers);
    plt.yticks(range(len(tickers)), tickers)
    plt.title('Корреляция между акциями');
    plt.savefig('img/001matplotlib_4correlation.png')
    plt.show();
    plt.close()


# Задаем тикеры и даты
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'BLK']
start_date = '2024-09-01'
end_date = '2024-12-01'

# Получаем данные по цене и объему
stock_data = get_stock_data(tickers, start_date, end_date)
volume_data = get_stock_volume(tickers, start_date, end_date)

line_plot_stocks(stock_data, 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'BLK')
plot_volume_chart(volume_data, 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'BLK')
scatter_plot(stock_data, 'AAPL', 'BLK')
plot_correlation_stock(stock_data, 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'BLK')
