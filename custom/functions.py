import pandas as pd

def load_and_process_data():
    dataset = pd.read_csv("dataset/air_crashes_clean.csv", sep=';', encoding="Latin-1")

    dataset['latitude_srt'] = dataset['Latitude'].astype(str)
    dataset['longitude_srt'] = dataset['Longitude'].astype(str)

    dataset['latitude_srt'] = dataset['latitude_srt'].apply(format_coordinates)
    dataset['longitude_srt'] = dataset['longitude_srt'].apply(format_coordinates)

    dataset['Latitude'] = dataset['latitude_srt']
    dataset['Longitude'] = dataset['longitude_srt']

    dataset = dataset.drop(['latitude_srt', 'longitude_srt'], axis=1)

    return dataset


def format_coordinates(coord_str):
    # Remove vírgulas e ponto final
    cleaned_str = coord_str.replace(',', '').replace('.', '')

    # Verifica se é um valor negativo
    is_negative = False
    if cleaned_str.startswith('-'):
        is_negative = True
        cleaned_str = cleaned_str[1:]

    # Insere o ponto na posição adequada (após os primeiros 2 caracteres)
    formatted_coord = cleaned_str[:2] + '.' + cleaned_str[2:]

    if is_negative:
        formatted_coord = '-' + formatted_coord

    return formatted_coord



