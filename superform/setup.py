from setuptools import setup
setup(
    name='superform',
    packages=['superform'],
    include_package_data=True,
    install_requires=[
        'flask',
        'google-api-python-client',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'requests',
        'python3-saml', 'sqlalchemy'
    ],
)