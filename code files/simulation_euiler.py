from vector import Vector
from star_euiler import Star_euiler
from globals import *
from utility import *
from copy import deepcopy
import pickle
from datetime import datetime

class Simulation_euiler:
    def __init__(self, n, initial_stars=[]):
        self.stars = []
        self.energy = []
        self.angular_momentum = []
        total_momentum = Vector()
        if n > 6:
            for _ in range(n):
                self.stars.append(Star_euiler())
                self.stars[-1].randomize_star(
                    [M_TO_LY * 0, M_TO_LY * 0],
                    [km_to_m(0), km_to_m(0)],
                    [M_SUN, M_SUN])
                if len(initial_stars) >= len(self.stars):
                    initial_star = initial_stars[len(self.stars) - 1]
                    star = self.stars[-1]
                    if not initial_star.p is None:
                        star.p = initial_star.p
                    if not initial_star.v is None:
                        star.v = initial_star.v
                    if not initial_star.m is None:
                        star.m = initial_star.m
                total_momentum += self.stars[-1].calculate_momentum()
            self.STARS_ARRAY = [deepcopy(self.stars)]
        else:
            self.STARS_ARRAY = [deepcopy(initial_stars[:n])]
            self.stars = initial_stars[:n]
        self.dt_array = [86400]
        self.time_array = [0]

    def iterate(self):
        dt = calculate_time_step(self.stars, self.dt_array[-1])
        self.dt_array.append(dt)
        elapsed_time_weeks = self.dt_array[-1]/(86400 * 7)
        self.time_array.append(self.time_array[-1] + elapsed_time_weeks)
        previous_stars = deepcopy(self.stars)
        for i, s in enumerate(self.stars):
            s.update(previous_stars, dt, self.STARS_ARRAY[-1][i].v)
        self.STARS_ARRAY.append(deepcopy(self.stars))

    def printer(self):
        if self.stars[0].bound_check(self.stars[1]):
            print("The system is bound")
        else:
            print("The system is not bound and will fall apart")
        print(len(self.STARS_ARRAY))

    def calc_angular_momentum(self):
        l = self.stars[0].calc_angular_momentum(self.stars[1])
        return l

    def calc_total_energy(self):
        E = self.stars[0].calculate_potential_energy(self.stars[1])
        E += self.stars[0].calculate_kinetic_energy(self.stars[1])

        return E / (self.stars[0].m + self.stars[1].m)

    def run(self, duration):
        runtime = 0
        while runtime < duration:
            self.angular_momentum.append(self.calc_angular_momentum())
            self.energy.append(self.calc_total_energy())
            print(int((runtime / (duration * 1.0)) * 100), "%")
            if len(self.STARS_ARRAY) % 100 == 0:
                self.printer()
            self.iterate()
            runtime += self.dt_array[-1]
        self.printer()
        with open(f"DT_ARRAY_EULER", "wb") as file:
            pickle.dump(self.dt_array, file)
        with open(f"STARS_ARRAY_EULER", "wb") as file:
            pickle.dump(self.STARS_ARRAY, file)
        with open(f"TIME_ARRAY_EULER", 'wb') as file:
            pickle.dump(self.time_array, file)
        with open("energy_track_euler", "wb") as file:
            pickle.dump(self.energy, file)
        with open("angular_momentum_euler", "wb") as file:
            pickle.dump(self.angular_momentum, file)



    def from_stars(self, stars_array):
        self.stars = stars_array
        self.STARS_ARRAY = [deepcopy(self.stars)]
        self.dt_array = [86400]