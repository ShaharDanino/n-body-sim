from vector import Vector
from star_RK import Star_RK
from globals import *
from utility import *
from copy import deepcopy
import pickle
from datetime import datetime

class Simulation_RK:
    def __init__(self, n, initial_stars=[]):
        self.stars = []
        self.energy = []
        self.angular_momentum = []
        total_momentum = Vector()
        if n > 6:
            for _ in range(n):
                self.stars.append(Star_RK())
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
        if self.stars[0].p.x < 150e9 and self.stars[0].p.x > 149e9:
            print("something")
        self.dt_array.append(dt)
        elapsed_time_weeks = self.dt_array[-1]/(86400 * 7)
        self.time_array.append(self.time_array[-1] + elapsed_time_weeks)
        previous_stars = deepcopy(self.stars)
        RK4 = [deepcopy(self.stars) for _ in range(4)]

        # calculates acceloration for every star in the stars array
        for s in RK4[0]:
            s.calculate_star_gravitations(RK4[0])

        for s, s2 in zip(RK4[1], RK4[0]):
            s.update(previous_stars, dt / 2, vk=s2.a, pk=s2.v)
        for s, s2, pv in zip(RK4[1], RK4[0], previous_stars):
            s.v = pv.v + s2.a * (dt / 2)
            s.calculate_star_gravitations(RK4[1])

        for s, s2 in zip(RK4[2], RK4[1]):
            s.update(previous_stars, dt / 2, vk=s2.a, pk=s2.v)
        for s, s2, pv in zip(RK4[2], RK4[1], previous_stars):
            s.v = pv.v + s2.a * (dt / 2)
            s.calculate_star_gravitations(RK4[2])

        for s, s2 in zip(RK4[3], RK4[2]):
            s.update(previous_stars, dt, vk=s2.a, pk=s2.v)
        for s, s2, pv in zip(RK4[3], RK4[2], previous_stars):
            s.v = pv.v + s2.a * dt
            s.calculate_star_gravitations(RK4[3])

        #calculates final acceloration and moves stars
        for s, s1, s2, s3, s4, pv in zip(self.stars, RK4[0], RK4[1], RK4[2], RK4[3], previous_stars):
            s.a = (s1.a + (s2.a + s3.a) * 2 + s4.a) / 6
            s.v = (s1.v + (s2.v + s3.v) * 2 + s4.v) / 6
            s.apply_velocity(dt) #moves star based on previous velocity
            s.v = pv.v
            s.apply_acceleration(dt)
        self.STARS_ARRAY.append(deepcopy(self.stars))

    def calc_total_energy(self):
        E = self.stars[0].calculate_potential_energy(self.stars[1])
        E += self.stars[0].calculate_kinetic_energy(self.stars[1])

        return E / (self.stars[0].m + self.stars[1].m)

    def calc_angular_momentum(self):
        l = self.stars[0].calc_angular_momentum(self.stars[1])
        return l

    def printer(self):
        if self.stars[0].bound_check(self.stars[1]):
            print("The system is bound")
        else:
            print("The system is not bound and will fall apart")
        print(len(self.STARS_ARRAY))

    def run(self, duration):
        runtime = 0
        while runtime < duration:
            self.energy.append(self.calc_total_energy())
            self.angular_momentum.append(self.calc_angular_momentum())
            self.printer()
            print(int((runtime / (duration * 1.0)) * 100), "%")
            if len(self.STARS_ARRAY) % 100 == 0:
                self.printer()
            self.iterate()
            runtime += self.dt_array[-1]
        self.printer()
        with open(f"DT_ARRAY_RUNGE", "wb") as file:
            pickle.dump(self.dt_array, file)
        with open(f"STARS_ARRAY_RUNGE", "wb") as file:
            pickle.dump(self.STARS_ARRAY, file)
        with open(f"TIME_ARRAY_RUNGE", 'wb') as file:
            pickle.dump(self.time_array, file)
        with open("energy_track_runge", "wb") as file:
            pickle.dump(self.energy, file)
        with open("angular_momentum_runge", "wb") as file:
            pickle.dump(self.angular_momentum, file)


    def from_stars(self, stars_array):
        self.stars = stars_array
        self.STARS_ARRAY = [deepcopy(self.stars)]
        self.dt_array = [86400]