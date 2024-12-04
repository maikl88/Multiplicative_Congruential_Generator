import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from srs.mcg import create_generators


def to_binary_string(number, bits=31):
    """Преобразует число в битовую строку фиксированной длины"""
    return format(number, f'0{bits}b')


def count_series(sequence, k=3):
    """
    Подсчитывает частоту появления серий длины k в битовом представлении чисел
    """
    # Словари для подсчета
    bit_counts = {'0': 0, '1': 0}  # подсчет отдельных битов
    series_counts = {}  # подсчет серий длины k

    # Генерируем все возможные серии длины k
    all_series = [format(i, f'0{k}b') for i in range(2 ** k)]
    for series in all_series:
        series_counts[series] = 0

    total_bits = 0

    # Анализ каждого числа в последовательности
    for number in sequence:
        binary = to_binary_string(number)
        total_bits += len(binary)

        # Подсчет отдельных битов
        for bit in binary:
            bit_counts[bit] += 1

        # Подсчет серий длины k
        for i in range(len(binary) - k + 1):
            series = binary[i:i + k]
            if series in series_counts:
                series_counts[series] += 1

    return bit_counts, series_counts, total_bits


def test_series(sequence_length=1000, k=3):
    """
    Выполняет тест проверки серий для последовательности
    """
    generator = create_generators()
    sequence = generator.generate_sequence(sequence_length)

    # Подсчет частот
    bit_counts, series_counts, total_bits = count_series(sequence, k)

    # Вывод результатов
    print(f"\nРезультаты анализа серий (длина последовательности: {sequence_length}):")
    print(f"\nЧастота появления отдельных битов:")
    for bit, count in bit_counts.items():
        frequency = count / total_bits
        print(f"Бит {bit}: {count} раз ({frequency:.4f})")

    print(f"\nЧастота появления серий длины {k}:")
    for series, count in sorted(series_counts.items()):
        frequency = count / (total_bits - k + 1)
        print(f"Серия {series}: {count} раз ({frequency:.4f})")

    # Визуализация результатов
    # График для отдельных битов
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.bar(bit_counts.keys(),
            [count / total_bits for count in bit_counts.values()],
            color=['blue', 'green'])
    plt.title('Частота появления битов')
    plt.ylabel('Относительная частота')
    plt.axhline(y=0.5, color='r', linestyle='--', label='Идеальная частота (0.5)')
    plt.legend()

    # График для серий
    plt.subplot(1, 2, 2)
    series_labels = list(series_counts.keys())
    series_frequencies = [count / (total_bits - k + 1) for count in series_counts.values()]
    ideal_frequency = 1 / (2 ** k)

    plt.bar(series_labels, series_frequencies)
    plt.title(f'Частота появления серий длины {k}')
    plt.xticks(rotation=45)
    plt.ylabel('Относительная частота')
    plt.axhline(y=ideal_frequency, color='r', linestyle='--',
                label=f'Идеальная частота (1/{2 ** k})')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'series_analysis_{sequence_length}.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Статистический анализ
    print("\nСтатистический анализ:")
    # Хи-квадрат тест для битов
    expected_bit_count = total_bits / 2
    chi_square_bits = sum((count - expected_bit_count) ** 2 / expected_bit_count
                          for count in bit_counts.values())
    print(f"Хи-квадрат статистика для битов: {chi_square_bits:.4f}")

    # Хи-квадрат тест для серий
    expected_series_count = (total_bits - k + 1) / (2 ** k)
    chi_square_series = sum((count - expected_series_count) ** 2 / expected_series_count
                            for count in series_counts.values())
    print(f"Хи-квадрат статистика для серий: {chi_square_series:.4f}")


if __name__ == "__main__":
    # Тестируем с разными размерами последовательности
    test_series(1000)
    test_series(10000)
    test_series(100000)