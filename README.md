# let us:Go!

## API Update

- 190629
  - Token얻는 API변경 (`/rest-auth/login/` -> `/auth/token/`)
    - Token key값과 User정보를 함께 반환
- 190627
  - Track추가
    - Seminar List, Seminar Detail의 Reponse변경
  - Seminar의 속성 삭제, 추가
    - [삭제] sessionSet
    - [추가] trackSet
    - [삭제] entryFee -> Track으로 이동
  - Attend의 속성 삭제, 변경, 추가
    - [삭제] seminar
    - [추가] track
    - [변경] type -> discountType (할인 구분 [일반, 학생])
    - [추가] applicantType (지원자 구분 [일반, 스태프])
- 190626
  - UserAttribute AvailableCheck (회원가입시 속성가능여부(중복체크)) API추가



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

#### 1. 세미나 상세 받아오기 (Seminar Detail)

[API - Seminar Detail](https://letusgo.lhy.kr/doc/#operation/seminars_read) 에 GET요청(id에 0) 가장 최신의 세미나 정보 수신

#### 2. 회원가입 (User Create)

[API - User Create](https://letusgo.lhy.kr/doc/#operation/members_create) 에 POST요청, 유저 생성

#### 3. Token 받아오기 (rest-auth_login_create)

[API - Auth_AuthToken](https://letusgo.lhy.kr/doc/#operation/auth_token_create) 에 POST요청, Token과 User정보수신

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
