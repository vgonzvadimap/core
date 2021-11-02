from typing import Any, List, Tuple
import os
import boto3
import requests
from requests_aws4auth import AWS4Auth

"""
This file comes from amplify/lambda-shared-code.

If anything needs to be updated, it needs to be there and then
pushed in the various functions using update_lambdas.py

We use this method in order to be able to test locally our
lambda functions (in opposite to using layers which can't
be tested locally)

Make sure that your lambda function Pipfile has
boto3, requests, requests_aws4auth 
in the [packages] section.
After making sure of this ^ you have to -> amplify build funciton <nameOfTheFunction>

NOTE: In order for mutations and queries to work, you must
add the proper privacy policies at the API level 
 @auth(rules: [{allow: private, provider: iam}])

"""
# IMPORTANT: Example queries - check API for details
# query = """
#     query {
#         listProjects {
#             items {
#                 id
#                 owner
#                 }
#         }
#     }
# """
# get_project = """
#     query GetProject($id: ID!){
#         getProject(id: $id){
#             id
#             owner
#         }
#     }
# """
# params = dict(id='3')
# create_equipment = """
#     mutation CreateSurveyCompletion ($input: CreateSurveyCompletionInput!) {
#     createSurveyCompletion(input: $input) {
#         version
#         id
#     }
# }
# """
#params = dict(id=3)

Param = dict
Arguments = List[Param]


def param(type: str, required: bool, unit: str = '', nested_dict=None) -> Param:
    return dict(type=type, required=required, unit=unit, nested_dict=nested_dict)


def validate_object(obj: dict, expected_format: dict) -> dict:
    def validate_type(key: str, value: Any, expected_type: str) -> Any:
        type_lut: dict = dict(
            bool=bool,
            str=str,
            int=int,
            float=float
        )
        def type_isnt_supported(t): return t not in type_lut
        def type_is_valid(val, t): return type(val) == type_lut.get(t)
        def type_is_numerical(val, t): return t == 'float' and type(val) == int
        if type_isnt_supported(expected_type):
            raise ValueError(
                f'Unsupported type {expected_type} for validation in key {key}')
        if not type_is_valid(value, expected_type):
            if type_is_numerical(value, expected_type):
                return type_lut.get(expected_type)(value)
            else:
                raise TypeError(
                    f'Invalid type {type(value)} expected {expected_type} for key {key}')
        return type_lut.get(expected_type)(value)

    validated_obj = dict()
    for key, params in expected_format.items():
        def required_key_is_missing(): return obj.get(
            key) is None and params.get('required')
        if required_key_is_missing():
            raise KeyError(f'Missing required key {key} in object.')
        if params.get('type') == 'dict':
            validated_obj[key] = validate_object(
                obj.get(key), params.get('nested_dict'))
        else:
            if params.get('required'):
                validated_obj[key] = validate_type(
                    key, obj.get(key), params.get('type'))
    # Add objects not in specs but in object as is
    validated_obj.update(
        {k: v for k, v in obj.items() if k not in expected_format}
    )
    return validated_obj


def format_error_response(error: str):
    response = dict(
        error=error
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': response
    }


def format_response(response: dict):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': response
    }


def get_environment_variables(env_vars_list: List) -> dict:
    return {env_var: os.environ[env_var] for env_var in env_vars_list}


def get_secret_variables(secret_vars_list: List) -> dict:
    client = boto3.client('ssm')
    secret_vars = dict()
    for secret_var in secret_vars_list:
        response = client.get_paramater(
            Name=os.environ[secret_var],
            WithDecryption=True
        )
        secret_vars[secret_var] = response.get('value')
    return secret_vars


def validate_arguments(event_arguments: dict, expected_arguments: Arguments) -> dict:
    # NOTE: If there is a nested dict with an unknown format, simply put an empty dict()
    # in param('dict', True, nested_dict=dict())
    return validate_object(event_arguments, expected_arguments)


class AppSyncInterface:
    def __init__(
        self,
        endpoint_env='API_FRONTENDSTATES_GRAPHQLAPIENDPOINTOUTPUT',
        region_env='REGION'
    ):
        def create_session(region: str):
            session = requests.Session()
            credentials = boto3.session.Session().get_credentials()
            session.auth = AWS4Auth(
                credentials.access_key,
                credentials.secret_key,
                region,
                'appsync',
                session_token=credentials.token
            )
            return session

        env_vars = get_environment_variables([
            endpoint_env,
            region_env
        ])
        self.endpoint = env_vars.get(endpoint_env)
        self.region = env_vars.get(region_env)
        self.session = create_session(self.region)

    def query(self, query: str, params: dict = None):
        """
        Check the graphql API to build your queries.
        """
        body = dict(query=query)
        if params is not None:
            body['variables'] = params

        response = self.session.request(
            url=self.endpoint,
            method='POST',
            json=body
        )
        return response

    def mutation(self, mutation: str, params: dict):
        response = self.session.request(
            url=self.endpoint,
            method='POST',
            json={
                'query': mutation,
                'variables': {
                    'input': params
                }
            }
        )
        return response

    def create_task(self):
        pass

    def create_error(self):
        pass
