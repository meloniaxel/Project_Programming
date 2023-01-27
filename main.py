import pandas as pd


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

