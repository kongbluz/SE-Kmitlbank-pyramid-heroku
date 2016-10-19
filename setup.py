from setuptools import setup

requires = [
    'pyramid',
    'pyramid_tm',
    'pyramid_chameleon',
    'passlib',
    'sqlalchemy',
    'bcrypt',
    'zope.sqlalchemy',
    'colander',
    'deform',
    'paste',
    'waitress',
    'psycopg2',
]

setup(name = 'bin',
      install_requires = requires,
      entry_points="""\
      [paste.app_factory]
      main = bin:main
      [console_scripts]
      initialize_bin_db = bin.scripts.initializedb:main
      """,
)
