from setuptools import setup

setup(
    name='module_name',
    version='1.0.0',
    author='Your Name',
    author_email='your@email.com',
    description='Details about the package',
    packages=['module_name', 'module_name.config'],
    package_data={
        'module_name': ['config/rules.yml'],
    },
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'dependency1',
        'dependency2',
        # List any other dependencies your module requires
    ],
)