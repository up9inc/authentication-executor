import setuptools

setuptools.setup(
    name="authentication_executor",
    version="1.0.0",
    author="Up9",
    author_email="admin@up9.com",
    description="Authentication Executor",
    long_description="Authenticates according to a configuraion",
    long_description_content_type="text/markdown",
    url="https://github.com/up9inc/authentication-executor",
    packages=setuptools.find_namespace_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
