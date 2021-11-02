import json
from lambda_utils import param

# think about set
enums = dict(
    spec_types=['BatterySpecs', 'ControllerSpecs', 'EVChargerSpecs', 'HybridInverterSpecs',
                'InverterSpecs', 'InverterChargerSpecs', 'MPPTSpecs', 'RapidShutdownSpecs', 'SolarPanelSpecs'],
    chemistry_compatibilities=[
        'Lithium_Ion', 'Lithium_Ion_FLP', 'Lead_Acid_ADM', 'Lead_Acid_Gel'],
    applications=['V2B', 'Dumb_charge',
                  'Smart_charge', 'Heila_compatible'],
    voltage_connections=['MONO_120_240V_split_phase', 'MONO_120V', 'MONO_240V', 'TRI_120_208V', 'TRI_347_600V',
                         'TRI_240V', 'TRI_480V', 'TRI_277_480V', 'TRI_600V', 'TRI_400V', 'TRI_127_220V', 'TRI_440V'],
    frequency=['Hz_50', 'Hz_60']
)


# def type_lookup(t):
def optional_string(value):
    if type(value) is None:
        return None
    elif type(value) == str:
        return value
    else:
        raise TypeError(f'{value} is not a string. String is expected')


def string(value):
    if type(value) == str:
        return value
    else:
        raise TypeError(f'Expected string for value {value}')


def optional_integer(value):
    if type(value) is None:
        return None
    elif type(value) == int:
        return value
    else:
        raise TypeError(f'{value} is not an integer. Integer is expected')


def integer(value):
    if type(value) == int:
        return value
    else:
        raise TypeError(f'Expected integer for value {value}')


def optional_floating(value):
    if type(value) is None:
        return None
    elif type(value) == float or type(value) == int:
        return value
    else:
        raise TypeError(f'{value} is not a float. Float is expected')


def floating(value):
    if type(value) == float or type(value) == int:
        return value
    else:
        raise TypeError(f'Expected integer for value {value}')


def optional_boolean(value):
    if type(value) is None:
        return None
    elif type(value) == bool:
        return value
    else:
        raise TypeError(f'{value} is not a boolean. Boolean is expected')


def boolean(value):
    if type(value) == bool:
        return value
    else:
        raise TypeError(f'Expected boolean for value {value}')


def check_if_optional(value_type, value_key):
    if 'opt' not in value_type:
        raise KeyError(
            f'{value_key} is not in your dict')


def enum_verify(enum_list):
    if type(enum_list) == list:
        if len(enum_list) != 0:
            return enum_list
        else:
            raise TypeError(f'Expected arguments for list {enum_list}')
    else:
        raise TypeError(f'Expected list for value {enum_list}')


specs_lookup_table: dict = dict(
    BatterySpecs=dict(
        lifetime=param(
            'dict',
            True,
            nested_dict=dict(
                lifetime_cycle=param('int', True, 'year'),
                lifetime_calendar=param('int', True),
                lifetime_cycle_dod=param('float', True)
            )
        ),
        chemestry=param(
            'dict',
            True,
            nested_dict=dict(
                bess_chemestry_compatibility=param(
                    enums['chemistry_compatibilities'], True)
            )
        ),
        electrical_specs=param(
            'dict',
            True,
            nested_dict=dict(
                efficiency=param(
                    'dict',
                    True,
                    nested_dict=dict(
                        mean_efficiency=param('float', True)
                    )
                ),
                current=param(
                    'dict',
                    True,
                    nested_dict=dict(
                        max_charge=param('float', True),
                        nominal_charge=param('float', True),
                        max_discharge=param('float', True),
                        nominal_discharge=param('float', True)
                    )
                ),
                voltage=param(
                    'dict',
                    True,
                    nested_dict=dict(
                        max_voltage=param('float', True, 'V'),
                        min_voltage=param('float', True, 'V'),
                        nominal_voltage=param('float', True, 'V')
                    )
                ),
                voltage=param(
                    'dict',
                    True,
                    nested_dict=dict(
                        max_voltage=param('float', True, 'V'),
                        min_voltage=param('float', True, 'V'),
                        nominal_voltage=param('float', True, 'V')
                    )
                ),
                capacity=param(
                    'dict',
                    True,
                    nested_dict=dict(
                        rated_Ah=param('float', True, 'V'),
                        rated_kWh=param('float', True, 'V')
                    )
                )
            )
        )
    ),
    ControllerSpecs=None,
    EVChargerSpecs=dict(
        lifetime=param(
            'dict',
            True,
            nested_dict=dict(
                warranty=param('int', True, 'year'),
            )
        ),
        lifetime=param(
            'dict',
            True,
            nested_dict=dict(
                lifetime_cycle=param('int', True, 'year'),
                lifetime_calendar=param('int', True),
                lifetime_cycle_dod=param('float', True)
            )
        ),
    )
)


type_lut = dict(
    string=string,
    opt_string=optional_string,

    integer=integer,
    opt_integer=optional_integer,

    floating=floating,
    opt_floating=optional_floating,

    boolean=boolean,
    opt_boolean=optional_boolean
)


def type_check(current_specs, required_specs):
    for required_specs_key, required_specs_type in required_specs.items():
        if required_specs_key not in current_specs:
            check_if_optional(required_specs_type, required_specs_key)
        else:
            current_specs_value = current_specs.get(required_specs_key)
            for type_of_spec in type_lut:
                if type_of_spec == required_specs_type:
                    type_lut.get(type_of_spec)(current_specs_value)
            if type(required_specs_type) == list:
                enum_verify(current_specs_value)


def handler(event, context):
    method = event.get('arguments').get('method')

    if method == 'getSpecsFormat':
        return {
            'body': specs_lookup_table  # Returns all specs
        }

    elif method == 'verify':
        params = event.get('arguments').get('params').get('body')
        specs_name = list(params)[0]

        current_specs = params.get(specs_name)
        required_specs = specs_lookup_table.get(specs_name).get(specs_name)

        type_check(current_specs, required_specs)

        return {
            'body': params
        }

    return {
        # 'statusCode': 200,
        # 'headers': {
        #     'Access-Control-Allow-Headers': '*',
        #     'Access-Control-Allow-Origin': '*',
        #     'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        # },
        'body': specs_lookup_table.get(method)
    }


# class AbstractClass:
#     @abstractmethod
#     def __init__(self,):
#         self.required_arguments = None

#     def validate_parameters():
#         pass


# class HardwareValidator(AbstractClass):
#     def __init__(self)


# def handler(...):
#     hardware_validator = HardwareValidator()
#     hardware_validator.set_required_param(
#         []
#     )
