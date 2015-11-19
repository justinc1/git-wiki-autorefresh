#!/usr/bin/env python

"""
To use with github/gitlab wiki, for local edit preview.
The gollum local server shows only commited data.
So do git add + commit when any file is saved.

pip install GitPython==1.0.1
"""

import logging
import logging.config
import sys
from git import Repo
from time import sleep
from os.path import abspath, curdir


LOG_FILE = '/tmp/git-wiki-autorefresh.log'
LOG_LEVEL = logging.DEBUG
# ADD_UNTRACKED = False


def main():
    log = logging.getLogger(__name__)
    commit_msg = 'auto-save'
    if len(sys.argv) >= 2:
        commit_msg = sys.argv[1]
    log.info('commit_msg %s', commit_msg)
    
    commit_cnt = 0
    repo_path = abspath(curdir)
    log.info('repo_path %s', repo_path)
    repo = Repo(repo_path)

    while True:
        if repo.is_dirty():
            log.info('repo is dirty')
            # refresh all_files, so that external 'git add'-ed files are included too
            all_files = []
            for ent in repo.index.entries:
                filename = ent[0]
                log.debug('adding file %s', filename)
                all_files.append(filename)
            # add and commit
            repo.index.add(all_files)
            log.info('repo commit')
            repo.index.commit(commit_msg + '-' + str(commit_cnt))
            commit_cnt += 1
        sleep(1)
        
        
def setup_logging():
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                # 'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
                'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
            },
            'simple': {
                #'format': '%(levelname) 8s %(message)s'
                'format': '%(levelname)-8s %(asctime)s %(module)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                #'class': 'logging.NullHandler',
                'formatter': 'simple'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': LOG_FILE,
            },
        },
        'loggers': {
            '': {
                'handlers': ['file', 'console'],
                #'handlers': [ 'console'],
                'propagate': False,
                'level': LOG_LEVEL,
            },
        }
    }
    logging.config.dictConfig(LOGGING)

    
if __name__ == "__main__":
    setup_logging()
    main()

##