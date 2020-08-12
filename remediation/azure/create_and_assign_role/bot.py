import uuid

from azure.mgmt.authorization import AuthorizationManagementClient


def run(ctx):

    data = {
        "resourceId": "3d56a405-344a-40c8-96ad-39e8c4fb30b5",
        "subcriptionId": "2731df3f-27cc-4548-8d8d-8bc4ca3f8429",
        "scope": "/subscriptions/{}/".format("2731df3f-27cc-4548-8d8d-8bc4ca3f8429"),
        "role_definition_id": "66c7753a-5c5a-4706-bd77-33ad55021b9a",
        "role_definition": {
            "properties": {
                "roleName": "Joshua test role name",
                "description": "",
                "assignableScopes": ["/subscriptions/{}/".format("2731df3f-27cc-4548-8d8d-8bc4ca3f8429")],
                "permissions": [
                    {
                        "actions": [],
                        "notActions": [],
                        "dataActions": [],
                        "notDataActions": []
                    }
                ]
            }
        }
    }

    # authorization_management_client = AuthorizationManagementClient(ctx.get_client().get(AuthorizationManagementClient))
    authorization_management_client = ctx.get_client().get(AuthorizationManagementClient)

    # Create Role
    results = authorization_management_client.role_definitions.create_or_update(scope=data.get("scope"), role_definition_id=data.get('role_definition_id'), role_definition=data.get('role_definition'))

    properties = {
        "properties": {
            "roleDefinitionId": results.id,
            "principalId": data.get('resourceId')
        }
    }

    # Assign Role
    authorization_management_client.role_assignments.create(scope=data.get('scope'), role_assignment_name=str(uuid.uuid4()), parameters=properties)
