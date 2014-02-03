"""
Keep your application settings in sync.

Copyright (C) 2013 Laurent Raufaste <http://glop.org/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

from constants import BACKUP_MODE
from constants import RESTORE_MODE
from constants import UNINSTALL_MODE
import appsdb
import application
import mackup
import utils


def main():
    """Main function"""

    # Get the command line arg
    args = utils.parse_cmdline_args()

    mckp = mackup.Mackup()
    app_db = appsdb.ApplicationsDatabase()

    if args.mode == BACKUP_MODE:
        # Check the env where the command is being run
        mckp.check_for_usable_backup_env()

        # Backup each application
        for app_name in utils.get_apps_to_backup():
            app = application.ApplicationProfile(mckp,
                                                 app_db.get_files(app_name))
            app.backup()

    elif args.mode == RESTORE_MODE:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        for app_name in app_db.get_app_names():
            app = application.ApplicationProfile(mckp,
                                                 app_db.get_files(app_name))
            app.restore()

    elif args.mode == UNINSTALL_MODE:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        if utils.confirm("You are going to uninstall Mackup.\n"
                         "Every configuration file, setting and dotfile"
                         " managed by Mackup will be unlinked and moved back"
                         " to their original place, in your home folder.\n"
                         "Are you sure ?"):
            for app_name in app_db.get_app_names():
                app = application.ApplicationProfile(mckp,
                                                     app_db.get_files(app_name)
                                                     )
                app.uninstall()

            # Delete the Mackup folder in Dropbox
            # Don't delete this as there might be other Macs that aren't
            # uninstalled yet
            # delete(mckp.mackup_folder)

            print ("\n"
                   "All your files have been put back into place. You can now"
                   " safely uninstall Mackup.\n"
                   "\n"
                   "Thanks for using Mackup !"
                   .format(os.path.abspath(__file__)))
    else:
        raise ValueError("Unsupported mode: {}".format(args.mode))

    # Delete the tmp folder
    mckp.clean_temp_folder()
