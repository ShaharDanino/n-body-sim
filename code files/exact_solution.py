import math
import pickle

from globals import G, M_SUN, AU
import matplotlib.pyplot as plt


def calculate_eccentricity(m_central, v_orbiting, r0):
    v_squared = v_orbiting ** 2
    r0_squared = r0 ** 2

    return math.sqrt(1 + ((v_squared * r0_squared * (v_squared - ((2 * G * m_central)/r0))) / ((G ** 2) * (m_central ** 2))))


def calculate_semi_major(r0, v0, m, e):
    return ((r0 ** 2) * (v0 ** 2)) / (G * m * (1 - (e ** 2)))


def get_r(a, e, theta):
    return (a * (1 - e ** 2)) / (1 + (e * math.cos(theta)))


def calculate_period_time(a, m_sun):
    return 2 * math.pi * math.sqrt(math.pow(abs(a), 3) / (G * m_sun))
def main():
    m_sun = M_SUN
    v_orbiting = 10000
    distance = 2 * AU

    e = calculate_eccentricity(m_sun, v_orbiting, distance)
    print(str(e))

    a = calculate_semi_major(distance, v_orbiting, m_sun, e)
    print(str(a))

    T = calculate_period_time(a, m_sun)
    print(str(T / (60*24*60)))

    x_array = []
    y_array = []
    for angle in range(360):
        theta = math.radians(angle)
        r = get_r(a, e, theta)

        x_array.append(r * math.cos(theta))
        y_array.append(r * math.sin(theta))

    plt.plot(x_array, y_array)
    plt.axis("equal")

    plt.show()

    with open("ANALYTIC_SOLUTION_X", "wb") as file:
        pickle.dump(x_array, file)
    with open("ANALYTIC_SOLUTION_Y", "wb") as file:
        pickle.dump(y_array, file)
    with open("orbital_period", "wb") as file:
        pickle.dump(T, file)
    with open("orbital_eccentricity", "wb") as file:
        pickle.dump(e, file)


if __name__ == "__main__":
    main()
