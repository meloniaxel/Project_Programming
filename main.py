import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# Rectify the null values by taking the value of the previous row
# it should be coherent as the average temperature of 1 month shouldn't be very different from the previous one
# but if several null value are on consecutive rows it won't so accurate
# because all months will be at the same temperature
def rectify_null_values(dataset):
    print("\n#######################")
    print("Rectification of the dataset (fill null value with nearby values) ... \n")
    # Uncomment to see that AverageTemperature and AverageTemperatureUncertainty contain null values
    # dataset.info()

    # We extract the first line containing null AverageTemperature
    # and the line before without null value on AverageTemperature
    null_values_temp = dataset['AverageTemperature'].isnull()
    null_rows_temp = dataset[null_values_temp]
    first_null_temp = null_rows_temp.head(1)
    previous_index_temp = dataset['dt'] == first_null_temp['dt'].values[0] - 1
    previous_index_city = dataset['City'] == first_null_temp['City'].values[0]
    previous_row_temp = dataset[previous_index_temp & previous_index_city]

    # same with AverageTemperatureUncertainty
    # note : the lines are actually the same as those picked for the AverageTemperature
    null_values_uncertainty = dataset['AverageTemperatureUncertainty'].isnull()
    null_rows_uncertainty = dataset[null_values_uncertainty]
    first_null_uncertainty = null_rows_uncertainty.head(1)
    previous_index_uncertainty = dataset['dt'] == first_null_uncertainty['dt'].values[0] - 1
    previous_index_city = dataset['City'] == first_null_uncertainty['City'].values[0]
    previous_row_uncertainty = dataset[previous_index_uncertainty & previous_index_city]

    # rectify null values (!data must be sorted by city and date!)
    dataset['AverageTemperature'].fillna(method='ffill', inplace=True)
    dataset['AverageTemperatureUncertainty'].fillna(method='ffill', inplace=True)

    # uncomment to check that the value are correctly rectified
    # dataset.info()


def explore_data(dataset):
    print(" ## The dates go from", dataset.dt.min(), 'to', dataset.dt.max())
    print(" ## Here is the list of the cities of the dataset :\n", dataset.City.unique())
    print(" ## Here is the list of the countries of the dataset :\n", dataset.Country.unique())

    # Convert date string type in date time and keep only the year
    dataset['dt'] = pd.to_datetime(dataset['dt'])
    dataset['dt'] = dataset['dt'].dt.year
    # Group data by years keeping the mean temperature and mean temperature uncertainty of each year
    new_data = dataset.groupby(['dt', 'City', 'Country', 'Latitude', 'Longitude']).agg(
        AverageTemperature=('AverageTemperature', 'mean'),
        AverageTemperatureUncertainty=('AverageTemperatureUncertainty', 'mean')).reset_index()

    new_data = new_data.sort_values(by=['City', 'dt'])

    return new_data


def get_temperatures_by_country(dataset):
    new_data = dataset.groupby(['dt', 'Country']).agg(
        AverageTemperature=('AverageTemperature', 'mean'),
        AverageTemperatureUncertainty=('AverageTemperatureUncertainty', 'mean')).reset_index()
    new_data = new_data.sort_values(by=['Country', 'dt'])
    return new_data


def get_temperatures_by_continent(dataset):
    Asia = ['India', 'Syria', 'Turkey', 'Iraq', 'Thailand', 'China', 'Bangladesh', 'Pakistan', 'Vietnam', 'Indonesia',
            'Saudi Arabia', 'Afghanistan', 'Philippines', 'Iran', 'Russia', 'Japan', 'Burma', 'South Korea',
            'Singapore', 'Taiwan']
    Europe = ['Germany', 'Ukraine', 'United Kingdom', 'Spain', 'France', 'Italy']
    America = ['Brazil', 'Colombia', 'United States', 'Peru', 'Mexico', 'Canada', 'Chile', 'Dominican Republic']
    Oceania = ['Australia']
    Africa = ['Côte D\'Ivoire', 'Ethiopia', 'Egypt', 'South Africa', 'Morocco', 'Senegal', 'Tanzania', 'Zimbabwe',
              'Nigeria', 'Congo (Democratic Republic Of The)', 'Angola', 'Somalia', 'Kenya', 'Sudan']

    renamed_country = dataset.replace(Asia, 'Asia').replace(Europe, 'Europe').replace(America, 'America').replace(
        Oceania, 'Oceania').replace(Africa, 'Africa')
    data_by_continent = renamed_country.groupby(['dt', 'Country']).agg(
        AverageTemperature=('AverageTemperature', 'mean'),
        AverageTemperatureUncertainty=('AverageTemperatureUncertainty', 'mean')).reset_index()
    data_by_continent = data_by_continent.sort_values(by=['Country', 'dt'])

    return data_by_continent


