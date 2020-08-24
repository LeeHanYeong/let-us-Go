# drf-yasg
BASIC_DESCRIPTION = """
base64로 인코딩된 **사용자ID/비밀번호** 쌍을 Header에 전달\n
HTTP Request의 Header `Authorization`에
`Basic <base64로 인코딩된 "username:password" 문자열>`값을 넣어 전송\n
**개발서버에서만 편의를 위해 제공(api.dev.letusgo.app)**

```
Authorization: Basic ZGVmYXVsdF9jb21wYW55QGxoeS5rcjpkbGdrc2R1ZA==
```
"""

TOKEN_DESCRIPTION = """
### [DRF AuthToken](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
인증정보를 사용해 [AuthToken](#operation/auth_token_create) API에 요청, 결과로 돌아온 **key**를
HTTP Request의 Header `Authorization`에 `Token <key>`값을 넣어 전송

```
Authorization: Token fs8943eu342cf79d8933jkd
```
"""
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {
            "type": "HTTP Basic Auth (RFC 7617)",
            "description": BASIC_DESCRIPTION,
        },
        "Token": {"type": "DRF AuthToken", "description": TOKEN_DESCRIPTION},
    },
}
