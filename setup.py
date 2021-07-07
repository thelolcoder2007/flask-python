import setuptools

with open("c:/code/flask-python/readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-package-app-terents",
    version="Alpha0.0.1",
    author="thelolcoder2007",
    author_email="simon.vanharingen@gmail.com",
    description="Flask package for fleur home",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: no license",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"flask"},
    packages=setuptools.find_packages(where="flask"),
    python_requires=">=3.9"
    install_requires=['flask', 'flask_wtf', 'wtforms']
)
