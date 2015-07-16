## Installing
`cd canyonero && python setup.py develop`

## Running
`python -m canyonero`

This will start an instance of the REST API at `localhost:5000`

## Using

```
curl http://localhost:5000/1 -d "some body" -X PUT
curl http://localhost:5000/1
curl http://localhost:5000/
```
