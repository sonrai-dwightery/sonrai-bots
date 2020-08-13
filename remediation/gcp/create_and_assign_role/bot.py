import logging
import re
import googleapiclient.errors


def run(ctx):
    data = {
            "resource_id": "the name of the identity ",
            "organization_id": "521402727133",
            "project_id": "development-test-245814",
            "role": {
                'roleId': "projects/development-test-245814/roles/CustomRole88",
                'role': {
                    'title': "Joshua Test Role",
                    'description': "",
                    'includedPermissions': [
                        "accessapproval.requests.dismiss",
                        "accessapproval.requests.get",
                        "accessapproval.requests.list",
                        "accessapproval.settings.delete"
                    ],
                    'stage': "Alpha"
                }
            }
        }

    service = ctx.get_client().get('iam', 'v1')

    ##### Creating the role #####
    # Does role exist
    try:
        # Yes other wise throw exception
        get_role(service=service, name=data.get('role').get('roleId'))

            # Is the role GCP defined (does not start with role/{role_id} then its custom managed)

                # Yes
                # Create a new role with the same name + sonraiManage

                # No
                # Patch role
    except googleapiclient.errors.HttpError as e:
        # No
        if e.resp.status == 404:
            # Create new role
            pass

    #### Assign role to identity ######
    # Get role name
    # Assign role to user


    
def create_role(service, name, project, title, description, permissions, stage):
    """Creates a role."""

    # pylint: disable=no-member
    role = service.projects().roles().create(
        parent='projects/' + project,
        body={
            'roleId': name,
            'role': {
                'title': title,
                'description': description,
                'includedPermissions': permissions,
                'stage': stage
            }
        }).execute()

    print('Created role: ' + role['name'])
    return role

def edit_role(service, name, project, title, description, permissions, stage):
    """Creates a role."""

    # pylint: disable=no-member
    role = service.projects().roles().patch(
        name='projects/' + project + '/roles/' + name,
        body={
            'title': title,
            'description': description,
            'includedPermissions': permissions,
            'stage': stage
        }).execute()

    print('Updated role: ' + role['name'])
    return role


def get_role(service, name):
    """Gets a role."""

    if re.search("^projects/[^/]+/roles/[^/]+$",name):
        return service.projects().roles().get(name=name).execute()

    elif re.search("^organizations/[^/]+/roles/[^/]+$", name):
        return service.organizations().roles().get(name=name).execute()

    elif re.search("^roles/[^/]+$", name):
        return service.roles().get(name=name).execute()

    else:
        return Exception('roleId: {} not excepted'.format(name))
