# FastdlUpdater
Simple python script to update and maintain fastdl folder for games such as CS:GO.

# What it can do:
* Add and compress to bz2 format (Only if the file is smaller then 150mb) files from your game root directory to fastdl directory;
* Remove files from fastdl if they aren't in your game root directory anymore (Will also delete empty folders that are left on fastdl);
* Update files that were changed in game root directory and don't match to fastdl ones (Only when ``full`` argument is specified);
* Will look only for required files in game root directory (For example only ``.bsp`` and ``.nav`` files in ``maps/`` folder).

# Requirements:
* python 3.4.2 (Was tested only on that version!).

# Usage:
Edit ``gameRootFolder`` and ``fastdlRootFolder`` variables in ``fastdl.py`` to point directly into game root folder and fastdl folder respectivly, relative to ``fastdl.py`` script (Use only ``/`` as a separator!). Then run ``fastdl.py`` script, and it should start updating your fastdl folder. You can also run script with ``full`` as a parameter, like ``python3 fastdl.py full``, and that will update all files that don't match with root game directory (That may take a while if you have a lot of big files in your root game directory, this is why it was made as an optional thing).
