from datetime import datetime
from pathlib import Path
from fabric.api import local, task, lcd, env
from fabric.contrib.console import confirm
from fabric.utils import abort, puts

FABFILE_DIR = str(Path(env.real_fabfile).parent)
GENERATED_OUTPUT_DIRS = [
    Path(d) for d in [
        'calls',
        'mapped_reads',
        'sorted_reads',
    ]
]

@task
def clean():
    """Remove all generated outputs."""
    dirs_to_remove = [
        '%s/' % folder for folder in GENERATED_OUTPUT_DIRS
    ]
    puts(
        'Fabric is going to remove all generated outputs '
        'under folders: {!s}'.format(', '.join(dirs_to_remove))
    )
    confirm('Proceed to remove all outputs in these folders?', False)

    with lcd(FABFILE_DIR):
        for folder in GENERATED_OUTPUT_DIRS:
            local('rm -rf %s' % folder)
