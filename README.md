# Mini Wallet Exercise

&nbsp;

#### 1. Virtual environment setup (Python version 3.6.9)
```sh
$ virtualenv -p python3 test-env
```
#### 2. Install requirements
```sh
$ source env/bin/activate
(test-env)$ pip install -r requirements.txt
```
#### 3. Run server (localhost)
```sh
(test-env)$ Python manage.py runserver
```

Use the API collection to setup the environment in post

Initialize the auth token using below Api:
http://locahost:800/api/v1/init