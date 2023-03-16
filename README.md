# FastdlUpdater

Simple python script to update and maintain fastdl folder for games such as CS:GO.

# What it can do:

* Add and compress to bz2 format (Only if the file is smaller then 150mb) files from your game root directory to fastdl directory;
* Remove files from fastdl if they aren't in your game root directory anymore (Will also delete empty folders that are left on fastdl);
* Update files that were changed in game root directory and don't match to fastdl ones (Only when ``full`` argument is specified);
* Will look only for required files in game root directory (For example only ``.bsp`` and ``.nav`` files in ``maps/`` folder).

# Requirements:

* Python 3.4.2 and above;

# Usage:

1. Edit ``gameRootFolder`` and ``fastdlRootFolder`` variables in ``fastdl.py`` to point directly into game root folder and fastdl folder respectivly, relative to ``fastdl.py`` script (Use only ``/`` as a separator!);
2. Optionally edit the ``fastdl_blacklist.txt`` file to blacklist default files you don't want to be added to the fastdl.
3. Run the ``fastdl.py`` script, and it should start updating your fastdl folder.
4. Additionally you can use optional arguments if you seek a need in this (Refer to [arguments](#Arguments) section);

# Arguments:
* ``-h``, ``--help``: Prints help this help info;
* ``-f``, ``--full_check``: Performs full check on all files to ensure their validity (NOTE: The operation is very costly!!!);
* ``-v {0, 1, 2}``, ``--verbose {0, 1, 2}``: Verbosity levels (default: 2):
  * 0 - Only changes to the data would be printed;
  * 1 - Header, footer, and data changes would be printed;
  * 2 - Header, footer, blacklist notifications, comparison info (if ``-f`` is used) and data changes would be printed;

# Example crontab usage:
``*/5 * * * * USER "python3 PATH/fastdl.py" > /dev/null 2>&1`` - where ``*/5 * * * *`` will run the script every 5 minutes, ``USER`` is a user to run the script, ``PATH/fastdl.py`` is an absolute path to ``fastdl.py`` script, ``> /dev/null 2>&1`` would null the input and output streams.
