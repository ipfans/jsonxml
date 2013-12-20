JSONXML
========
Converter between xml and json

Usage
----
```
    data = {
        "data": {
            "a": "1",
            "b": "2",
        },
    }
    json_data = json.dumps(data)
    xml_data = json2xml(json_data)
    print xml_data
    json_data = xml2json(xml_data, True, 0)
    print json_data
```

License
-------
This code released under the terms of the [MIT license](http://opensource.org/licenses/MIT).

Contributors
------------
This script was originally written by R.White, Hay Kranen, George Hamilton and Dan Brown. Thanks for your works.