# test_logic.py

import os
import sys
import pandas as pd
import pytest

# Добавляем корень проекта в путь (на случай запуска извне)
sys.path.insert(0, os.path.dirname(__file__))

from logic import filter_and_sort_places

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "moscow_places.csv")


def test_csv_exists():
    """Проверяем, что CSV-файл существует"""
    assert os.path.exists(CSV_PATH), f"Файл не найден: {CSV_PATH}"


def test_filter_by_category():
    """Фильтрация по типу заведения: 'кофейня'"""
    df = pd.read_csv(CSV_PATH)
    df['seats'] = pd.to_numeric(df['seats'], errors='coerce').fillna(0).astype(int)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    result = filter_and_sort_places(df, categories_list=["кофейня"], districts_list=[])

    assert len(result) > 0, "Должны быть найдены кофейни"
    assert all(cat == "кофейня" for cat in result["category"].unique())


def test_filter_by_district():
    """Фильтрация по округу: 'Центральный административный округ'"""
    df = pd.read_csv(CSV_PATH)
    df['seats'] = pd.to_numeric(df['seats'], errors='coerce').fillna(0).astype(int)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    result = filter_and_sort_places(df, categories_list=[], districts_list=["Центральный административный округ"])

    assert len(result) > 0, "Должны быть заведения в ЦАО"
    assert all(dist == "Центральный административный округ" for dist in result["district"].unique())


def test_min_seats_filter():
    """Фильтр: минимум 100 мест"""
    df = pd.read_csv(CSV_PATH)
    df['seats'] = pd.to_numeric(df['seats'], errors='coerce').fillna(0).astype(int)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    result = filter_and_sort_places(df, categories_list=[], districts_list=[], seats_min=100)

    assert all(row["seats"] >= 100 for _, row in result.iterrows())


def test_rating_filter():
    """Фильтр: рейтинг ≥ 4.5"""
    df = pd.read_csv(CSV_PATH)
    df['seats'] = pd.to_numeric(df['seats'], errors='coerce').fillna(0).astype(int)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    result = filter_and_sort_places(df, categories_list=[], districts_list=[], rating_min=4.5)

    for _, row in result.iterrows():
        if pd.notna(row["rating"]):
            assert row["rating"] >= 4.5


def test_empty_filters_return_data():
    """Если фильтры пустые — возвращаются все строки"""
    df = pd.read_csv(CSV_PATH)
    df['seats'] = pd.to_numeric(df['seats'], errors='coerce').fillna(0).astype(int)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    result = filter_and_sort_places(df, categories_list=[], districts_list=[], seats_min=None, rating_min=0.0)

    assert len(result) > 0
    assert len(result) <= len(df)