# Summary

To run: `make dev`, you have to have python3 installed

## How to use

Run the server (see above) and make a http request

```
GET http://localhost:5555/api/v1/youtube/gqaHkPEZAew/summary
```

Optionally you may also load transcript (if available)

```
GET http://localhost:5555/api/v1/youtube/gqaHkPEZAew/captions
```
