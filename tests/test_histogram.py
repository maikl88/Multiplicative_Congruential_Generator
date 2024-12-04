import matplotlib

matplotlib.use('Agg')  # Установка бэкенда 'Agg' до импорта pyplot
import matplotlib.pyplot as plt
import numpy as np
from srs.mcg import create_generators


def test_histogram_distribution(sample_size=10000, num_bins=50):
    """
    Тест распределения элементов последовательности с помощью гистограммы

    Args:
        sample_size: размер выборки
        num_bins: количество интервалов для гистограммы
    """
    # Создаем генератор и получаем последовательность
    generator = create_generators()

    # Генерируем нормализованные числа (от 0 до 1)
    sequence = [generator.get_normalized_next() for _ in range(sample_size)]

    # Создаем гистограмму
    plt.figure(figsize=(12, 6))

    # Построение гистограммы
    counts, bins, _ = plt.hist(sequence, bins=num_bins, density=True,
                               alpha=0.7, color='blue', edgecolor='black')

    # Добавляем линию равномерного распределения для сравнения
    plt.axhline(y=1, color='r', linestyle='--', label='Идеальное равномерное распределение')

    # Вычисляем статистики
    mean_val = np.mean(sequence)
    std_val = np.std(sequence)

    # Добавляем подписи и информацию
    plt.title(f'Гистограмма распределения {sample_size} элементов последовательности\n'
              f'Среднее = {mean_val:.4f}, СКО = {std_val:.4f}')
    plt.xlabel('Значение')
    plt.ylabel('Плотность')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Сохраняем график в файл
    plt.savefig(f'histogram_{sample_size}.png')
    plt.close()

    # Выводим статистику
    print(f"Статистические характеристики распределения:")
    print(f"Размер выборки: {sample_size}")
    print(f"Среднее значение: {mean_val:.4f}")
    print(f"Стандартное отклонение: {std_val:.4f}")
    print(f"Минимальное значение: {min(sequence):.4f}")
    print(f"Максимальное значение: {max(sequence):.4f}")

    # Тест Колмогорова-Смирнова на равномерность
    from scipy import stats
    ks_statistic, p_value = stats.kstest(sequence, 'uniform')
    print(f"\nТест Колмогорова-Смирнова:")
    print(f"Статистика: {ks_statistic:.4f}")
    print(f"P-значение: {p_value:.4f}")


if __name__ == "__main__":
    # Запускаем тест с разными размерами выборки
    test_histogram_distribution(10000)
    test_histogram_distribution(100000)