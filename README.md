# Axel Meloni (Erasmus student) - Programming project 2022-2023

I used the following dataset for the
project : https://www.kaggle.com/datasets/thedevastator/global-land-and-surface-temperature-trends-analy?select=GlobalTemperatures.csv

The dataset shows the evolution of average temperature over the years from different cities in the world. I explored the
data to show some interesting aspects and draw differents plots.

# Exploration and cleaning

I did a basic exploration of the dataset, I showed some useful data to know :

- the interval of time of the data
- the list of cities present in the dataset
- the list of country present in the dataset

the dates were string that I convert into datetime type and I grouped the data by years as the data for each month are
too precise for the range of our time (~300years)

During the exploration I could find that some AverageTemperature and AverageTemperatureUncertainty values were null.
To clean them I decided to fill the null value with the value of the previous year as it shouldn't be a huge difference
between two consecutive years.

From the exploration I could compute the delta of the temperature for each city and each country and thus find the
cities and countries the most and less affected by the average temperature evolution

# Plots

I draw some plots to show the evolution of the temperatures.

Here is what I've drawn :

- Evolution of the temperature of a city
- Evolution of the temperature of a country
- Evolution of the temperature of a continent
- Evolution of the temperature of a latitude group
- Evolution of the world temperature

I grouped the cities in 3 latitude groups :

- Equator = cities between 30°N and 30°S
- South = cities below 30°S
- North = cities above 30°N

In the plots I have drawn the exact temperature values and a line more smooth to see better the evolution of the
temperature.
For each drawing there is also the AverageTemperatureUncertainty that correspond to the error of temperature for each
year. On the plots we can see that the error is always very high for the first years and reduces as we approach to the
more recent years.
This should be because we had more precise tools to register the temperature in recent years than 300years ago

With the graphs we can see that globally the temperatures are rising everywhere but the evolution is more pronounced for
countries away from the equator.
We can also find thanks to the graph showing the evolution of the world temperature that there is a big rise just after
1800 during approximately 15 years (that correspond approximately to the peak of the industrial revolution)

# Git

For the project I used github.

I have opened some issues to follow my progress and to be sure that I didn't forget something to do over the time.
I have also used different branches to implement main functionality even if it was a little useless as I was the only
one working on this project. So I just prohibited the push on master and I was working on other branch and then I was
merging my work directly into master when the functionalities were finished.

# Streamlit

I implement two pages with streamlit that resume my work.

However, the plots on streamlit are very slow and are not render as good as in the python script, so I just displayed with streamlit the plots of the evolution of average temperature for one city and the one for the world.

I recommend to try both the streamlit view and the python script. To switch from one to another, please go at the end of the file 'main.py' and comment the line you don't want to use