# We divide the latitude into 3 groups :
# - Equator = city with latitude contained between 30°N and 30°S
# - Sud = city with latitude between 30°S and Pole Sud (90°S)
# - North = city with latitude between 30°N and Pole Nord (90°N)
def get_temperatures_by_latitude(dataset):
    data = dataset.copy()
    Equator_regex = '^[0-2](.)*\.(.)*|^[0-9]\.(.)*'
    North_regex = '[3-9](.)*N'
    South_regex = '[3-9](.)*S'
    data['Latitude'] = data['Latitude'].replace(Equator_regex, 'Equator', regex=True).replace(
        North_regex, 'North', regex=True).replace(South_regex, 'South', regex=True)
    data_by_lat = data.groupby(['Latitude', 'dt']).agg(
        AverageTemperature=('AverageTemperature', 'mean'),
        AverageTemperatureUncertainty=('AverageTemperatureUncertainty', 'mean')).reset_index()
    data_by_lat = data_by_lat.sort_values(by=['Latitude', 'dt'])

    return data_by_lat


def get_world_temperature(dataset):
    return dataset.groupby(['dt']).agg(
        AverageTemperature=('AverageTemperature', 'mean'),
        AverageTemperatureUncertainty=('AverageTemperatureUncertainty', 'mean')).reset_index()


def get_temperatures_of(dataset, names, column):
    values = {}
    for i in range(len(names)):
        mask = dataset[column] == names[i]
        values[names[i]] = dataset[mask]

    return values


def plot_temp_evolution_of_city(dataset, city_name):
    res = get_temperatures_of(dataset, city_name, 'City')
    return generic_plot_temp_evolution(res, city_name)


def plot_temp_evolution_of_country(dataset, country_name):
    countries_data = get_temperatures_by_country(dataset)
    res = get_temperatures_of(countries_data, country_name, 'Country')
    return generic_plot_temp_evolution(res, country_name)


def plot_temp_evolution_of_continent(dataset, continent_name):
    continent_data = get_temperatures_by_continent(dataset)
    res = get_temperatures_of(continent_data, continent_name, 'Country')
    generic_plot_temp_evolution(res, continent_name)


def plot_temp_evolution_of_all_continent(dataset):
    continent_data = get_temperatures_by_continent(dataset)
    continents = ['Asia', 'Europe', 'America', 'Oceania', 'Africa']
    res = get_temperatures_of(continent_data, continents, 'Country')
    generic_plot_temp_evolution(res, continents, 'continents')


def plot_temp_evolution_by_latitude(dataset):
    latitude_data = get_temperatures_by_latitude(dataset)
    latitudes = ['North', 'Equator', 'South']
    res = get_temperatures_of(latitude_data, latitudes, 'Latitude')
    generic_plot_temp_evolution(res, latitudes, 'latitudes')


def plot_world_temp_evolution(dataset):
    res = {}
    res['world'] = get_world_temperature(dataset)
    return generic_plot_temp_evolution(res, ['world'])


def generic_plot_temp_evolution(dataset, names, subject=''):
    years_list = []
    y_list = []
    error_list = []
    for i in range(len(names)):
        name = names[i]
        years = dataset[name]['dt']
        years_list.append(years)
        years_list.append(years)
        temp = dataset[name]['AverageTemperature']
        rolled_data = dataset[name].AverageTemperature.rolling(15).mean()
        y_list.append(temp)
        y_list.append(rolled_data)
        uncertainty = dataset[name]['AverageTemperatureUncertainty']
        error_list.append(uncertainty)
        error_list.append(uncertainty)
    if len(names) == 1:
        return plot_data(years_list, y_list, 'Average Temperature Evolution of ' + names[0], 'Years',
                  'Average Temperature', ['real data', 'smoothed data'], error_list)
    else:
        labels_list = []
        for i in range(len(names)):
            labels_list.append(names[i] + '(real data)')
            labels_list.append(names[i] + '(smoothed data)')
        return plot_data(years_list, y_list, 'Average Temperature Evolution of ' + subject, 'Years',
                  'Average Temperature', labels_list, error_list)


def plot_data(x_list, y_list, title, x_label, y_label, y_list_labels, uncertainty_list):
    fig = plt.figure(figsize=(20, 16))
    plt.title(title)
    for i in range(len(y_list)):
        plt.errorbar(x_list[i], y_list[i], uncertainty_list[i], label=y_list_labels[i])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()
    return fig


def find_most_affected_cities(dataset):
    delta_values = []
    city_list = dataset.City.unique()
    for i in range(len(city_list)):
        mask = dataset['City'] == city_list[i]
        res = dataset[mask]
        delta = res.AverageTemperature.max() - res.AverageTemperature.min()
        delta_values.append(delta)
    delta_data = pd.DataFrame({'City': city_list, 'Delta': delta_values}).sort_values(by=['Delta'], ascending=False)
    print('\n # Most affected cities :\n', delta_data.head())
    print('\n # Less affected cities :\n', delta_data.tail().sort_values(by='Delta'))
    return delta_data


def find_most_affected_countries(dataset):
    country_data = get_temperatures_by_country(dataset)
    delta_values = []
    country_list = country_data.Country.unique()
    for i in range(len(country_list)):
        mask = country_data['Country'] == country_list[i]
        res = country_data[mask]
        delta = res.AverageTemperature.max() - res.AverageTemperature.min()
        delta_values.append(delta)
    delta_data = pd.DataFrame({'Country': country_list, 'Delta': delta_values}).sort_values(by=['Delta'],
                                                                                            ascending=False)
    print('\n # Most affected countries :\n', delta_data.head())
    print('\n # Less affected countries :\n', delta_data.tail().sort_values(by='Delta'))
    return delta_data


