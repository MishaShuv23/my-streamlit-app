# logic.py

import pandas as pd

# Колонки (лучше дублировать, чем тянуть из app.py)
COL_NAME = 'name'
COL_CATEGORY = 'category'
COL_DISTRICT = 'district'
COL_SEATS = 'seats'
COL_RATING = 'rating'

def filter_and_sort_places(df, categories_list, districts_list, seats_min=None, rating_min=0.0):
    """
    Фильтрует и сортирует заведения по заданным критериям.
    
    :param df: исходный DataFrame
    :param categories_list: список категорий (например, ["кофейня"])
    :param districts_list: список округов (например, ["Центральный административный округ"])
    :param seats_min: минимальное число мест (int или None)
    :param rating_min: минимальный рейтинг (float, по умолчанию 0.0)
    :return: отфильтрованный и отсортированный DataFrame
    """
    filtered_df = df.copy()

    # Фильтр по категориям
    if categories_list:
        filtered_df = filtered_df[filtered_df[COL_CATEGORY].isin(categories_list)]

    # Фильтр по округам
    if districts_list:
        filtered_df = filtered_df[filtered_df[COL_DISTRICT].isin(districts_list)]

    # Фильтр по местам
    if seats_min is not None and seats_min > 0:
        filtered_df = filtered_df[filtered_df[COL_SEATS] >= seats_min]

    # Фильтр по рейтингу
    if rating_min > 0:
        filtered_df = filtered_df[filtered_df[COL_RATING] >= rating_min]

    # Сортировка: рейтинг (по убыванию) → название (по возрастанию)
    filtered_df = filtered_df.sort_values(
        by=[COL_RATING, COL_NAME],
        ascending=[False, True],
        na_position='last'
    )
    return filtered_df