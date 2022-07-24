# python-orange-funbox

### Prerequisites

This module is written in python 2

### How to install

Clone the `funbox.py` file to the directory in which you want to use it:
```bash
python.py
your_script.py
```

### How to use this package:
```python
# Import the module:
import funbox

# Initialize:
funbox = funbox.FunBox("http://192.168.1.1", "put_password_here")

# Now you can use the module methods:
import json
info = funbox.DeviceInfo()
print json.dumps(info, indent=4)

# If needed, reconnect to funbox:
funbox.reconnect()

# You can also restart your router
funbox.restart()
```

More examples can be found in the wiki.
