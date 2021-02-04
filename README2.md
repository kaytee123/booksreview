```sh
python3 -m venv venv
pip install -r requirements.txt

export FLASK_APP=app.py
$ flask run
 * Running on http://127.0.0.1:5000/

```

Or run `$ flask run --host=0.0.0.0` to allow access from another computer

---

## Client Request

<br>

### Request Payload Structure

_**name**_: The name of the command example, `"AddBook"`

_**data**_: Data for the command

_**meta**_: Metadata for the command

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
