from globals import *
from vector import Vector
import random
import math

class Star_RK:
    def __init__(self, pos=[0, 0, 0], vel=[0, 0, 0], mass=M_SUN):
        self.p = Vector(pos)

        self.v = Vector(vel)

        self.a = Vector()

        self.m = mass
        # self.g = gravity


    def __eq__(self, other):
        return self.p == other.p and self.v == other.v and self.a == other.a and self.m == other.m


    def randomize_star(self, pos_reach, vel_reach, mass_reach):
        self.p.randomize_vector(pos_reach)
        self.v.randomize_vector(vel_reach)
        self.m = random.uniform(mass_reach[0], mass_reach[1])


    def distance(self, other_star):
        return (other_star.p - self.p).calculate_magnitude()
        # return math.sqrt(sum((other_star.pos[i] - self.p[i])**2 for i in range(DIMENSIONS)))

    def calculate_kinetic_energy(self, other_star):
        Ke1 = (self.m / 2) * (self.v.calculate_magnitude() ** 2)
        Ke2 = (other_star.m / 2) * (other_star.v.calculate_magnitude() ** 2)
        return Ke1 + Ke2

    # def calculate_total_Ke(self, stars):
    #     total_Ke = 0.0
    #     for s in stars:
    #         total_Ke += s.calculate_kinetic_energy()
    #     return total_Ke


    def calculate_potential_energy(self, other_star, softening=1e7): # Check how to calculate the total potential energy of the system
        r = self.distance(other_star)
        r_softened = max(r, softening)
        Pe = -(G * (self.m * other_star.m) / (r_softened))
        return Pe

    def bound_check(self, other_star):
        print(self.calculate_potential_energy(other_star) + self.calculate_kinetic_energy(other_star))
        if (self.calculate_potential_energy(other_star) + self.calculate_kinetic_energy(other_star)) > 0:
            return False
        return True

    def calculate_momentum(self):
        return self.v * self.m

    # def apply_forces(self, other_star, softening=1e7):
    #     r = self.distance(other_star)
    #     r_softened = max(r, softening)
    #     self.g = G * (self.m * other_star.m) / (r_softened ** 2)

    def calculate_star_gravitation(self, other_star, softening=1e7):
        r = self.distance(other_star)
        r_softened = max(r, softening)
        gravitation = G * (self.m * other_star.m) / (r_softened ** 2)

        return (other_star.p - self.p).normalized() * gravitation

    def calculate_star_gravitations(self, stars, softening=1e7):
        self.a = Vector()
        for other_star in stars:
            if other_star == self:
                continue

            force = self.calculate_star_gravitation(other_star, softening=softening)
            self.a += force / self.m

    def apply_acceleration(self, dt):
        self.v += self.a * dt

    def apply_velocity(self, dt):
        self.p += self.v * dt

    def calc_angular_momentum(self, other_star):
        rx = self.p.x - other_star.p.x
        ry = self.p.y - other_star.p.y
        r = Vector([rx, ry, 0])
        m = self.m

        return m * r.cross_product(self.v)

    def update(self, stars, dt, vk=None, pk=None, softening=1e7):
        if vk and pk:
            self.a = vk
            self.v = pk
            self.apply_velocity(dt)
        else:
            self.calculate_star_gravitations(stars, softening)
            self.apply_acceleration(dt)
            self.apply_velocity(dt)




    # def __str__(self):
    #     return str(f'Star: a{self.a}, v{self.v}, p{self.p}, m({self.m})')


#To change the function of the location to x=x0+v0t+1/2at^2