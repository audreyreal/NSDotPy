# NSDotPy
A Python wrapper around requests for legally interacting with the HTML NationStates site, as well as a barebones API client. Built for legality first and foremost, as well as ease of use.

## Installation
``pip install nsdotpy``

## Simple Example
```python
from nsdotpy import NSClient
session = NSClient("NSDotPy Example," "1.0.0", "User Nation", "Dev Nation")
if session.login("User Nation", "Password"):  # logs in and checks if login was successful
    session.move_to_region("Lily")  # only moves if you successfully logged in
```
## TODO:
- ~~Region Admin Controls~~
- Dossier and reports handling
- More fleshed out API Client
