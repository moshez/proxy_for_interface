from typing import Any

import attr
from proxy_forward import proxy_for, generate_proxy
from zope import interface

class IFoo(interface.Interface):
    def foo(hello):
        pass

class IBar(interface.Interface):
     def bar(thing):
         pass

@attr.s(auto_attribs=True)
class SimpleFoo:
    x: Any = attr.ib(default=1)

    def foo(self, hello):
        print("foo", self.x, hello)

@attr.s(auto_attribs=True)
class SimpleBar:
    x: Any = attr.ib(default=5)

    def bar(self, thing):
        print("bar", self.x, thing)

@generate_proxy
@attr.s(auto_attribs=True)
class Foo:
    _foo: Any = attr.ib(factory=SimpleFoo, metadata={proxy_for: IFoo})
    _bar: Any = attr.ib(factory=SimpleBar, metadata={proxy_for: IBar})
 
a = Foo()
a.foo("hello")
a.bar("goodbye")
