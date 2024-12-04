import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from srs.mcg import create_generators


def calculate_acf(sequence, max_lag=50):
    """
    Вычисляет автокорреляционную функцию для последовательности

    Args:
        sequence: исследуемая последовательность
        max_lag: максимальное значение сдвига
    Returns:
        acf: массив значений автокорреляции для разных сдвигов
    """
    # Нормализация последовательности
    sequence = np.array(sequence)
    n = len(sequence)
    mean = np.mean(sequence)
    var = np.var(sequence)
    normalized_seq = (sequence - mean) / np.sqrt(var)

    # Вычисление ACF для разных сдвигов
    acf = np.zeros(max_lag + 1)
    for lag in range(max_lag + 1):
        # Вычисление корреляции для текущего сдвига
        acf[lag] = np.sum(normalized_seq[:(n - lag)] * normalized_seq[lag:]) / n

    return acf


def test_autocorrelation(sequence_length=10000, max_lag=50):
    """
    Выполняет тест автокорреляции для последовательности
    """
    generator = create_generators()
    sequence = generator.generate_sequence(sequence_length)

    # Вычисляем ACF
    acf = calculate_acf(sequence, max_lag)

    # Вычисляем доверительные интервалы (95%)
    confidence_interval = 1.96 / np.sqrt(sequence_length)

    # Создаем график
    plt.figure(figsize=(12, 6))
    lags = np.arange(max_lag + 1)

    # Основной график ACF
    plt.stem(lags, acf, basefmt='b-', linefmt='b-', markerfmt='bo', label='ACF')

    # Добавляем доверительные интервалы
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axhline(y=confidence_interval, color='r', linestyle='--', alpha=0.5,
                label='95% доверительный интервал')
    plt.axhline(y=-confidence_interval, color='r', linestyle='--', alpha=0.5)

    plt.title('Автокорреляционная функция')
    plt.xlabel('Сдвиг (lag)')
    plt.ylabel('ACF')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.savefig(f'autocorrelation_{sequence_length}.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Анализ результатов
    print(f"\nАнализ автокорреляции (длина последовательности: {sequence_length}):")
    print(f"Максимальный сдвиг: {max_lag}")
    print(f"95% доверительный интервал: ±{confidence_interval:.4f}")

    # Поиск значимых корреляций
    significant_lags = np.where(np.abs(acf[1:]) > confidence_interval)[0] + 1
    if len(significant_lags) > 0:
        print("\nОбнаружены значимые корреляции для сдвигов:")
        for lag in significant_lags:
            print(f"Сдвиг {lag}: ACF = {acf[lag]:.4f}")
    else:
        print("\nЗначимых корреляций не обнаружено")


if __name__ == "__main__":
    # Тестируем с разными размерами последовательности
    test_autocorrelation(10000)
    test_autocorrelation(100000)