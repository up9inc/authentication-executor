import base64

valid_custom_code_1 = b"def custom_auth() -> AuthenticationPayload:\n" \
                      b"\tprint('debugTest')\n" \
                      b"\tresp = requests.get('http://google.com')\n" \
                      b"\treturn AuthenticationPayload(headers={'Auth':'1'})"

code2 = b"def custom_auth() -> AuthenticationPayload:\n" \
        b"\tresp = requests.get('http://google.com')\n" \
        b"\treturn AuthenticationPayload(headers={'Auth':'2'})"

code3 = b"def custom_auth() -> AuthenticationPayload:\n" \
        b"\ttarget.additional_headers()"

code4 = b"def koko():"

configs_1 = {
    "XXX_ZZZ": {
        "type": "customCode",
        "spec": {
            "customCode": base64.b64encode(valid_custom_code_1).decode()
        }
    }
}

configs = {
    "XXX_ZZZ": {
        # valid_custom_code_spec_1,
            "type": "customCode",
            "spec": {
                "customCode": base64.b64encode(code2).decode()
            }
    },
    "REQUEST": {
        "type": "request",
        "spec": {
            "url": "http://google.com/token"
        }
    },
    "AUTH_HELPER": {
        "type": "authHelper",
        "spec": {
            "formURL": "https://shahar-dev.dev.testr.io",
            "username": "user1@up9.com",
            "password": "user1",
            "headers": {
                "authorization": {}
            },
            "additionalUrls": [
            ],
            "endpoints": [
                {
                    "method": "get",
                    "service": "https://shahar-dev.dev.testr.io",
                    "target": "TARGET_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/",
                    "regexPath": {},
                    "regex": "^/$",
                    "originalUrl": "shahar-dev.dev.testr.io/",
                    "headers": {}
                },
                {
                    "method": "get",
                    "service": "https://auth.shahar-dev.dev.testr.io",
                    "target": "TARGET_AUTH_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/auth/realms/testr/protocol/openid-connect/login-status-iframe.html",
                    "regexPath": {},
                    "regex": "^/auth/realms/testr/protocol/openid-connect/login-status-iframe.html$",
                    "originalUrl": "auth.shahar-dev.dev.testr.io/auth/realms/testr/protocol/openid-connect/login-status-iframe.html",
                    "headers": {}
                },
                {
                    "method": "get",
                    "service": "https://shahar-dev.dev.testr.io",
                    "target": "TARGET_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/silent-check-sso.html",
                    "regexPath": {},
                    "regex": "^/silent-check-sso.html$",
                    "originalUrl": "shahar-dev.dev.testr.io/silent-check-sso.html",
                    "headers": {}
                },
                {
                    "method": "post",
                    "service": "https://auth.shahar-dev.dev.testr.io",
                    "target": "TARGET_AUTH_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/auth/realms/testr/protocol/openid-connect/token",
                    "regexPath": {},
                    "regex": "^/auth/realms/testr/protocol/openid-connect/token$",
                    "originalUrl": "auth.shahar-dev.dev.testr.io/auth/realms/testr/protocol/openid-connect/token",
                    "headers": {}
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/",
                    "regexPath": {},
                    "regex": "^/models/$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/",
                    "headers": {
                        "authorization": {
                            "idx": 0
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://shahar-dev.dev.testr.io",
                    "target": "TARGET_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/app/profile",
                    "regexPath": {},
                    "regex": "^/app/profile$",
                    "originalUrl": "shahar-dev.dev.testr.io/app/profile",
                    "headers": {}
                },
                {
                    "method": "get",
                    "service": "https://auth.shahar-dev.dev.testr.io",
                    "target": "TARGET_AUTH_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/auth/realms/testr/invite-link/getInviteLink",
                    "regexPath": {},
                    "regex": "^/auth/realms/testr/invite-link/getInviteLink$",
                    "originalUrl": "auth.shahar-dev.dev.testr.io/auth/realms/testr/invite-link/getInviteLink",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "post",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/admin/apiKey",
                    "regexPath": {},
                    "regex": "^/admin/apiKey$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/admin/apiKey",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/status",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/status$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/status",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/lastResults/{name}",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/lastResults/[^/]+$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/lastResults/all",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/suites/",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/suites/$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/suites/",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/lastResults/{name}/swagger",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/lastResults/[^/]+/swagger$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/lastResults/all/swagger",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/lastResults/{name}/dataDependency",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/lastResults/[^/]+/dataDependency$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/lastResults/all/dataDependency",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/lastResults/{name}/dataDependency/span",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/lastResults/[^/]+/dataDependency/span$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/lastResults/all/dataDependency/span",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/agents/",
                    "regexPath": {},
                    "regex": "^/agents/$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/agents/",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/suites/{name}",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/suites/[^/]+$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/suites/all",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/suites/{name}/targets",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/suites/[^/]+/targets$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/suites/all/targets",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/suites/{name}/runs",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/suites/[^/]+/runs$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/suites/all/runs",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/suites/{name}/agents/{agentId}/profiles",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/suites/[^/]+/agents/[^/]+/profiles$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/suites/all/agents/0509162f71bf420999ff2d2b9e394fd6/profiles",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "get",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/suites/{name}/tests",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/suites/[^/]+/tests$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/suites/all/tests",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                },
                {
                    "method": "post",
                    "service": "https://trcc.shahar-dev.dev.testr.io",
                    "target": "TARGET_TRCC_SHAHAR_DEV_DEV_TESTR_IO",
                    "path": "/models/{modelId}/suites/{name}",
                    "regexPath": {},
                    "regex": "^/models/[^/]+/suites/[^/]+$",
                    "originalUrl": "trcc.shahar-dev.dev.testr.io/models/my_model/suites/all",
                    "headers": {
                        "authorization": {
                            "idx": 1
                        }
                    }
                }
            ]
        }
    }
}
