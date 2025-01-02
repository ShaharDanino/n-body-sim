import math
import random
from globals import DIMENSIONS

class Vector:
    def __init__(self, arr=[0, 0, 0]):
        self.x = arr[0]
        self.y = arr[1]
        if len(arr) == 3:
            self.z = arr[2]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def randomize_vector(self, reach):
        self.x = random.uniform(reach[0], reach[1])
        self.y = random.uniform(reach[0], reach[1])
        self.z = 0
        if DIMENSIONS == 3:
            self.z = random.uniform(reach[0], reach[1])

    def cross_product(self, other_vector):
        return self.x * other_vector.y - self.y * other_vector.x

    def calculate_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __add__(self, other):
        return Vector([
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        ])

    def __sub__(self, other):
        return Vector([
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        ])

    def __mul__(self, scalar):
        return Vector([
            scalar * self.x,
            scalar * self.y,
            scalar * self.z
        ])

    def __truediv__(self, scalar):
        return Vector([
            self.x / scalar,
            self.y / scalar,
            self.z / scalar
        ])

    def normalized(self):
        return self / self.calculate_magnitude()

    # def __str__(self):
    #     if DIMENSIONS == 2:
    #         return f'({self.x}, {self.y})'
    #     elif DIMENSIONS == 3:
    #         return f'({self.x}, {self.y}, {self.z})'