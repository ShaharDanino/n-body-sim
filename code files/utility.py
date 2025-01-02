from globals import M_TO_KM

def filter_stars(stars):
    avg = 0

    for star in stars:
        avg += star.m

    avg /= len(stars)

    new_arr = []

    for star in stars:
        if star.m < avg * 1000:
            new_arr.append(star)

    return new_arr
def calculate_time_step(stars, last_dt):

    min_temp = float('inf')

    new_arr = filter_stars(stars)

    for star in new_arr:
        if star.m < (stars[0].m * 100000):
            v_mag = star.v.calculate_magnitude()
            a_mag = star.a.calculate_magnitude()

            if a_mag == 0:
                return 86400.0  # A default time step if acceleration is zero

            temp = v_mag / a_mag
            min_temp = min(min_temp, temp)

    dt_next = min_temp * 0.01

    return min(dt_next, last_dt * 1.1)


def m_to_km_per_sec_sqrd(a):
    return a / M_TO_KM


def km_to_m_per_sec_sqrd(a):
    return a * M_TO_KM


def m_to_km(v):
    return v / M_TO_KM


def km_to_m(v):
    return v * M_TO_KM


def yr_to_secs(t):
    return t * 60 * 60 * 24 * 365.25


def secs_to_hours(time_in_sec):
    return time_in_sec // (60 * 60)


def secs_to_min(time_in_sec):
    return time_in_sec // 60
