#!/usr/bin/python

from optparse import OptionParser
import os
from subprocess import check_call
import sys
import time


mw_files = (
    '/Applications/MWClient.app',
    '/Applications/MWEditor.app',
    '/Applications/MWServer.app',
    '/Documents/MonkeyWorks',
    '/Library/Application Support/MonkeyWorks',
    '/Library/Application Support/NewClient',
    '/Library/Frameworks/MonkeyWorksCocoa.framework',
    '/Library/Frameworks/MonkeyWorksCore.framework',
    '/Library/Frameworks/Narrative.framework',
    '/Library/Frameworks/Sparkle.framework',
    '/Library/MonkeyWorks',
    '/Library/Receipts/MonkeyWorksAppSupport.pkg',
    '/Library/Receipts/MonkeyWorksApps.pkg',
    '/Library/Receipts/MonkeyWorksFrameworks.pkg',
    '/Library/Receipts/MonkeyWorksResources.pkg',
    '/Library/Receipts/MonkeyWorksSupport.pkg',
    '/Library/Receipts/applications.pkg',
    '/Library/Receipts/applicationsupport.pkg',
    '/Library/Receipts/developer.pkg',
    '/Library/Receipts/documents.pkg',
    '/Library/Receipts/frameworks.pkg',
    )


def backup_files(filelist, backupdir):
    if os.path.exists(backupdir):
        ctime = os.stat(backupdir)[-1]
        check_call(['mv',
                    backupdir,
                    '%s (%s)' % (backupdir, time.ctime(ctime))])

    for filename in filelist:
        if os.path.exists(filename):
            destdir = os.path.join(backupdir, os.path.dirname(filename[1:]))
            sys.stderr.write('Moving "%s" to "%s"\n' % (filename, backupdir))
            check_call(['mkdir', '-p', destdir])
            check_call(['mv', filename, destdir])


def restore_files(filelist, backupdir):
    for filename in filelist:
        srcfile = os.path.join(backupdir, filename[1:])
        if os.path.exists(srcfile):
            sys.stderr.write('Restoring "%s" from "%s"\n' %
                             (filename, backupdir))
            check_call(['mv', srcfile, os.path.dirname(filename)])

    check_call(['rm', '-Rf', backupdir])


def get_backupdir(path):
    return os.path.expanduser(os.path.join('~/.Trash', path))


def main():
    parser = OptionParser()
    parser.add_option('-b', '--backup', action='store_true', dest='backup',
                      help="don't restore, but back up old installation")
    (options, args) = parser.parse_args()

    backupdir = get_backupdir('Old MonkeyWorks')

    if options.backup:
        backup_files(mw_files, backupdir)
    else:
        backup_files(mw_files, get_backupdir('Uninstalled MonkeyWorks'))
        restore_files(mw_files, backupdir)


if __name__ == '__main__':
    main()