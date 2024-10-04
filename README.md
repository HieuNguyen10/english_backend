## ******** SMILE HOME PROJECT ********

### Cấu trúc project
``` commandline
.  
├── alembic  
│   ├── versions    // thư mục chứa file migrations  
│   └── env.py  
├── app  
│   ├── api         // các file api được đặt trong này  
│   ├── core        // chứa file config load các biến env & function tạo/verify JWT access-token  
│   ├── db          // file cấu hình make DB session  
│   ├── helpers     // các function hỗ trợ như login_manager, paging  
│   ├── models      // Database model, tích hợp với alembic để auto generate migration  
│   ├── schemas     // Pydantic Schema  
│   ├── services    // Chứa logic CRUD giao tiếp với DB  
│   └── main.py     // cấu hình chính của toàn bộ project  
├── tests  
│   ├── api         // chứa các file test cho từng api  
│   ├── faker       // chứa file cấu hình faker để tái sử dụng  
│   ├── .env        // config DB test  
│   └── conftest.py // cấu hình chung của pytest  
├── .gitignore  
├── alembic.ini  
├── docker-compose.yaml  
├── Dockerfile  
├── env.example  
├── logging.ini     // cấu hình logging  
├── postgresql.conf // file cấu hình postgresql, sử dụng khi run docker-compose  
├── pytest.ini      // file setup cho pytest  
├── README.md  
└── requirements.txt
```

### Environment and Requirements Installation  (You can choose 1 of the 2 ways below)
#### Install common
``` bash
* sudo apt-get update
* sudo apt install -y build-essential libssl-dev libffi-dev
* sudo apt-get install g++ gcc
* sudo apt-get install libpq-dev
* sudo apt install apt-transport-https ca-certificates curl software-properties-common
* sudo apt-get install wget ca-certificates

```

#### C1: install canda
``` bash
> cd /tmp
> curl -O https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh (YES HẾT)
> source ~/.bashrc
> sudo rm -rf Anaconda3-2021.05-Linux-x86_64.sh
> conda update --all
> conda update -n base conda
> conda env list
> conda create -n <name_environment> python=3.8
> conda activate <name_environment>
> sudo pip install --upgrade -r requirements.txt 

```


#### C2: install pipenv
``` bash
> python3 -m pip install --user virtualenv
> python3 -m venv envs
> source envs/bin/activate
> sudo pip install --upgrade -r requirements.txt 

Hoặc

#### 👇️ if you get permissions error  #####

* sudo pip3 install virtualenv
* pip install virtualenv --user
* virtualenv envs
* source envs/bin/activate
* sudo pip install --upgrade -r requirements.txt 

```


### Databases
#### B1: Install postgresql database on ubuntu 20.04
``` bash
* sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
* sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
* sudo apt-get update
* sudo apt-get -y install postgresql-14
```

#### B2: create databases
``` bash
* sudo -u postgres psql
* CREATE DATABASE spincontents;
* CREATE USER user_spincontents WITH PASSWORD '123456';
* GRANT ALL PRIVILEGES ON DATABASE spincontents TO user_spincontents;
```

#### B3: Connect databases
``` bash
* change your username , password, database_name in path to file ./env.example
* cp env.example .env
* echo APP_ENV=dev >> .env
* echo SECRET_KEY=$(openssl rand -hex 32) >> .env
```

#### B4: init tables
``` bash
* alembic revision --autogenerate
* alembic upgrade head
```

### Run APP
``` bash
* uvicorn app.main:app --host 0.0.0.0 --port 5000
* uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload (not run on production)

```