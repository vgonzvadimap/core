from lambda_utils import validate_arguments, validate_object, param
import unittest

class TestValidation(unittest.TestCase):
    # TODO: Figure out what can go wrong with the validationS
    # Write tests for validate_object and validate_arguments
    def test_validate_object(self):
        equipment_specs: dict = dict(
            solar_panel=dict(
                width=param('float', True, 'm'),
                length=param('float', True, 'm'),
                thickness=param('float', True, 'mm'),
                electrical_specs=param(
                    'dict',
                    True,
                    nested_dict=dict(
                        example=param('float', True),
                        voc_2=param('float', False)
                        )
                    )
                )
            )
        data = dict(
            width=3.1,
            length=0,
            thickness=22,
            electrical_specs=dict(
                example=0,
                bob='str'
            )
        )
        obj = validate_arguments(data, equipment_specs.get('solar_panel'))
        for k, v in data.items():
            self.assertIn(k, obj)

    def test_validate_arguments_pass():
        pass

if __name__ == '__main__':
    unittest.main()