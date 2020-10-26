# Auth Executor

## General
A library for executing authentication flows. 

Features:
* Extensible - new authenticators can be added, as long as they conform to the `BaseAuthenticatorABC` interface
* A wrapped `requests` library which exposes a `to_har()` function
* Loosely coupled from the app (test runner, calibrator, standalone wizard etc.) and unaware of TRCC.

## Authenticators
### Custom Code
A python function which returns an authentication payload.

#### Example
```
def custom_auth() -> AuthenticationPayload: 
  resp = requests.post('https://auth-server.com/token', json={'secret': 'MY_SECRET'})
  token = resp.json()['access_code']

  # Any print() will be logged as debug data
  print('Received token: {token}')

  # Note: you must return a valid AuthenticationPayload object
  return AuthenticationPayload(headers={"Authorization": token})
```

#### Spec
```
{
    // Base 64 encoded custom code
    "customCode": "ZGVmIGN1c3RvbV9hdXRoKCkgLT4gQXV0aGVudGljYXRpb25QYXlsb2FkOiAKICByZXNwID0gcmVxdWVzdHMucG9zdCgnaHR0cHM6Ly9hdXRoLXNlcnZlci5jb20vdG9rZW4nLCBqc29uPXsnc2VjcmV0JzogJ01ZX1NFQ1JFVCd9KQogIHRva2VuID0gcmVzcC5qc29uKClbJ2FjY2Vzc19jb2RlJ10KCiAgIyBBbnkgcHJpbnQoKSB3aWxsIGJlIGxvZ2dlZCBhcyBkZWJ1ZyBkYXRhCiAgcHJpbnQoJ1JlY2VpdmVkIHRva2VuOiB7dG9rZW59JykKCiAgIyBOb3RlOiB5b3UgbXVzdCByZXR1cm4gYSB2YWxpZCBBdXRoZW50aWNhdGlvblBheWxvYWQgb2JqZWN0CiAgcmV0dXJuIEF1dGhlbnRpY2F0aW9uUGF5bG9hZChoZWFkZXJzPXsiQXV0aG9yaXphdGlvbiI6IHRva2VufSk="
}
```

### Basic Auth
#### Spec
```
{
    "username": "myUser",
    "password": "myPass"
}
```

### Browser-Based (Auth Helper)
#### Spec
See https://github.com/up9inc/authentication-helper/#request

> Note: If an auth helper configuration is provided to the library, 
it will convert the auth helper format to auth executor format, and ignore any other configurations that were provided. 

### Headers
#### Spec 
```
{
    "headers": [
        {
            "key": "Auth1",
            "value": "Bearer XYZ"
        },
        ...
    ]
}
```

## Assignments
Assignments are a mapping between auth configurations and entities (services and endpoints).

## Configuration Example
The authentication property of an environment profile may look like this:
```
{
    "assignments" : {
        "payloadId" : "customCode1", // Will be applied to all endpoints
        "services": {
            "TARGET_MY_TARGET": {
                "payloadId": "myTargetConfig1",
                "endpoints": [
                    {
                        "method": "get",
                        "path": "/myPath2",
                        "payloadId": "myEpConfig1"
                    }
                ]
            }
        }
    },
    "configurations" : {
        "customCode1" : {
            "type" : "customCode",
            "spec" : {
                // See custom code spec
            }
        },
        "myEpConfig1" : {
            "type" : "basicAuth",
            "spec" : {
                "username": "strongUser",
                "password": "strongPass"
            }
        },
        "myTargetConfig1" : {
            "type" : "basicAuth",
            "spec" : {
                "username": "weakUser",
                "password": "weakPass"
            }
        }
    }
}
```

## Output
The execution has two outputs:
* An auth execution status (har, payload, used config) via the `ApiClientABC`
* JSON format that's compatible with up9lib (modeler-generated tests)

## Limitations & TODOs
* Think if there's need for auth payload in a form different from headers (body, for example)
* Add support for generic http request
* Add support for oauth2, okta, auth0 etc
* HAR format is partial, see TODOs in `RequestWrapper`
* Auth Execution Id is created by the executor itself when it starts (via an interface). 
It'd be better to refactor such that it would receive the id. 
This can be done with no changes to the library itself, only by providing a different implementation of the `ApiClientABC` interface 