<!-- markdownlint-disable -->

# TODO:
- Region Admin Controls
- Dossier and reports handling
- More fleshed out API Client

<a href="..\src\session.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `session.py`





---

<a href="..\src\session.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `canonicalize`

```python
canonicalize(string: str) → str
```

Converts a string to its canonical form used by the nationstates api. 



**Args:**
 
 - <b>`string`</b> (str):  The string to convert 



**Returns:**
 
 - <b>`str`</b>:  The canonical form of the string 


---

## <kbd>class</kbd> `NSSession`




<a href="..\src\session.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    script_name: str,
    script_version: str,
    script_author: str,
    script_user: str,
    keybind: str = 'space',
    link_to_src: str = ''
)
```

A wrapper around requests that abstracts away interacting with the HTML nationstates.net site. Focused on legality, correctness, and ease of use. 



**Args:**
 
 - <b>`script_name`</b> (str):  Name of your script 
 - <b>`script_version`</b> (str):  Version number of your script 
 - <b>`script_author`</b> (str):  Author of your script 
 - <b>`script_user`</b> (str):  Nation name of the user running your script 
 - <b>`keybind`</b> (str, defaults to space):  Keybind to fulfill one click = one request rule 
 - <b>`link_to_src`</b> (str, optional):  Link to the source code of your script. 




---

<a href="..\src\session.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `api_request`

```python
api_request(data: dict) → Response
```

Sends a request to the nationstates api with the given data. 



**Args:**
 
 - <b>`data`</b> (dict):  Payload to send with the request, e.g. {"nation": "testlandia", "q": "region"} 



**Returns:**
 
 - <b>`requests.Response`</b>:  The response from the server 

---

<a href="..\src\session.py#L372"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `apply_wa`

```python
apply_wa(reapply: bool = True) → bool
```

Applies to the WA. 



**Args:**
 
 - <b>`reapply`</b> (bool, optional):  Whether to reapply if you've been sent an application that's still valid. Defaults to True. 



**Returns:**
 
 - <b>`bool`</b>:  True if the application was successful, False otherwise 

---

<a href="..\src\session.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `change_nation_flag`

```python
change_nation_flag(flag_filename: str) → bool
```

Changes the nation flag to the given image. 



**Args:**
 
 - <b>`flag_filename`</b> (str):  Filename of the flag to change to 



**Returns:**
 
 - <b>`bool`</b>:  True if the flag was changed, False otherwise 

---

<a href="..\src\session.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `change_nation_settings`

```python
change_nation_settings(
    email: str = '',
    pretitle: str = '',
    slogan: str = '',
    currency: str = '',
    animal: str = '',
    demonym_noun: str = '',
    demonym_adjective: str = '',
    demonym_plural: str = '',
    new_password: str = ''
) → bool
```

Given a logged in session, changes customizable fields and settings of the logged in nation. Variables must be explicitly named in the call to the function, e.g. "session.change_nation_settings(pretitle='Join Lily', currency='Join Lily')" 



**Args:**
 
 - <b>`email`</b> (str, optional):  New email for WA apps. 
 - <b>`pretitle`</b> (str, optional):  New pretitle of the nation. Max length of 28. 
 - <b>`slogan`</b> (str, optional):  New Slogan/Motto of the nation. Max length of 55. 
 - <b>`currency`</b> (str, optional):  New currency of the nation. Max length of 40. 
 - <b>`animal`</b> (str, optional):  New national animal of the nation. Max length of 40. 
 - <b>`demonym_noun`</b> (str, optional):  Noun the nation will refer to its citizens as. Max length of 44. 
 - <b>`demonym_adjective`</b> (str, optional):  Adjective the nation will refer to its citizens as. Max length of 44. 
 - <b>`demonym_plural`</b> (str, optional):  Plural form of "demonym_noun". Max length of 44. 
 - <b>`new_password`</b> (str, optional):  New password to assign to the nation. 



**Returns:**
 
 - <b>`bool`</b>:  True if changes were successful, False otherwise. 

---

<a href="..\src\session.py#L419"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `clear_dossier`

```python
clear_dossier() → bool
```

Clears a logged in nation's dossier. 



**Returns:**
 
 - <b>`bool`</b>:  Whether it was successful or not 

---

<a href="..\src\session.py#L395"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `endorse`

```python
endorse(nation: str, endorse: bool = True) → bool
```

Endorses the given nation. 



**Args:**
 
 - <b>`nation`</b> (str):  Nation to endorse 
 - <b>`endorse`</b> (bool, optional):  True=endorse, False=unendorse. Defaults to True. 



**Returns:**
 
 - <b>`bool`</b>:  True if the endorsement was successful, False otherwise 

---

<a href="..\src\session.py#L331"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `join_wa`

```python
join_wa(nation: str, app_id: str) → bool
```

Joins the WA with the given nation. 



**Args:**
 
 - <b>`nation`</b> (str):  Nation to join the WA with 
 - <b>`app_id`</b> (str):  ID of the WA application to use 



**Returns:**
 
 - <b>`bool`</b>:  True if the join was successful, False otherwise 

---

<a href="..\src\session.py#L170"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `login`

```python
login(nation: str, password: str) → bool
```

Logs in to the nationstates site. 



**Args:**
 
 - <b>`nation`</b> (str):  Nation name 
 - <b>`password`</b> (str):  Nation password 



**Returns:**
 
 - <b>`bool`</b>:  True if login was successful, False otherwise 

---

<a href="..\src\session.py#L283"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `move_to_region`

```python
move_to_region(region: str, password: str = '') → bool
```

Moves the nation to the given region. 



**Args:**
 
 - <b>`region`</b> (str):  Region to move to 
 - <b>`password`</b> (str, optional):  Region password, if the region is passworded 



**Returns:**
 
 - <b>`bool`</b>:  True if the move was successful, False otherwise 

---

<a href="..\src\session.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `request`

```python
request(
    url: str,
    data: dict = {},
    files: dict = {},
    allow_redirects: bool = False
) → Response
```

Sends a request to the given url with the given data and files. 



**Args:**
 
 - <b>`url`</b> (str):  URL to send the request to 
 - <b>`data`</b> (dict, optional):  Payload to send with the request 
 - <b>`files`</b> (dict, optional):  Payload to send with requests that upload files 



**Returns:**
 
 - <b>`requests.Response`</b>:  The response from the server 

---

<a href="..\src\session.py#L355"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `resign_wa`

```python
resign_wa()
```

Resigns from the WA. 



**Returns:**
 
 - <b>`bool`</b>:  True if the resignation was successful, False otherwise 

---

<a href="..\src\session.py#L309"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `vote`

```python
vote(pollid: str, option: str) → bool
```

Votes on a poll. 



**Args:**
 
 - <b>`pollid`</b> (str):  ID of the poll to vote on, e.g. "199747" 
 - <b>`option`</b> (str):  Option to vote for (starts at 0) 



**Returns:**
 
 - <b>`bool`</b>:  True if the vote was successful, False otherwise 

---

<a href="..\src\session.py#L435"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `wa_vote`

```python
wa_vote(council: str, vote: str) → bool
```

Votes on the current WA resolution. 



**Args:**
 
 - <b>`council`</b> (str):  Must be "ga" for general assembly, "sc" for security council. 
 - <b>`vote`</b> (str):  Must be "for" or "against". 



**Returns:**
 
 - <b>`bool`</b>:  Whether the vote was successful or not 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
