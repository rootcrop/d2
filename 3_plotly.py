import plotly.express as px
import seaborn as sns
import numpy as np
import pandas as pd

# загружаем датасет чаевых (tips dataset)
# этот набор имеет данные : total_bill, tip, sex, smoker, day, time, size
df = tips = px.data.tips()


def plotly_histogram():
    """
    plotly:             круговая диаграмма (pie chart)
                        Общее распределение счетов по дням.

    :param
    :return:            запускает plotly график
    """
    fig = px.histogram(df, x="total_bill", facet_row="day", facet_col="time",
                       nbins=30, title="Общее распределение счетов по дням")
    fig = px.pie(df, names='day', values='total_bill', title="Plotly. Общее распределение счетов по дням")
    fig.show()


def plotly_box():
    """
    Plotly              коробчатый график (box plot)
                        общего счета в разбивке по дням и полу.
    :param
    :return:            запускает plotly график
    """
    fig = px.box(df, x="day", y="total_bill", color="sex",
                 title="Plotly. Коробчатый график общего счета в разбивке по дням и полу")
    fig.show()


def plotly_scatter():
    """
    Plotly          диаграмма рассеяния (scatter plot) показывающая соотношение
                    чаевых и общего счета в зависимости от статуса (не)курильщика.

    :param
    :return:        запускает plotly график
    """

    fig = px.scatter(df, x="total_bill", y="tip", color="smoker", size='size', opacity=0.3,
                     title="Plotly. Соотношение чаевых и общего счета в зависимости от статуса (не)курильщика")
    fig.show()


def plotly_sunburst():
    """
    Plotly          диаграмма общего счета (sunburst chart) в разбивке по дням, полу и времени

    :param
    :return:        запускает plotly график
    """

    fig = px.sunburst(df,
                      path=['day', 'sex', 'time'],  # фильтры по выводу диаграмм
                      values='total_bill',
                      title="Plotly. Подробная круговая диаграмма общего счета в разбивке по дням, полу и времени")
    fig.show()


'''

'''


def plotly_scatter3d():
    """
    Plotly      трехмерная диаграмма рассеяния (3D scatter plot)
                эффектный 3D график, показывающий зависимость чаевых (tip) от
                общей суммы счета(total bill), разбитый по
                времени (выделено разной формой и цветом) и размеру компании

    :return:    запускает plotly график
    """
    fig = px.scatter_3d(df, x='total_bill', y='tip', z='size',
                        color='day', symbol='time', size='size', opacity=0.5,
                        title="Plotly. 3D график зависимости чаевых(tip) от общей суммы счета(total bill): "
                              "по дням, времени и размеру компании(party size)")

    fig.update_layout(scene=dict(  # обновленный макет осей X,Y,Z для сцены
        xaxis_title='Всего заказ',
        yaxis_title='Чаевые',
        zaxis_title='Человек в группе'
    ))
    fig.show()


def plotly_choropleth():
    """
    Plotly      пример использования карты хороплет (choropleth map),
                натягиваем датасет с чаевыми на глобус (на фоновую картограму)

    :return:
    """
    df = px.data.tips()

    # симулируем данные
    location_map = {'Thur': 'RUS', 'Fri': 'DEU', 'Sat': 'CHN', 'Sun': 'USA'}
    df['location'] = df['day'].map(location_map)

    # подсчитываем сумму чека в зависимости от местоположения
    location_data = df.groupby('location')['total_bill'].sum().reset_index()

    # Создаем  карту хороплета (choropleth map)
    fig = px.choropleth(location_data, locations='location', color='total_bill',
                        hover_name='total_bill', projection='natural earth',
                        title='Plotly. Общий счет по местоположению', color_continuous_scale='Sunsetdark')
    fig.show()


plotly_choropleth()
plotly_scatter3d()
plotly_histogram()
plotly_box()
plotly_scatter()
plotly_sunburst()
