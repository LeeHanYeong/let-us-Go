# let us: Go!

[![github-action]][github-workflow]
[![coverage]][codecov]
[![github-last-commit]][github]
[![made-with]][django]

iOS 세미나 **`let us: Go!`** 의 API서버 애플리케이션

>  API문서: https://api.dev.letusgo.app/doc

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

### .env파일 추가 (docker-compose의 env_file에서 사용)

```shell
AWS_SECRETS_MANAGER_ACCESS_KEY_ID=*****
AWS_SECRETS_MANAGER_SECRET_ACCESS_KEY=*****
AWS_ROUTE53_ACCESS_KEY_ID=*****
AWS_ROUTE53_SECRET_ACCESS_KEY=*****
CODECOV_TOKEN=*****
```



## Run

```shell
docker-compose up -d
```



## Scripts

### Let's Encrypt

#### 인증서 생성

```shell
sh .scripts/ssl_cert.sh
```

#### 인증서 갱신

```shell
sh .scripts/ssl_renew.sh
```



### Source update & restart

```shell
sh run.sh
```

- 소스 업데이트 (git pull)
- ssl_renew.sh를 Cronjob에 등록 (Monthly)
- docker-compose build, restart



## Test

```shell
# coverage기반 pytest실행
pytest --cov app
# codecov리포트 전송, CODECOV_TOKEN환경변수 필요
codecov
```



## Deployment

### EC2 초기설정

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



### EC2에 CI완료 후 run.sh실행을 위한 설정

>  GitHub Action ([AWS SSM Send-Command](https://github.com/marketplace/actions/aws-ssm-send-command)) 사용

#### GitHub Action에 비밀값 설정

- SSM FullAccess권한을 가진 Credential추가
  - AWS_SSM_ACCESS_KEY_ID
  - AWS_SSM_SECRET_ACCESS_KEY

#### EC2 IAM Role설정

-  AmazonSSMFullAccess



## Trouble shooting

### RDS Database생성시

template0으로부터, LC_COLLATE를 따로 설정 (한글 ordering관련)

```
CREATE DATABASE letusgo OWNER=lhy TEMPLATE template0 LC_COLLATE 'C';
```

[coverage]: https://img.shields.io/codecov/c/github/LeeHanYeong/let-us-go/develop.svg
[codecov]: https://codecov.io/github/LeeHanYeong/let-us-go
[github-action]: https://img.shields.io/github/workflow/status/LeeHanYeong/let-us-go/CI/develop.svg
[github-workflow]: https://github.com/leehanyeong/let-us-go/actions?query=workflow%3ACI
[github-last-commit]: https://img.shields.io/github/last-commit/LeeHanYeong/let-us-go/develop.svg
[github]: https://github.com/leehanyeong/let-us-go
[made-with]: https://img.shields.io/badge/Made%20with-Django-blue
[django]: https://www.djangoproject.com/
