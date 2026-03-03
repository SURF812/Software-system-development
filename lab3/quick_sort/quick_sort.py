"""
Модуль быстрой сортировки (Quick Sort).
"""

from typing import List


def quick_sort(arr: List[int]) -> List[int]:
    """
    Выполняет быструю сортировку массива.
    
    Args:
        arr: Список целых чисел для сортировки
        
    Returns:
        Новый отсортированный список
    """
    if not arr:
        return []
    
    if len(arr) <= 1:
        return arr[:]
    
    return _quick_sort_recursive(arr[:])


def _quick_sort_recursive(arr: List[int]) -> List[int]:
    """
    Рекурсивная функция быстрой сортировки.
    
    Args:
        arr: Список целых чисел
        
    Returns:
        Отсортированный список
    """
    # Базовый случай: массив из 0 или 1 элементов уже отсортирован
    if len(arr) <= 1:
        return arr
    
    # Выбираем опорный элемент (median-of-three для оптимизации)
    pivot = _choose_pivot(arr)
    
    # Разделяем массив на три части
    less = []      # Элементы меньше pivot
    equal = []     # Элементы равны pivot
    greater = []   # Элементы больше pivot
    
    for num in arr:
        if num < pivot:
            less.append(num)
        elif num > pivot:
            greater.append(num)
        else:
            equal.append(num)
    
    # Рекурсивно сортируем и объединяем
    return _quick_sort_recursive(less) + equal + _quick_sort_recursive(greater)


def _choose_pivot(arr: List[int]) -> int:
    """
    Выбирает опорный элемент используя median-of-three.
    
    Args:
        arr: Список целых чисел
        
    Returns:
        Значение опорного элемента
    """
    first = arr[0]
    last = arr[-1]
    mid = arr[len(arr) // 2]
    
    # Находим медиану из трех
    if first <= mid <= last or last <= mid <= first:
        return mid
    elif mid <= first <= last or last <= first <= mid:
        return first
    else:
        return last


def quick_sort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    Выполняет быструю сортировку на месте (in-place).
    
    Args:
        arr: Список целых чисел для сортировки
        low: Нижняя граница
        high: Верхняя граница
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Находим индекс разделения
        pi = _partition(arr, low, high)
        
        # Рекурсивно сортируем элементы до и после разделения
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)


def _partition(arr: List[int], low: int, high: int) -> int:
    """
    Функция разделения для in-place сортировки.
    
    Args:
        arr: Список целых чисел
        low: Нижняя граница
        high: Верхняя граница
        
    Returns:
        Индекс опорного элемента после разделения
    """
    # Выбираем последний элемент как опорный
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1