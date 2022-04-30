# Elice Assignment



## Environment

- OS
  - macOS
- python --version
  - python 3.9.10
- DB
  - postgresqld
- run on localhost
- 
- 

## File Structure

```
├── my_forum/
│      ├─ __init__.py
│      ├─ models.py
│      ├─ forms.py
│      ├─ views/
│      │   └─ main_views.py
│      ├─ static/
│      │   └─ style.css
│      └─ templates/
│            └─ index.html
├── requirements.txt
├── README.md
└── config.py
```


## Prerequisite

- Make a virtual environment

  ```shell
  $ cd elice_assignment
  $ python3 -m venv myvenv
  ```

- Run a virtual environment

  ```shell
  (myvenv) ~/elice_assignment $ source myvenv/bin/activate
  ```

- Install requirements

  - install requirements

    ```shell
    (myvenv) ~$ pip install -r requirements.txt
    ```

  - pip upgrade

    ```shell
    (myvenv) ~$ python3 -m pip install --upgrade pip
    ```

    

## Usage

```shell
(myvenv) ~/elice_assignment $ export FLASK_APP=my_forum
```

```shell
(myvenv) ~/elice_assignment $ export FLASK_ENV=development
```

```shell
(myvenv) ~/elice_assignment $ flask run
```

## Database managing

- 모델을 새로 생성하거나 변경할 때 사용
  - 실행하면 **작업 파일이 생성**된다.

```shell
(myvenv) ~/elice_assignment $ flask db migrate
```

- 모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용
  - 위에서 생성된 작업 파일을 실행하여 **데이터베이스를 변경**한다.

```shell
(myvenv) ~/elice_assignment $ flask db upgrade
```

## Wrap up

- db에 constraint로 길이 제한을 걸었으니, forms.py에도 반영해야함
- 로그인 로직
  - 방법1 : HMAC을 써서 쿠키를 못 바꾸게
  - 방법2 : redis에 넣을 때 random string을 key로 써서 그 key를 쿠키에 넣고, redis에도 넣고 한다.
- pagination은 특정 page에 대한 요청임
  - flask ORM에서 limit과 offset을 쓰면 됨

