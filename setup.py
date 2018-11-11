import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="udemy",
    version="0.0.1",
    author="Prem Lakshmanan",
    author_email="prem1pre@gmail.com",
    description="Software to load and analyze udemy free api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PREM1980/udemy",
    packages=setuptools.find_packages(),
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)