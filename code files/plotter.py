import matplotlib.pyplot as plt
from utility import m_to_km
from globals import M_SUN, AU, M_EARTH
import matplotlib.ticker as ticker
import pickle

def m_to_km(meters):
    return meters / 1000

def plot_v_a(history_array, dt_array, plot_type, time_array, i='None'):
    t_array = make_t_array(dt_array)
    check = ""
    if i == 'None':
        for star_array in zip(*history_array):
            if plot_type == 'vel':
                y_array = [m_to_km(s.v.calculate_magnitude()) for s in star_array]
                check = "vel"

            elif plot_type == 'acc':
                y_array = [m_to_km(s.a.calculate_magnitude()) for s in star_array]
                check = "acc"

            plt.plot(range(len(dt_array)), y_array)
            plt.xlabel("Time in weeks")
            if check == "vel":
                plt.title("Velocity as a function of time")
                plt.ylabel("Velocity in km/s")
            elif check == "acc":
                plt.title("Acceleration as a function of time")
                plt.ylabel("Acceleration in km/s^2")
        plt.show()
    else:
        star_array = list(zip(*history_array))
        if plot_type == 'vel':
            y_array = [m_to_km(s.v.calculate_magnitude()) for s in star_array]
            check = "vel"

        elif plot_type == 'acc':
            y_array = [m_to_km(s.a.calculate_magnitude()) for s in star_array]
            check = "acc"

        plt.plot(range(len(time_array)), y_array)
        plt.xlim(left=0, right=len(time_array))
        plt.xlabel("Time iterations")
        if check == "vel":
            plt.title("Velocity as a function of time iterations")
            plt.ylabel("Velocity in km/s")
        elif check == "acc":
            plt.title("Acceleration as a function of time iterations")
            plt.ylabel("Acceleration in km/s^2")
        plt.show()


