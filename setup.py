import setuptools

setuptools.setup(
    name="proxy_for_interface",
    use_incremental=True,
    description="Automatically proxy interface methods",
    long_description=(
        "Rethinking composition without soriricide"
    ),
    author="Moshe Zadka",
    author_email="moshez@zadka.club",
    url="https://github.com/moshez/proxy_for_interface/",
    packages=["proxy_for_interface"],
    package_dir={"": "src"},
    setup_requires=[
        'incremental',
    ],
    install_requires=[
        'attrs',
        'incremental',
        'publication',
        'zope.interface',
    ],
    license="MIT",
)
