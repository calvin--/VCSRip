# VCSRip
Pentesting tool for identifying and ripping public version control systems.

## Features

- Scan for public version control systems on host

**git**

- Download git metafiles
- Download git objects
- Download git pack files if possible
- Extract git objects to plain source files

**svn**

- Supports new and old svn structure (wc.db vs. entries)
- Download pristine copies of source files

## Reliability

This tool works by identifying if the target host has been misconfigured to allow direct file access in dot (.) folders, like .svn and .git. Directory listing is not needed for the tool to function. Even though the target host allows access to the required metafiles, it is not guaranteed that it will be able to restore plaintext files.

**git**

For .git the amount of plaintext files that can be salvaged depends on several factors. The index file will always contain a list of filenames (and paths) and the corresponding sha1 hash. Git stores data in either git objects or packfiles. Git occasionally pack objects into pack files to save space.

If all the objects are present in the .git/objects directory, the tool will be able to download these and extract plaintext files (objects are zlib compressed). Often not all objects are present, because git has packaged them to pack files. In these cases the tool will fetch the files it can, and be able to extract these, which will give some amount of the source files.

Sometimes the objects folder contains no objects, as they have all been packaged. In these cases there is a small chance that the file .git/objects/info/packs will exist. This file contains the filename of the pack files, which are located in .git/objects/packs. These packfiles can be downloaded and extracted, resulting in the sourcefiles of the repository. However, the .git/objects/info/packs file is not always there. You cannot reliably guess the name of the pack files as they are named based on the sha1 hash of the files they contain.

**svn**

For the new style svn structure, using a sqlite database called wc.db, it is almost always possible to get all the prestine source files of the repository. This works by querying the sqlite database, and getting the path/filename  and the checksum (sha) of the file. This information can be used to create a url for the .svn/pristine/[first two characters of the sha]/[full sha].svn-base.

For the old style svn structure, with entries files in the root and all subfolders, the successrate depends on how the target server is configured. It is always possible to get the filename from them metafiles. Old style svn stores pristine copies of files in .svn/text-base/[FILENAME].svn-base. However, some webservers will not server files of this structure as plaintext: index.php.svn-base, and instead interpret them as their original filetype. This prevent the ability to download the plaintext source files.

## Requirements

- Python 2.7
- requests

## Usage
**TODO: The tool is still under development, so these instructions will change.**

    python __init__.py [url]

**Options**
-v, --verbose: Debug logging
--git-download-pack: Attempt to download pack files, will only work if .git/objects/info/packs exists.


## TODO

- Option to extract git source files
- Mercurial (hg) support
