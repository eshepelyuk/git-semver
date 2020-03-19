from setuptools import setup, find_packages

setup(
    author='Ievgenii Shepeliuk',
    author_email='eshepeluyk@gmail.com',
    description='Semantic versions management integrated to git.',
    license='Apache License, Version 2.0',
    name='git_semver',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    long_description="",
    classifiers=[],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires = ">=3.6",
    install_requires=['GitPython~=3.1', 'semantic-version~=2.8', 'click~=7.0'],
    extras_require={
        'test': ['pytest ~= 5.3']
    },
    entry_points={'console_scripts': ['git-semver=git_semver.main:git_semver']},
    url='https://github.com/eshepelyuk/git-semver'
)
