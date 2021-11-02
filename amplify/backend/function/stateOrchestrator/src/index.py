import json
import requests
import boto3
import os
from requests_aws4auth import AWS4Auth

import lambda_utils as util
query = """
        query {
            listProjects {
                items {
                    id
                    owner
                    }
            }
        }
    """
get_project = """
    query GetProject($id: ID!){
        getProject(id: $id){
            id
            owner
        }
    }
"""

create_equipment = """
    mutation CreateSurveyCompletion ($input: CreateSurveyCompletionInput!) {
    createSurveyCompletion(input: $input) {
        version
        id
    }
}
"""
def handler(event, context):
    try:
        arguments = util.validate_arguments(
            event.get('arguments'), 
            dict(
                project_id=util.param('str', True)
            )
        )
    except Exception as e:
        return util.format_error_response(str(e))

    interface = util.AppSyncInterface()
    # response = interface.query(get_project, params=dict(id='3'))
    response = interface.mutation(
        create_equipment, dict(version='3'))
    return util.format_response(dict(
            code=response.status_code,
            txt=response.text
        ))