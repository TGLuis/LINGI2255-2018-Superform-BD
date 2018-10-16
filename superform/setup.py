from setuptools import setup

setup(
    name='superform',
    packages=['superform'],
    include_package_data=True,
    install_requires=[
        'flask',
        'google-api-python-client',
        'python3-saml', 'sqlalchemy'
    ],
)