def plot_pos():
    choice = int(input("What would you like to plot? (1 - Euler, 2 - Runge, 3 - Both): "))

    # Adjusting figure size
    fig, ax = plt.subplots(figsize=(10, 8))  # Increased figure size
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    with open("STARS_ARRAY_EULER", "rb") as file:
        stars_array_euler = pickle.load(file)

    with open("STARS_ARRAY_RUNGE", "rb") as file:
        stars_array_runge = pickle.load(file)

    with open("ANALYTIC_SOLUTION_X", "rb") as file:
        EXACT_SOLUTION_X = pickle.load(file)
    with open("ANALYTIC_SOLUTION_Y", "rb") as file:
        EXACT_SOLUTION_Y = pickle.load(file)

    if choice == 1 or choice == 3:
        for star_array in zip(*stars_array_euler):
            x_array = [s.p.x / AU for s in star_array]
            y_array = [s.p.y / AU for s in star_array]
            ax.plot(x_array, y_array, '#FF0000',
                     label="Euler's Orbit" if 'Euler\'s Orbit' not in [line.get_label() for line in ax.get_lines()] else "")

    if choice == 2 or choice == 3:
        for star_array in zip(*stars_array_runge):
            x_array = [s.p.x / AU for s in star_array]
            y_array = [s.p.y / AU for s in star_array]
            ax.plot(x_array, y_array, '#00FF00', linestyle='dashdot',
                     label="Runge-Kutta's Orbit" if 'Runge-Kutta\'s Orbit' not in [line.get_label() for line in ax.get_lines()] else "")

    for i in range(len(EXACT_SOLUTION_X)):
        EXACT_SOLUTION_X[i] /= AU
        EXACT_SOLUTION_Y[i] /= AU
    #ax.plot(EXACT_SOLUTION_X, EXACT_SOLUTION_Y, '#0000FF', label='Analytic Solution', linestyle='dashed')


    #ax.text(0, 0, 'm = M sun', fontsize=15)
    """ax.text((stars_array_runge[0][0].p.x + stars_array_runge[0][0].v.x) / AU,
             (stars_array_runge[0][0].p.y + stars_array_runge[0][0].v.y) / AU * 4000000,
             f'v = {(stars_array_runge[0][0].v.y / 30290):.1f} v earth', fontsize=20)
"""
    with open("orbital_eccentricity", "rb") as file:
        e = pickle.load(file)
    with open("energy_track_runge", "rb") as file:
        Energy = pickle.load(file)[0]
    with open("energy_track_euler_earth", "rb") as file:
        earth_energy = pickle.load(file)[0] * (-1)
    #ax.text(0.01, 0.99, f'eccentricity = {e:.2f}', ha='left', va='top', transform=ax.transAxes, fontsize=20)
    ax.text(0.01, 0.99, r"$\tilde{E}$ = " + f"{(Energy / earth_energy):.2f}", ha='left', va='top', transform=ax.transAxes, fontsize=20)
    ax.text(0.01, 0.95, f'v = {(stars_array_runge[0][0].v.y / 30290):.1f} v earth', ha='left', va='top',
            transform=ax.transAxes, fontsize=20)

    ax.arrow(stars_array_runge[0][0].p.x / AU, stars_array_runge[0][0].p.y / AU, stars_array_runge[0][0].v.x * 20000 / AU,
              stars_array_runge[0][0].v.y * 2000000 / AU, width=0.01, color='k', head_width=0.04)

    ax.arrow(stars_array_runge[0][1].p.x / AU, stars_array_runge[0][1].p.y / AU,
             stars_array_runge[0][1].v.x * 20000 / AU,
             stars_array_runge[0][1].v.y * 2000000 / AU, width=0.01, color='k', head_width=0.04)



    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("X (AU)", fontsize=20)
    ax.set_ylabel("Y (AU)", fontsize=20)

    # Set limits to ensure plot is centered and zoom out a bit
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    max_range = max(abs(x_min), abs(x_max), abs(y_min), abs(y_max))

    # Zoom out by a factor (e.g., 20%)
    zoom_out_factor = 0.95
    ax.set_xlim(-max_range * zoom_out_factor, max_range * zoom_out_factor)
    ax.set_ylim(-max_range * zoom_out_factor, max_range * zoom_out_factor)

    # Format the y-axis labels to use scientific notation
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(True)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_powerlimits((-1, 1))
    ax.tick_params(axis='y', which='major', labelsize=25)
    ax.tick_params(axis='x', which='major', labelsize=25)

    # Move the scientific notation exponent to the top-left of the y-axis
    ax.yaxis.get_offset_text().set_fontsize(15)
    ax.yaxis.get_offset_text().set_position((0, 1.05))

    # Set the legend location to upper right
    plt.legend(loc='upper right')

    # Adjust layout to add padding around the plot
    plt.tight_layout(pad=0)

    # Save the plot with minimal white space around it
    plt.savefig('plot_minimal_white_space.png', bbox_inches='tight', pad_inches=0)

    plt.show()

def plot_dt():
    with open("DT_ARRAY_EULER", "rb") as file:
        dt_array_euler = pickle.load(file)
    with open("DT_ARRAY_RUNGE", "rb") as file:
        dt_array_runge = pickle.load(file)
    with open("TIME_ARRAY_EULER", "rb") as file:
        time_array_euler = pickle.load(file)
    with open("TIME_ARRAY_RUNGE", "rb") as file:
        time_array_runge = pickle.load(file)
    with open("orbital_period", "rb") as file:
        T = pickle.load(file)

    i = int(input("Runge - 1, Euler - 2 , both - 3: "))
    fig, ax = plt.subplots(figsize=(10, 8))

    def normalize_arrays(time_array, dt_array, T):
        dt_array_normalized = [dt / T for dt in dt_array]
        time_array_normalized = [t * 7 * 24 * 60 * 60 / T for t in time_array]
        return time_array_normalized, dt_array_normalized
    if i == 1:
        time_array, dt_array = normalize_arrays(time_array_runge, dt_array_runge, T)
        ax.plot(time_array, dt_array, label="Runge")
    elif i == 2:
        time_array, dt_array = normalize_arrays(time_array_euler, dt_array_euler, T)
        ax.plot(time_array, dt_array, label="Euler")
    elif i == 3:
        time_array_euler_norm, dt_array_euler_norm = normalize_arrays(time_array_euler, dt_array_euler, T)
        time_array_runge_norm, dt_array_runge_norm = normalize_arrays(time_array_runge, dt_array_runge, T)
        ax.plot(time_array_euler_norm, dt_array_euler_norm, label="Euler")
        ax.plot(time_array_runge_norm, dt_array_runge_norm, label="Runge")

    plt.xlabel("Laps", fontsize=20)
    plt.ylabel("Time step value in seconds / orbital time", fontsize=20)

    # Format the y-axis labels to use scientific notation
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(True)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_powerlimits((-1, 1))
    ax.tick_params(axis='y', which='major', labelsize=25)
    ax.tick_params(axis='x', which='major', labelsize=25)

    # Move the scientific notation exponent to the top-left of the y-axis
    ax.yaxis.get_offset_text().set_fontsize(15)
    ax.yaxis.get_offset_text().set_position((0, 1.05))

    # Adjust the number of y-axis ticks
    ax.yaxis.set_major_locator(ticker.MaxNLocator(prune='both'))

    plt.tight_layout()
    plt.legend(loc="upper right")
    plt.show()

