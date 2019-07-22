import hashlib
import textwrap

import attr

import publication

from ._version import __version__


def add_method_dunders(cls, method):
    try:
        method.__module__ = cls.__module__
    except AttributeError:
        pass

    try:
        method.__qualname__ = ".".join((cls.__qualname__, method.__name__))
    except AttributeError:
        pass


def make_forwarding_method(attr_name, iface, method_name):
    args = iface.getDescriptionFor(method_name).getSignatureString()[1:-1]
    source = textwrap.dedent(
        f"""\
    def {method_name}(self, {args}):
        return self.{attr_name}.{method_name}({args})
    """
    )
    sha = hashlib.sha1()
    sha.update(method_name.encode("utf8"))
    sha.update(attr_name.encode("utf8"))
    sha.update(iface.__module__.encode("utf8"))
    sha.update(iface.getName().encode("utf8"))
    sha.update(attr_name.encode("utf8"))
    unique_file_name = "<proxy generated {sha.hexdigest()}>"
    return make_function(source, method_name, unique_file_name)


def make_function(source, method_name, unique_file_name):
    globs = {}
    locs = {}
    bytecode = compile(source, unique_file_name, "exec")
    eval(bytecode, globs, locs)
    return locs[method_name]


def forward_for_interface(cls, attr_name, iface):
    for method_name in iface:
        method = make_forwarding_method(attr_name, iface, method_name)
        add_method_dunders(cls, method)
        setattr(cls, method_name, method)


class _ProxySentinel:
    pass


proxy_for = _ProxySentinel()


def generate_proxy(cls):
    for attribute in attr.fields(cls):
        if proxy_for not in attribute.metadata:
            continue
        for iface in attribute.metadata[proxy_for]:
            attr_name = attribute.name
            forward_for_interface(cls, attr_name, iface)
    return cls


__all__ = ["generate_proxy", "proxy_for", "__version__"]

publication.publish()
