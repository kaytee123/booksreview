Setting up an enviroment

```sh
python3 -m venv venv
```

Setting up an enviroment: Window

```sh
py -3 -m venv venv
```

## Activate the environment

Before you work on your project, activate the corresponding environment:

```sh
. venv/bin/activate
```

For Windows:

```sh
venv\Scripts\activate
```

## Installing Project Requirements

```sh
pip install -r requirements.txt
```

## Running Flask App

```sh
$ export FLASK_APP=run.py

$ flask run
 * Running on http://127.0.0.1:5000/
```

on Windows:

```sh
set FLASK_APP=run.py

$ flask run
 * Running on http://127.0.0.1:5000/
```

Or run `$ flask run --host=0.0.0.0` to allow access from another computer

---

## Client Request

<br>

### Request Payload Structure

_**name**_: Name of the command example, `"AddBook"`

_**data**_: Data for the command

_**meta**_: Metadata for the command

Please note that you can add an underscore(\_) to command name so it is ingnored.
For example, `_AddBook`

---

### Sample Request

**Endpoint:** `http://127.0.0.1:5000/api/v1`

**Method:** `POST`

**Content-Type:** `application/json`

**Body:**

```json
[
  {
    "name": "AddBook",
    "data": {
      "title": "Law of Leadership",
      "author": "John C. Maxwell",
      "coverImageLink": "",
      "purchaseLink": "",
      "genre": "",
      "summary": ""
    },
    "meta": {}
  },

  {
    "name": "FindBooks",
    "data": {},
    "meta": {}
  }
]
```

**Response Data:**

```json
{
  "AddBook": {
    "cover_image_link": null,
    "created_at": null,
    "genre": null,
    "id": "601c047c15c7faefe5ce22ea",
    "purchase_link": null,
    "summary": null,
    "title": "Law of Leadership"
  }
}
```
