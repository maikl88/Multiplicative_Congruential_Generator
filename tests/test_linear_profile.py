import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from srs.mcg import create_generators


def berlekamp_massey(sequence):
    """
    Реализация алгоритма Берлекампа-Мэсси для вычисления линейной сложности
    последовательности
    """
    n = len(sequence)
    c = [0] * n  # текущий LFSR
    b = [0] * n  # предыдущий LFSR
    c[0], b[0] = 1, 1

    L, m = 0, -1  # L - длина LFSR, m - последнее изменение

    for i in range(n):
        d = sequence[i]  # вычисление расхождения
        for j in range(1, L + 1):
            d ^= c[j] & sequence[i - j]

        if d:  # если есть расхождение
            t = c.copy()
            for j in range(i - m):
                if i - j < n:
                    c[i - j] ^= b[j]
            if L <= i // 2:
                L = i + 1 - L
                m = i
                b = t

    return L


def calculate_complexity_profile(sequence):
    """
    Вычисляет профиль линейной сложности для последовательности
    """
    n = len(sequence)
    profile = []

    for k in range(1, n + 1):
        subsequence = sequence[:k]
        complexity = berlekamp_massey(subsequence)
        profile.append(complexity)

    return profile


def binary_sequence_from_numbers(numbers, bits=31):
    """
    Преобразует последовательность чисел в битовую последовательность
    """
    binary_sequence = []
    for num in numbers:
        # Преобразуем число в битовую строку и берем младшие биты
        binary = format(num, f'0{bits}b')[-bits:]
        binary_sequence.extend([int(b) for b in binary])
    return binary_sequence


def test_linear_complexity(sequence_length=1000):
    """
    Выполняет тест профиля линейной сложности
    """
    generator = create_generators()
    sequence = generator.generate_sequence(sequence_length)

    # Преобразуем в битовую последовательность
    binary_sequence = binary_sequence_from_numbers(sequence)

    # Вычисляем профиль
    profile = calculate_complexity_profile(binary_sequence)

    # Создаем график
    plt.figure(figsize=(12, 6))

    # График профиля линейной сложности
    x = range(1, len(profile) + 1)
    plt.plot(x, profile, 'b-', label='Профиль линейной сложности')

    # Идеальная линия N/2
    plt.plot(x, [n / 2 for n in x], 'r--', label='Идеальная линия (N/2)')

    plt.title('Профиль линейной сложности')
    plt.xlabel('Длина подпоследовательности (N)')
    plt.ylabel('Линейная сложность (L)')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.savefig(f'linear_complexity_{sequence_length}.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Анализ результатов
    print(f"\nАнализ профиля линейной сложности:")
    print(f"Длина последовательности: {len(binary_sequence)}")
    print(f"Конечная линейная сложность: {profile[-1]}")

    # Вычисляем отклонение от идеальной линии
    ideal_line = [n / 2 for n in x]
    mean_deviation = np.mean([abs(p - i) for p, i in zip(profile, ideal_line)])
    print(f"Среднее отклонение от идеальной линии: {mean_deviation:.2f}")


if __name__ == "__main__":
    # Тестируем с меньшей длиной последовательности для начала
    test_linear_complexity(100)  # для демонстрации