def show_info_of(dataset):
    print('\n ## Info of the dataset:')
    dataset.info()
    print('\n ## Description of the dataset :')
    print(dataset.describe())
    print('\n ## Example values of the dataset :')
    print('5 first lines :')
    print(dataset.head(5))
    print('\n5 last lines :')
    print(dataset.tail(5))


def main_python():
    # Opening dataset
    data = pd.read_csv('./datasets/GlobalLandTemperaturesByMajorCity.csv')
    print('#####################"')
    print('Following dataset has been opened : GlobalLandTemperaturesByMajorCity.csv \n')

    print('#####################')
    print('Here are some useful info about the dataset :')
    show_info_of(data)

    print('\n#####################')
    print('Let\'s explore the values of the dataset :')
    data = explore_data(data)

    rectify_null_values(data)

    print("#####################")
    print("Find the most and less affected cities and countries of our data by the evolution of the temperatures :")
    find_most_affected_cities(data)
    find_most_affected_countries(data)

    print("####################")
    print("We can plot some evolution of the average temperature :\n")
    print("here are the available city : \n", data.City.unique())
    city = input("\n Please, enter a city that you want to see his plot temperature :")
    fig = plot_temp_evolution_of_city(data, [city])

    print("\nHere are the available country : \n", data.Country.unique())
    country = input("\nPlease, enter a country that you want to see his plot temperature :")
    fig = plot_temp_evolution_of_country(data, [country])

    print("\nHere are the available continent : Asia, Africa, Europe, America, Oceania")
    continent = input("Please, enter a continent that you want to see his plot temperature :")
    plot_temp_evolution_of_continent(data, [continent])

    choice = 1
    while choice != 0:
        print("\nWhat do you like to see now :")
        print(' - 1: Evolution of average temperature of all the continent')
        print(' - 2: Evolution of average temperature depending on the latitude')
        print(' - 3: Evolution of the world average temperature depending on the latitude')
        print(' - 0: Nothing')
        choice = int(input('\ntype here what you would like : '))

        if choice == 1:
            plot_temp_evolution_of_all_continent(data)
        elif choice == 2:
            plot_temp_evolution_by_latitude(data)
        elif choice == 3:
            plot_world_temp_evolution(data)
        elif choice != 0:
            print('type 0 to exit')


def main_streamlit():
    # Streamlit
    app_mode = st.sidebar.selectbox('Select Page',['Exploration','Plot'])
    data = pd.read_csv('./datasets/GlobalLandTemperaturesByMajorCity.csv')

    if app_mode=='Exploration':
        st.title("Axel Meloni (Erasmus student) - Programming project 2022-2023")
        st.write("I used the following dataset for the project : "
                 "https://www.kaggle.com/datasets/thedevastator/global-land-and-surface-temperature-trends-analy?select=GlobalTemperatures.csv \n"
                 "\nThe dataset shows the evolution of average temperature over the years from different cities in the world."
                 " I explored the data to show some interesting aspects and draw differents plots.")
        st.header("Exploration and Cleaning")
        st.write("I did a basic exploration of the dataset, I showed some useful data to know :")

        st.caption("the interval of time of the data")
        st.write('The dates go from', data.dt.min(), 'to', data.dt.max())
        st.caption('The list of cities')
        st.code(data.City.unique())
        st.caption('The list of countries')
        st.code(data.Country.unique())

        st.write(
            'the dates were string that I convert into datetime type and I grouped the data by years as the data for each month are too precise for the range of our time (~300years)'
            '\n\nDuring the exploration I could find that some AverageTemperature and AverageTemperatureUncertainty values were null.'
            'To clean them I decided to fill the null value with the value of the previous year as it shouldn\'t be a huge difference between two consecutive years.'
            '\n\nFrom the exploration I could compute the delta of the temperature for each city and each country and thus find the cities and countries the most and less affected by the average temperature evolution')

        delta_cities = find_most_affected_cities(data)
        delta_country = find_most_affected_countries(data)

        st.caption('Most affected cities')
        st.write(delta_cities.head())
        st.caption('Most affected countries')
        st.write(delta_country.head())

    if app_mode == 'Plot':
        st.write('I draw some plots to show the evolution of the temperatures.')
        st.write("The plots render better in the python script and are way faster to display,"
                 " so I just plot here in streamlit the plots for one countries and for the whole world"
                 "\n\nThe others are available launching the python script")
        city = st.selectbox("Choose a city",data.City.unique())
        st.caption(f'Evolution of average temperature of {city}')
        fig = plot_temp_evolution_of_city(data, [city])
        st.pyplot(fig)

        st.caption('Evolution of the world average temperature')
        fig = plot_world_temp_evolution(data)
        st.pyplot(fig)


# Please Comment The mehod you don't want to use
if __name__ == '__main__':
    # main_streamlit()
    main_python()