def plot_energy():
    with open("energy_track_euler", "rb") as file:
        energy_arr_euler = pickle.load(file)
    with open("TIME_ARRAY_EULER", "rb") as file:
        time_arr_euler = pickle.load(file)
    with open("energy_track_runge", "rb") as file:
        energy_arr_runge = pickle.load(file)
    with open("TIME_ARRAY_RUNGE", "rb") as file:
        time_arr_runge = pickle.load(file)
    with open("orbital_period", "rb") as file:
        T = pickle.load(file)
    with open("energy_track_euler_earth", "rb") as file:
        earth_energy = pickle.load(file)[0] * (-1)

    fig, ax = plt.subplots(figsize=(10, 8))
    choice = int(input("What method would you like to check: 1 - Runge, 2 - Euler, 3 - Both: "))

    def normalize_arrays(time_array, data_array, T):
        time_array_normalized = [t * 7 * 24 * 60 * 60 / T for t in time_array[:len(data_array)]]
        return time_array_normalized

    energy_arr_euler = [energy_arr_euler[i] / earth_energy for i in range(len(energy_arr_euler))]
    energy_arr_runge = [energy_arr_runge[i] / earth_energy for i in range(len(energy_arr_runge))]
    plt.xlabel("Laps", fontsize=20)
    plt.ylabel(r"$\tilde{E}$", fontsize=20)

    if choice == 1:
        time_arr = normalize_arrays(time_arr_runge, energy_arr_runge, T)
        ax.plot(time_arr, energy_arr_runge, label="Runge")
    elif choice == 2:
        time_arr = normalize_arrays(time_arr_euler, energy_arr_euler, T)
        ax.plot(time_arr, energy_arr_euler, label="Euler")
    elif choice == 3:
        time_arr_euler_norm = normalize_arrays(time_arr_euler, energy_arr_euler, T)
        time_arr_runge_norm = normalize_arrays(time_arr_runge, energy_arr_runge, T)
        ax.plot(time_arr_euler_norm, energy_arr_euler, label="Euler")
        ax.plot(time_arr_runge_norm, energy_arr_runge, label="Runge")

    # Format the y-axis labels to use scientific notation
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(True)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_powerlimits((-1, 1))
    ax.tick_params(axis='y', which='major', labelsize=25)
    ax.tick_params(axis='x', which='major', labelsize=25)

    # Move the scientific notation exponent to the top-left of the y-axis
    ax.yaxis.get_offset_text().set_fontsize(15)
    ax.yaxis.get_offset_text().set_position((0, 1.05))

    # Adjust the number of y-axis ticks
    ax.yaxis.set_major_locator(ticker.MaxNLocator(prune='both'))

    plt.tight_layout()
    plt.legend(loc="upper right")
    plt.show()

