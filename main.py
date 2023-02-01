import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Rectify the null values by taking the value of the previous row
# it should be coherent as the average temperature of 1 month shouldn't be very different from the previous one
# but if several null value are on consecutive rows it won't so accurate
# because all months will be at the same temperature
def rectify_null_values(dataset):
    # We can see that AverageTemperature and AverageTemperatureUncertainty contain null values
    dataset.info()

    # We extract the first line containing null AverageTemperature
    # and the line before without null value on AverageTemperature
    null_values_temp = dataset['AverageTemperature'].isnull()
    null_rows_temp = dataset[null_values_temp]
    first_null_temp = null_rows_temp.head(1)
    previous_index_temp = dataset['dt'] == first_null_temp['dt'].values[0] - 1
    previous_index_city = dataset['City'] == first_null_temp['City'].values[0]
    previous_row_temp = dataset[previous_index_temp & previous_index_city]
    print(previous_row_temp.T)
    print(first_null_temp.T)

    # same with AverageTemperatureUncertainty
    # note : the lines are actually the same as those picked for the AverageTemperature
    null_values_uncertainty = dataset['AverageTemperatureUncertainty'].isnull()
    null_rows_uncertainty = dataset[null_values_uncertainty]
    first_null_uncertainty = null_rows_uncertainty.head(1)
    previous_index_uncertainty = dataset['dt'] == first_null_uncertainty['dt'].values[0] - 1
    previous_index_city = dataset['City'] == first_null_uncertainty['City'].values[0]
    previous_row_uncertainty = dataset[previous_index_uncertainty & previous_index_city]
    print(previous_row_uncertainty.T)
    print(first_null_uncertainty.T)

    # rectify null values (!data must be sorted by city and date!)
    dataset['AverageTemperature'].fillna(method='ffill', inplace=True)
    dataset['AverageTemperatureUncertainty'].fillna(method='ffill', inplace=True)

    # check that the value are correctly rectified
    dataset.info()
    print(dataset[previous_index_temp & previous_index_city].T)
    print(dataset[null_values_temp].head(1).T)


def explore_data(dataset):
    print("The dates go from", dataset.dt.min(), 'to', dataset.dt.max())
    print(" Here is the list of the cities of the dataset :\n", dataset.City.unique())
    print(" Here is the list of the countries of the dataset :\n", dataset.Country.unique())

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
        North_regex, 'North',regex=True).replace(South_regex, 'South', regex=True)
    data_by_lat = data.groupby(['Latitude', 'dt']).agg(
        AverageTemperature=('AverageTemperature', 'mean'),
        AverageTemperatureUncertainty=('AverageTemperatureUncertainty', 'mean')).reset_index()
    data_by_lat = data_by_lat.sort_values(by=['Latitude', 'dt'])

    return data_by_lat


def get_world_temperature(dataset):
    return data.groupby(['dt']).agg(
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
    generic_plot_temp_evolution(res, city_name)


def plot_temp_evolution_of_country(dataset, country_name):
    countries_data = get_temperatures_by_country(dataset)
    res = get_temperatures_of(countries_data, country_name, 'Country')
    generic_plot_temp_evolution(res, country_name)


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
    generic_plot_temp_evolution(res, ['world'])


def generic_plot_temp_evolution(dataset, names, subject=''):
    years_list = []
    y_list = []
    for i in range(len(names)):
        name = names[i]
        years = dataset[name]['dt']
        years_list.append(years)
        years_list.append(years)
        temp = dataset[name]['AverageTemperature']
        rolled_data = dataset[name].AverageTemperature.rolling(15).mean()
        y_list.append(temp)
        y_list.append(rolled_data)
    if len(names) == 1:
        plot_data(years_list, y_list, 'Average Temperature Evolution of ' + names[0], 'Years',
                  'Average Temperature', ['real data', 'smoothed data'])
    else:
        labels_list = []
        for i in range(len(names)):
            labels_list.append(names[i] + '(real data)')
            labels_list.append(names[i] + '(smoothed data)')
        plot_data(years_list, y_list, 'Average Temperature Evolution of ' + subject, 'Years',
                  'Average Temperature', labels_list)


def plot_data(x_list, y_list, title, x_label, y_label, y_list_labels):
    plt.figure(figsize=(20, 16))
    plt.title(title)
    for i in range(len(y_list)):
        plt.plot(x_list[i], y_list[i], label=y_list_labels[i])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()


def show_info_of(dataset):
    print('Info :')
    dataset.info()
    print('Describe :')
    print(dataset.describe())
    print('5 first lines :')
    print(dataset.head(5))
    print('5 last lines :')
    print(dataset.tail(5))


if __name__ == '__main__':
    # Opening dataset
    data = pd.read_csv('./datasets/GlobalLandTemperaturesByMajorCity.csv')
    print('Dataset opened : \n', data)

    show_info_of(data)

    data = explore_data(data)

    rectify_null_values(data)

    tempByCity = get_temperatures_of(data, ['Abidjan', 'Paris'], 'City')
    tempByCountry = get_temperatures_by_country(data)
    tempByContinent = get_temperatures_by_continent(data)
    tempByLatitude = get_temperatures_by_latitude(data)

    # plot_temp_evolution_of_city(data, ['Abidjan'])
    # plot_temp_evolution_of_country(data, ['United States'])
    # plot_temp_evolution_of_continent(data, ['Europe'])
    # plot_temp_evolution_of_all_continent(data)
    # plot_temp_evolution_by_latitude(data)

    get_world_temperature(data)
    plot_world_temp_evolution(data)
