# let us:Go!

[![codecov](https://codecov.io/gh/LeeHanYeong/let-us-go/branch/develop/graph/badge.svg)](https://codecov.io/gh/LeeHanYeong/let-us-go)

## Requirements

**Production**

- Docker
- docker-compose

**Development**

- Python >= 3.8
- Poetry
- pre-commit
- black

> **Poetry, pre-commit, black은 brew를 사용해 설치**
> brew install poetry pre-commit black



## Installation

### Let's Encrypt

#### 인증서 생성

```shell
sh .scripts/ssl_cert.sh
```

#### 인증서 갱신

```shell
sh .scripts/ssl_renew.sh
```



## Run & Update

```shell
sh run.sh
```

- 소스 업데이트 (git pull)
- ssl_renew.sh를 Cronjob에 등록 (Monthly)
- docker-compose build, restart



## Test

```shell
pytest --cov app
```



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





## Other settings

### AWS EC2(Ubuntu 20.04)

```shell
# docker
sudo apt -y update
sudo apt -y dist-upgrade
sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt -y update
sudo apt -y install docker-ce docker-ce-cli containerd.io

# docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


# 점검 도구
sudo apt -y install net-tools

# zsh
sudo apt -y install zsh
echo n | sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sudo chsh -s $(which zsh) $(whoami)
```





## Trouble shooting

### RDS Database생성시

template0으로부터, LC_COLLATE를 따로 설정 (한글 ordering관련)

```
CREATE DATABASE letusgo OWNER=lhy TEMPLATE template0 LC_COLLATE 'C';
```