def plot_angular_momentum():
    with open("angular_momentum_euler", "rb") as file:
        angular_momentum_arr_euler = pickle.load(file)
    with open("TIME_ARRAY_EULER", "rb") as file:
        time_arr_euler = pickle.load(file)
    with open("angular_momentum_runge", "rb") as file:
        angular_momentum_arr_runge = pickle.load(file)
    with open("TIME_ARRAY_RUNGE", "rb") as file:
        time_arr_runge = pickle.load(file)
    with open("orbital_period", "rb") as file:
        T = pickle.load(file)

    fig, ax = plt.subplots(figsize=(10, 8))

    choice = int(input("What method would you like to check: 1 - Runge, 2 - Euler, 3 - Both: "))

    def normalize_arrays(time_array, data_array, T):
        time_array_normalized = [t * 7 * 24 * 60 * 60 / T for t in time_array[:len(data_array)]]
        return time_array_normalized

    angular_momentum_arr = []
    if choice == 1:
        time_arr = normalize_arrays(time_arr_runge, angular_momentum_arr_runge, T)
        angular_momentum_arr = angular_momentum_arr_runge
        ax.plot(time_arr, angular_momentum_arr_runge, label="Runge")
    elif choice == 2:
        time_arr = normalize_arrays(time_arr_euler, angular_momentum_arr_euler, T)
        angular_momentum_arr = angular_momentum_arr_euler
        ax.plot(time_arr, angular_momentum_arr_euler, label="Euler")
    elif choice == 3:
        time_arr_euler_norm = normalize_arrays(time_arr_euler, angular_momentum_arr_euler, T)
        time_arr_runge_norm = normalize_arrays(time_arr_runge, angular_momentum_arr_runge, T)
        ax.plot(time_arr_euler_norm, angular_momentum_arr_euler, label="Euler")
        ax.plot(time_arr_runge_norm, angular_momentum_arr_runge, label="Runge")
        # For limits, consider both arrays
        time_arr = time_arr_euler_norm + time_arr_runge_norm
        angular_momentum_arr = angular_momentum_arr_euler + angular_momentum_arr_runge

    # Set axis labels
    plt.xlabel("Laps", fontsize=20)
    plt.ylabel("Angular Momentum (kg * m^2 / s)", fontsize=20)

    # Format the y-axis labels to use scientific notation
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(True)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_powerlimits((-1, 1))
    ax.tick_params(axis='y', which='major', labelsize=25)
    ax.tick_params(axis='x', which='major', labelsize=25)

    # Move the scientific notation exponent to the top-left of the y-axis
    ax.yaxis.get_offset_text().set_fontsize(15)
    ax.yaxis.get_offset_text().set_position((0, 1.05))

    # Set the legend location to upper right
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.show()




def plotter(stars_filename='STARS_ARRAY', dt_filename='dt_array', i='None'):
    """with open("STARS_ARRAY_EULER", "rb") as file:
        stars_array_euler = pickle.load(file)
    with open("STARS_ARRAY_RUNGE", "rb") as file:
        stars_array_runge = pickle.load(file)
    with open("DT_ARRAY_EULER", "rb") as file:
        dt_array_euler = pickle.load(file)
    with open("DT_ARRAY_RUNGE", "rb") as file:
        dt_array_runge = pickle.load(file)
    with open("TIME_ARRAY_EULER", "rb") as file:
        time_array_euler = pickle.load(file)
    with open("TIME_ARRAY_RUNGE", "rb") as file:
        time_array_runge = pickle.load(file)
    with open("ANALYTIC_SOLUTION_X", "rb") as file:
        EXACT_SOULUTION_X = pickle.load(file)
    with open("ANALYTIC_SOLUTION_Y", "rb") as file:
        EXACT_SOULUTION_Y = pickle.load(file)

    if i != 'None':
        i = int(i)

    if plot_type in ['vel', 'acc']:
        plot_v_a(stars_array_euler, dt_array_euler, plot_type, time_array_euler, i=i)

    elif plot_type == 'dt':
        plot_dt(dt_array_euler, time_array_euler)

    elif plot_type == "dis":
        plot_dis(stars_array_euler, time_array_euler)

    elif plot_type == "pos":"""
    plot_pos()
    plot_dt()
    plot_energy()
    plot_angular_momentum()

    plt.show()

def main():
    #plot_type = input("What do you want to plot? pos, dis, vel, acc or dt? ")
    #i = input("To plot all bodies enter None, to plot some enter the index: ")
    plotter()

if __name__ == "__main__":
    main()
