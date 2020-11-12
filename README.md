# Property Sales of NYC

## Introduction

API to query property sales and web interface to view average sale price per year.

## API

Browsable API at http://localhost/swagger-ui/

Chart for average sale price over year at http://localhost/

### Endpoints

#### /api/sales/

List of property sales. Defaults to 100 records per page.

##### GET parameters

|name|type|description|
|----|----|-----------|
|limit|integer|number of results per page|
|offset|integer|initial index of returned results|
|price_min|number|minimum sale price|
|price_max|number|maximum sale price|
|date_after|date (YYYY-mm-dd)|minimum sale date|
|date_before|date (YYYY-mm-dd)|maximum sale date|
|borough|string|name of borough to query|
|neighborhood|string|name of neighborhood to query|

##### Result

```json
{
  "count": 123,
  "next": "http://api.example.org/api/sales/?offset=400&limit=100",
  "previous": "http://api.example.org/api/sales/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "borough": "string",
      "neighborhood": "string",
      "address": "string",
      "price": 0,
      "date": "2020-11-12T23:29:05.302Z"
    }
  ]
}
```

#### /api/sales/{id}/

##### Result

```json
{
  "id": 0,
  "borough": "string",
  "neighborhood": "string",
  "address": "string",
  "price": 0,
  "date": "2020-11-12T23:29:05.302Z"
}
```

#### /api/sales/summary/

Summary of average sale price by year of queried data.

##### GET parameters

|name|type|description|
|----|----|-----------|
|price_min|number|minimum sale price|
|price_max|number|maximum sale price|
|date_after|date (YYYY-mm-dd)|minimum sale date|
|date_before|date (YYYY-mm-dd)|maximum sale date|
|borough|string|name of borough to query|
|neighborhood|string|name of neighborhood to query|

##### Result

```json
{
    "result": [
        {
            "year": 2003,
            "avg": 1208391.4966309094
        },
        {
            "year": 2004,
            "avg": 1594847.7004073958
        },
        {
            "year": 2005,
            "avg": 2069719.9734724157
        }
    ]
}
```

## Deploy

```shell script
git clone https://github.com/zachary822/housing_prices.git
cd housing_prices
# also downloads data on first run
docker-compose up --build  # start
docker-compose down # stop
```
