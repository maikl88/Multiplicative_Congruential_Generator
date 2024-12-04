import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from srs.mcg import create_generators


def find_monotonic_sequences(numbers):
    """
    Находит длины последовательных участков возрастания и убывания
    Возвращает два списка длин: для возрастающих и убывающих участков
    """
    increasing_lengths = []
    decreasing_lengths = []

    current_length = 1
    current_increasing = None

    for i in range(1, len(numbers)):
        if current_increasing is None:
            current_increasing = numbers[i] > numbers[i - 1]
            continue

        if current_increasing and numbers[i] > numbers[i - 1]:
            current_length += 1
        elif not current_increasing and numbers[i] < numbers[i - 1]:
            current_length += 1
        else:
            # Сохраняем длину предыдущего участка
            if current_increasing:
                increasing_lengths.append(current_length)
            else:
                decreasing_lengths.append(current_length)
            # Начинаем новый участок
            current_length = 2
            current_increasing = not current_increasing

    # Добавляем последний участок
    if current_increasing:
        increasing_lengths.append(current_length)
    else:
        decreasing_lengths.append(current_length)

    return increasing_lengths, decreasing_lengths


def test_monotonicity(sequence_length=10000):
    """
    Выполняет тест на монотонность для последовательности
    """
    generator = create_generators()
    sequence = generator.generate_sequence(sequence_length)

    # Находим участки возрастания и убывания
    increasing_lengths, decreasing_lengths = find_monotonic_sequences(sequence)

    # Статистика
    print(f"\nАнализ монотонности (длина последовательности: {sequence_length}):")
    print(f"Количество участков возрастания: {len(increasing_lengths)}")
    print(f"Количество участков убывания: {len(decreasing_lengths)}")
    print(f"Средняя длина участка возрастания: {np.mean(increasing_lengths):.2f}")
    print(f"Средняя длина участка убывания: {np.mean(decreasing_lengths):.2f}")
    print(f"Максимальная длина участка возрастания: {max(increasing_lengths)}")
    print(f"Максимальная длина участка убывания: {max(decreasing_lengths)}")

    # Создаем гистограммы
    plt.figure(figsize=(15, 6))

    # Гистограмма длин участков возрастания
    plt.subplot(1, 2, 1)
    plt.hist(increasing_lengths, bins='auto', density=True, alpha=0.7)
    plt.title('Распределение длин участков возрастания')
    plt.xlabel('Длина участка')
    plt.ylabel('Частота')
    plt.grid(True, alpha=0.3)

    # Гистограмма длин участков убывания
    plt.subplot(1, 2, 2)
    plt.hist(decreasing_lengths, bins='auto', density=True, alpha=0.7)
    plt.title('Распределение длин участков убывания')
    plt.xlabel('Длина участка')
    plt.ylabel('Частота')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'monotonicity_analysis_{sequence_length}.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Дополнительная проверка - распределение длин должно быть убывающим
    # для действительно случайной последовательности
    print("\nПроверка распределения длин:")

    for length in range(2, max(max(increasing_lengths), max(decreasing_lengths))):
        inc_count = sum(1 for x in increasing_lengths if x == length)
        dec_count = sum(1 for x in decreasing_lengths if x == length)
        if inc_count > 0 or dec_count > 0:
            print(f"Длина {length}:")
            print(f"  Участки возрастания: {inc_count} раз")
            print(f"  Участки убывания: {dec_count} раз")


if __name__ == "__main__":
    test_monotonicity(10000)
    test_monotonicity(100000)