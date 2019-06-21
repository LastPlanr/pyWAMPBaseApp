# pyWAMPBaseApp

Utility classes for creating WAMP enabled applications.

## Usage

```python

from wampbaseapp.wamp_app import WampApp, register_method


class MyApplication(WampApp):
    def init(self):
        # Initialize things here instead of
        # overloading __init__ method.
        pass

    @register_method(prefix.my_method')
    def my_method(self, x):
        return x * 10

```
