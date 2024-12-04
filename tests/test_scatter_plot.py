import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from srs.mcg import create_generators


def test_plane_distribution(sequence_length=1000):
    """
    Тест распределения точек на плоскости согласно методике 4.1.2
    Args:
        sequence_length: длина последовательности n
    """
    # Создаем генератор
    generator = create_generators()

    # Получаем параметры
    R = 31  # разрядность для N = 2^31
    field_size = 2 ** R - 1  # размер поля

    # Генерируем последовательность
    sequence = generator.generate_sequence(sequence_length)

    # Создаем пары точек (εᵢ, εᵢ₊₁)
    x_coords = sequence[:-1]  # все элементы кроме последнего
    y_coords = sequence[1:]  # все элементы кроме первого

    # Создаем график
    plt.figure(figsize=(12, 12))

    # Основной график разброса точек
    plt.scatter(x_coords, y_coords, alpha=0.5, s=1)

    # Добавляем сетку
    plt.grid(True, alpha=0.3)

    # Добавляем подписи
    plt.title(
        f'Распределение на плоскости\nДлина последовательности: {sequence_length}, Размер поля: {field_size}x{field_size}')
    plt.xlabel('εᵢ')
    plt.ylabel('εᵢ₊₁')

    # Устанавливаем одинаковый масштаб по осям
    plt.axis('equal')

    # Устанавливаем пределы осей от 0 до field_size
    plt.xlim(0, field_size)
    plt.ylim(0, field_size)

    # Сохраняем график
    plt.savefig(f'plane_distribution_correct_{sequence_length}.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Статистический анализ
    print(f"\nСтатистический анализ распределения на плоскости:")
    print(f"Длина последовательности: {sequence_length}")
    print(f"Размер поля: {field_size}x{field_size}")
    print(f"Количество точек: {len(x_coords)}")

    # Корреляционный анализ
    correlation = np.corrcoef(x_coords, y_coords)[0, 1]
    print(f"\nКоэффициент корреляции между εᵢ и εᵢ₊₁: {correlation:.4f}")


if __name__ == "__main__":
    # Тестируем с разными длинами последовательности
    test_plane_distribution(1000)
    test_plane_distribution(10000)