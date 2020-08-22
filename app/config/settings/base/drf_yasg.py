# drf-yasg
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
        "Token": {"type": "DRF AuthToken", "description": TOKEN_DESCRIPTION,}
    }
}
