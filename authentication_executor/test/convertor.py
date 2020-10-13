import json

from authentication_executor.authenticators.auth_helper_authenticator import AuthHelperAuthenticator

with open("./auth_helper_output.json") as file:
    auth_helper_dict = json.loads(file.read())
    result = AuthHelperAuthenticator._convert_to_executor_format(auth_helper_dict)
    print(json.dumps(result, indent=3))
