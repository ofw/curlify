# Curlify - convert python requests request object to cURL command

# Example

```py
import curlify
import requests

response = requests.get("http://google.ru")
print(curlify.to_curl(response.request)
```
