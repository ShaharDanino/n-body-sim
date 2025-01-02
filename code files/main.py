import math

from simulation_RK import Simulation_RK
from utility import yr_to_secs
from star_RK import Star_RK
from globals import M_EARTH, AU, M_SUN
from utility import km_to_m
from star_euiler import Star_euiler
from simulation_euiler import Simulation_euiler
from exact_solution import main

def main():
    DIMENSIONS = int(input("How many dimensions do you want? "))
    N = int(input("How many bodies do you want? "))
    duration = yr_to_secs(10)
    simulation_ron = Simulation_RK(N, [
        Star_RK([AU, 0, 0], [0, -10000, 0], M_EARTH),
        Star_RK([0, 0, 0], [0, 0, 0], M_SUN),
        #Star_ronga([0, math.sqrt(3) * 10 * AU, 0], [km_to_m(-10), 0, 0]),
        #Star([-62500004980.16882, 839265540535.4622, 0], [-16309.327719849636, 16912.92334339637, 0]),
        #Star([-146185315941.9038, 828145565752.9617, 0], [-16309.327719849636, 16912.92334339637, 0]),
        #Star([566881252919.6533, 829069640517.2815, 0], [1173.100512993271, 0, 0]),
        #Star([303726252129.2898, 482251222050.04443, 0], [-13732.646224096738, 1526.4994964662546, 0], None),
        #Star([231091981037.9519, 165820317501.04517, 0], [-2156.06807416448, 42033.15753030315, 0], None),
        #Star([372148240411.5698, 14977871653.906006, 0], [-16486.020027402523, -2959.3354432422566, 0], None)
    ])

    simulation_euiler = Simulation_euiler(N, [
        Star_euiler([AU, 0, 0], [0, 10000, 0], M_EARTH),
        Star_euiler([0, 0, 0], [0, 0, 0], M_SUN),
        #Star_euiler([0, math.sqrt(3) * 10 * AU, 0], [km_to_m(-10), 0, 0]),
        # Star([-62500004980.16882, 839265540535.4622, 0], [-16309.327719849636, 16912.92334339637, 0]),
        # Star([-146185315941.9038, 828145565752.9617, 0], [-16309.327719849636, 16912.92334339637, 0]),
        # Star([566881252919.6533, 829069640517.2815, 0], [1173.100512993271, 0, 0]),
        # Star([303726252129.2898, 482251222050.04443, 0], [-13732.646224096738, 1526.4994964662546, 0], None),
        # Star([231091981037.9519, 165820317501.04517, 0], [-2156.06807416448, 42033.15753030315, 0], None),
        # Star([372148240411.5698, 14977871653.906006, 0], [-16486.020027402523, -2959.3354432422566, 0], None)
    ])

    choice = int(input("what kind of simulation would you like to run: (1 - ronga, 2 - euiler, 3 - both)"))
    if choice == 1:
        simulation_ron.run(duration=duration)
    elif choice == 2:
        simulation_euiler.run(duration = duration)
    else:
        simulation_ron.run(duration=duration)
        input("enter to countinue the simulation: ")
        simulation_euiler.run(duration=duration)

if __name__ == "__main__":
    main()
