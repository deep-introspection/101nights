Folder for MMF files.

# Compress for FAT32
tar cvzf - Nathalie-78_20171118_123017.mff | split -b 4294967295 - /Volumes/HAL9000/Nathalie-78_20171118_123017.mff.tgz.

# Decompress
## Linux
cat Nathalie-78_20171118_123017.mff.tgz.* | tar xzf -
## Windows
copy /b file1 + file2 + file3 + file4 filetogether