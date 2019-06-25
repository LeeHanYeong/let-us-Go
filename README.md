# let us:Go!

## API 설명

### Authentication

사용자 인증이 필요한 경우, Token인증을 사용합니다. Token인증에는 아래 라이브러리를 사용하고 있습니다.
[DRF Authentication - Token](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)



#### Token획득법

[API Docs - AuthToken](https://letusgo.lhy.kr/doc/#operation/rest-auth_login_create)
`/rest-auth/login/` URL에 아래와 같은 데이터를 `POST` 방식으로 전송

```json
{
	"username": "string",
	"email": "user@example.com",
	"password": "string"
}
```

성공시 Token문자열을 객체로 리턴

```json
{
  "key": "a129b636dc3f352f864398b471f17b43bb4ce352"
}
```



#### Token 사용법

```
Authorization: Token a129b636dc3f352f864398b471f17b43bb4ce352
```

위 key/value를 HTTP Request header로 지정해서 전송 (value의 token값 앞에 "Token "문자열이 존재해야 함)



### API 사용과정 설명

#### 1. 세미나 목록 받아오기 (Seminar List)

[API - Seminar List](https://letusgo.lhy.kr/doc/#operation/seminars_list) 에 GET요청, 세미나 목록 수신

#### 2. 회원가입 (User Create)

[API - User Create](https://letusgo.lhy.kr/doc/#operation/members_create) 에 POST요청, 유저 생성

#### 3. Token 받아오기 (rest-auth_login_create)

[API - rest-auth_login_create](https://letusgo.lhy.kr/doc/#operation/rest-auth_login_create) 에 POST요청, Token수신

#### 4. 인증(Authenticate)된 상태로 신청서 작성 (Attend Create)

수신한 Token을 Header에 등록 후, [API - Attend Create](https://letusgo.lhy.kr/doc/#operation/attends_create) 에 POST요청, Status code확인 (201)

#### 5. 인증(Authenticate)된 상태로 신청서 목록 확인 (Attend List)

수신한 Token을 Header에 등록 후, [API - Attend List](https://letusgo.lhy.kr/doc/#operation/attends_list) 에 GET요청, 신청서 목록 확인







## Trouble shooting

### RDS Database생성시

template0으로부터, LC_COLLATE를 따로 설정 (한글 ordering관련)

```
CREATE DATABASE letusgo OWNER=lhy TEMPLATE template0 LC_COLLATE 'C';
```
