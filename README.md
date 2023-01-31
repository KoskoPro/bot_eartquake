# bot_eartquake

Hello. This is my first project on Python.
This is a telegram bot that connects via api to the https://earthquake.usgs.gov/ database.
The user enters the following data: start_time, end_time, latitude, longitude, max_radius, min magnitude.
The bot gives the result of all earthquakes in the specified user parameters.
During the input of parameters, there is a check on the input data.
Result example:

2021-11-11 - 2021-11-21, Lt: 00,Lg: 0, radius 20000, minmagnitude 3 

1. Place: 232 km SSW of Pelabuhanratu, Indonesia. Magnitude: 4.3
2. Place: 44 km ESE of Bobon, Philippines. Magnitude: 5
3. Place: Volcano Islands, Japan region. Magnitude: 4.3
4. Place: 3 km S of Lomas de Sargentillo, Ecuador. Magnitude: 4.7
5. Place: 98 km NNW of Charlotte Amalie, U.S. Virgin Islands. Magnitude: 3.62
6. Place: Kuril Islands. Magnitude: 4.4
7. ............
