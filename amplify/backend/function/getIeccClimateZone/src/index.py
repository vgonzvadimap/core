from eeweather import rank_stations
import lambda_utils as util


def get_iecc_climate_zone(lat, lon, kg_zone):
    def get_iecc_climate_zone_from_kg(kg):
        koppenGeiger_to_IECC_dict = {
            'Cfa': '4A', 'Dfc': '6B', 'Cfc': '7A', 'ET': '7A', 'Dsc': '6B', 'Cfb': '4A', 'Dfb': '6A', 'Dwc': '7A', 'BSk': '5B', 'Csb': '5B',
            'Csa': '3B', 'BSh': '3B', 'BWh': '3B', 'BWk': '3B', 'Dsb': '5B', 'Dfa': '5A', 'Am': '1A', 'Aw': '2A', 'Af': '1A', 'As': '1A', 'Dwb': '6A', 'Dwa': '6A'}
        if kg not in koppenGeiger_to_IECC_dict:
            raise ValueError(
                f'Cannot find any IECC or KG correspondance for coordinates {lat};{lon}')
        else:
            doe_climate_zone = koppenGeiger_to_IECC_dict[kg]
            return doe_climate_zone

    stations_results = rank_stations(
        lat, lon, match_iecc_climate_zone=True, match_iecc_moisture_regime=True)
    nearest_result = stations_results[:1]
    climate_zone = nearest_result.iecc_climate_zone[0]
    moisture_regime = nearest_result.iecc_moisture_regime[0]

    if climate_zone is None or moisture_regime is None:
        try:
            doe_climate_zone = get_iecc_climate_zone_from_kg(kg_zone)
        except ValueError as e:
            return dict(error=str(e))
    else:
        doe_climate_zone = climate_zone + '' + moisture_regime

    return dict(iecc_zone=doe_climate_zone)


def handler(event, context):
    try:
        arguments = util.validate_arguments(
            event.get('arguments'),
            dict(
                lat=util.param('float', True),
                lon=util.param('float', True),
                kg_zone=util.param('str', True)
            )
        )
    except Exception as e:
        return util.format_error_response(str(e))

    # for tests -> lat: 37.33577030970146, lon: -121.89056396484375, kg_zone: Csb
    lat = arguments.get('lat')
    lon = arguments.get('lon')
    kg_zone = arguments.get('kg_zone')

    iecc_climate_zone = get_iecc_climate_zone(
        lat, lon, kg_zone).get('iecc_zone')

    return util.format_response(iecc_climate_zone)
