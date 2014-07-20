import sys
from subprocess import call


# Run the zetup script (reading config from zetuprc):
exec(open('__init__.py').read())

if 'sdist' in sys.argv:
    status = call('scons')
    if status:
        sys.exit(status)


zetup(
  packages=[
    'QtQuery',
    ],
  )
