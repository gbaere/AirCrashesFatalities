from typing import Optional, Tuple
from plotly.figure_factory._county_choropleth import shapely


# it would be used like:
# lon_lat = valid_lonlat(lon, lat)
# if lon_lat is None:
#     raise ValueError("(lon, lat) is not in WGS84 bounds")
# else:
#     lon, lat = lon_lat
def valid_lonlat(lon: float, lat: float) -> Optional[Tuple[float, float]]:
    """
    This validates a lat and lon point can be located
    in the bounds of the WGS84 CRS, after wrapping the
    longitude value within [-180, 180)

    :param lon: a longitude value
    :param lat: a latitude value
    :return: (lon, lat) if valid, None otherwise
    """
    if not isinstance(lon, (int, float)) or not isinstance(lat, (int, float)):
        return None  # Retornar None para valores inválidos

    if lon < -180 or lon > 180 or lat < -90 or lat > 90:
        return None  # Retornar None para valores fora dos intervalos válidos

    # Put the longitude in the range of [0,360):
    lon %= 360
    # Put the longitude in the range of [-180,180):
    if lon >= 180:
        lon -= 360
    lon_lat_point = shapely.geometry.Point(lon, lat)
    lon_lat_bounds = shapely.geometry.Polygon.from_bounds(
        xmin=-180.0, ymin=-90.0, xmax=180.0, ymax=90.0
    )
    # return lon_lat_bounds.intersects(lon_lat_point)
    # would not provide any corrected values

    # ... (mesmo código)
    if lon_lat_bounds.intersects(lon_lat_point):
        return lon, lat  # Retorna a tupla (longitude, latitude)
    else:
        return None  # Retorna None se não for válido


def convert_value(value):
    if isinstance(value, str):
        return float(value.replace(',', ''))
    return value



def format_latitude(number_str):
    return number_str.replace('.', '')[:-2] + '.' + number_str[-2:]

def format_longitude(number_str):
    if number_str[0] == '-':
        return number_str[:4] + '.' + number_str[4:]
    else:
        return number_str[:3] + '.' + number_str[3:]


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



