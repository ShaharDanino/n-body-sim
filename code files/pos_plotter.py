import pickle
import pandas as pd
import plotly.express as px
from globals import DIMENSIONS  # Make sure to import DIMENSIONS
import utility
import plotly.graph_objects as go

skip = 10
def process_data(Stars_array, time_list):

    time_arr = []
    id_list = []
    velocity_value_x = []
    velocity_value_y = []
    velocity_value_z = []
    z_list = []
    x_list = []
    y_list = []
    star_id = 1

    # parses the information from the files to diffrent arrays
    for i in range(0, len(Stars_array), skip):
        for star in Stars_array[i]:
            id_list.append(star_id)
            star_id += 1

            velocity_value_x.append(star.v.x)

            velocity_value_y.append(star.v.y)

            velocity_value_z.append(star.v.z)

            x_list.append(star.p.x)

            y_list.append(star.p.y)

            z_list.append(star.p.z)

            time_arr.append(time_list[i])
        star_id = 1

    data = {
        'StarID': id_list,  # Unique identifier for each star
        'Time': time_arr,  # Time points
        'X': x_list,  # X-coordinate of each star
        'Y': y_list,  # Y-coordinate of each star
        'Z': z_list,  # Z-coordinate of each star
        'VELOCITY_X': velocity_value_x,
        'VELOCITY_Y': velocity_value_y
    }

    print("finished parsing the data")

    # Convert the data dictionary to a DataFrame
    df = pd.DataFrame(data)

    if (z_list[0] == 0 and z_list[1] == 0):
        # Scatter plot using Plotly Express
        fig = px.scatter(df, x='X', y='Y', color='StarID', animation_frame='Time', title='Star Positions Over Time',
                         labels={'StarID': 'Star ID', 'Time': 'Time', 'Velocity X': 'VELOCITY_X',
                                 'Velocity Y': 'VELOCITY_Y'})
    else:
        fig = px.scatter_3d(df, x='X', y='Y', z='Z', color='StarID', animation_frame='Time',
                            title='Star Positions Over Time',
                            labels={'StarID': 'Star ID', 'Time': 'Time', 'Velocity X': 'VELOCITY_X',
                                    'Velocity Y': 'VELOCITY_Y'})
    print("finished with the scatter function")
    fig.update_layout(yaxis_range=[-200597870700, 200597870700])
    fig.update_layout(xaxis_range=[-200597870700, 200597870700])
    print("showing plot")
    # Display the plot
    fig.show()

def main():
    with open("STARS_ARRAY_RUNGE", "rb") as file:
        stars_array = pickle.load(file)
        file.close()
    #with open("DT_ARRAY" , "rb") as file:
     #   dt_array = pickle.load(file)
      #  file.close()
    with open("TIME_ARRAY_RUNGE" , "rb") as file:
        time_array = pickle.load(file)
        file.close()

    process_data(stars_array, time_array)

if __name__ == "__main__":
    main()

    """
    # Add traces for star trajectories and points
    for star_id in range(1, len(Stars_array[0]) + 1):
        trajectory_x = []
        trajectory_y = []
        points_x = []
        points_y = []
        for i, time_stars in enumerate(Stars_array):
            for j, star in enumerate(time_stars):
                if j == star_id - 1:  # Adjust for 0-based indexing
                    trajectory_x.append(star.p.x)
                    trajectory_y.append(star.p.y)
                    points_x.extend([star.p.x] * 10)  # Assuming 10 time points per step
                    points_y.extend([star.p.y] * 10)
        fig.add_trace(go.Scatter(x=trajectory_x, y=trajectory_y, mode='lines', name=f'Star {star_id} Trajectory'))
        fig.add_trace(go.Scatter(x=points_x, y=points_y, mode='markers', name=f'Star {star_id} Points'))
    """

"""
    
"""

"""
    fig = go.Figure()
    time_list = [item for item in time_list for _ in range(2)]

    id_list = []
    velocity_value_x = []
    velocity_value_y = []
    velocity_value_z = []
    z_list = []
    x_list = []
    y_list = []
    star_id = 1

    #parses the information from the files to diffrent arrays
    for i in range(0,len(Stars_array),skip):
        for star in Stars_array[i]:
            id_list.append(id)
            star_id += 1

            velocity_value_x.append(star.v.x)

            velocity_value_y.append(star.v.y)

            velocity_value_z.append(star.v.z)

            x_list.append(star.p.x)

            y_list.append(star.p.y)

            z_list.append(star.p.z)

        star_id = 1
    """