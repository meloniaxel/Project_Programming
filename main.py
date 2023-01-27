import pandas as pd


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


def get_temperature_by_city(dataset, city):
    values = {}
    for i in range(len(city)):
        mask = dataset['City'] == city[i]
        values[city[i]] = dataset[mask]

    return values


def get_temperature_by_country(dataset, country):
    values = {}
    for i in range(len(country)):
        mask = dataset['Country'] == country[i]
        values[country[i]] = dataset[mask]

    return values

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

    tempByCity = get_temperature_by_city(data, ['Abidjan', 'Paris'])
    tempByCountry = get_temperature_by_country(data, ['United States'])
