from setuptools import setup, find_packages

setup(
    name='brainkey_server',
    version='0.1',
    packages=find_packages(),
    url='',
    license='Apache 2.0',
    author='Brady Williamson',
    author_email='brady.williamson@uc.edu',
    description='Commands for Running DIMSE to DICOMweb Server',
    install_requires=[
        'requests',
        'pydicom',
        'pynetdicom',
        'pathlib',
        'urllib3',
        'azure-identity',
        'whatismyip'
    ]
)
