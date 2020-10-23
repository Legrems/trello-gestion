from setuptools import setup


setup(
    name="trello-gestion",
    version="0.0.1",
    description="A python tools for restoring trello boards from json",
    url="https://github.com/Legrems",
    author="Gremaud Loïc",
    author_email="flamelegrems@gmail.com",
    packages=["trello_gestion"],
    entry_points={"console_scripts": ["trello-gestion=trello_gestion.commands:main"]},
    install_requires=[
        "tqdm<=4.51",
        "requests<=2.25",
        "python-dateutil<=2.9",
    ],
    include_package_data=True,
)
