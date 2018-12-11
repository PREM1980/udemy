import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'certifi==2018.8.24'
    'chardet==3.0.4',
    'configparser==3.5.0',
    'future==0.17.1',
    'idna==2.7',
    'requests==2.19.1',
    'urllib3==1.23',
    'nose==1.3.7',
    'responses==0.10.2',
    'coverage==4.5.2',
    'nose==1.3.7',
    'python-coveralls==2.9.1'
]

setuptools.setup(
    name="udemy",
    version="0.0.1",
    author="Prem Lakshmanan",
    author_email="prem1pre@gmail.com",
    description="Software to load and analyze udemy free api data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PREM1980/udemy",
    install_requires=install_requires,
    keywords='',
    packages=setuptools.find_packages(),
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)