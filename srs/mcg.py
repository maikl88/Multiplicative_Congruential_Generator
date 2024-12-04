class MCG:
    def __init__(self, N, a, c, x0):
        """
        Initialize MCG with parameters:
        N = 2^31 (модуль)
        a = x0 = 2q + 3 (множитель и начальное значение)
        c = 0 (приращение)
        q = 4
        """
        self.N = N
        self.a = a
        self.c = c
        self.current = x0
        self.initial_x0 = x0

    def next(self):
        """Генерирует следующее число в последовательности"""
        self.current = (self.a * self.current + self.c) % self.N
        return self.current

    def reset(self):
        """Сброс генератора к начальному состоянию"""
        self.current = self.initial_x0

    def generate_sequence(self, length):
        """Генерирует последовательность заданной длины"""
        return [self.next() for _ in range(length)]

    def get_normalized_next(self):
        """Возвращает следующее число, нормализованное к интервалу [0,1]"""
        return self.next() / self.N


def create_generators():
    """Создает генератор с параметрами из задания"""
    N = 2 ** 31  # N = 2^31
    q = 4  # q = 4
    c = 0  # c = 0

    # a = x0 = 2q + 3 = 2*4 + 3 = 11
    a = x0 = 2 * q + 3

    return MCG(N=N, a=a, c=c, x0=x0)


# Создаем экземпляр генератора
generator = create_generators()

if __name__ == "__main__":
    # Демонстрация работы генератора
    print(f"Параметры генератора:")
    print(f"N = 2^31 = {2 ** 31}")
    print(f"a = x0 = 2*4 + 3 = {2 * 4 + 3}")
    print(f"c = {0}")
    print(f"q = {4}")

    print("\nПервые 10 сгенерированных чисел:")
    sequence = generator.generate_sequence(10)
    for i, num in enumerate(sequence, 1):
        print(f"Число {i}: {num}")

    print("\nПервые 10 нормализованных чисел (в интервале [0,1]):")
    generator.reset()
    for i in range(10):
        print(f"Число {i + 1}: {generator.get_normalized_next():.10f}")