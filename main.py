import pandas as pd

if __name__ == '__main__':
    # Opening dataset
    data = pd.read_csv('./datasets/GlobalLandTemperaturesByMajorCity.csv')
    print(data)

