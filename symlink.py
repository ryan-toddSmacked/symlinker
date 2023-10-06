#!/usr/bin/env python3

import os
import argparse
import glob
import fnmatch


def main():
    parser = argparse.ArgumentParser(description="Create symbolic links")

    parser.add_argument("source", help="Source file or directory")
    parser.add_argument("destination", help="Destination file or directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="Check files recursively")
    parser.add_argument("-i", "--include", nargs="*", type=str, help="Include only files or directories matching this pattern")
    parser.add_argument("-e", "--exclude", nargs="*", type=str, help="Exclude files or directories matching this pattern")
    parser.add_argument("-c", "--create", action="store_true", help="Create destination directory if it does not exist")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite of existing files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    parser.add_argument("-p", "--prune", action="store_true", help="Prune empty directories")
    args = parser.parse_args()

    
    # Get a list of all the files
    files = []

    if args.recursive:
        # use glob to get all the files
        files = glob.glob(args.source + "/**", recursive=True)
    else:
        files = glob.glob(args.source + "/*")

    # Remove source path from files list
    files = [x.replace(args.source, '') for x in files]

    excluded_files = []
    if args.exclude:
        for pattern in args.exclude:
            excluded_files.extend(fnmatch.filter(files, pattern))

    # loop through the include patterns and remove and excluded files that match the pattern
    if args.include:
        for pattern in args.include:
            # find all excluded files that match the pattern
            matches = fnmatch.filter(excluded_files, pattern)
            # remove the matches from the excluded files list
            for match in matches:
                excluded_files.remove(match)


    # remove the excluded files from the files list
    for file in excluded_files:
        files.remove(file)

    # if prune is set, remove empty directories from files list
    if args.prune:
        for file in files:
            if os.path.isdir(file):
                # This is a directory, check if it is empty
                if not os.listdir(file):
                    # Directory is empty, remove it from list
                    files.remove(file)

    # Create the symbolic links, Replace the source string with the target string
    # Append the source string to the files list to create the src_files list
    # Append the destination string to the files list to create the dest_files list
    src_files = [args.source + x for x in files]
    dest_files = [args.destination + x for x in files]

    idx = 0
    while (idx < len(files)):
        file = src_files[idx]
        destination = dest_files[idx]
    
        # put the symlink operation in a try block
        # os.symlink can throw the following exceptions: FileExistsError, FileNotFoundError, PermissionError
        try:
            os.symlink(file, destination)
            if args.verbose:
                print(f'Created symlink: {destination} -> {file}')
        except FileExistsError:
            if args.verbose and not args.force:
                print(f'Symlink already exists: {destination} -> {file}')
            else:
                # Delete the destination file and try to create the symlink again
                try:
                    os.remove(destination)
                    # decrement the index so we can try to create the symlink again
                    idx = idx - 1
                except:
                    print(f'Could not delete file: {destination}')
                pass
            pass
        except FileNotFoundError:
            if args.verbose and not args.create:
                print(f'File not found: {file}')
            else:
                # Attempt to create the output directory
                try:
                    os.makedirs(os.path.dirname(destination), exist_ok=True)
                    # decrement the index so we can try to create the symlink again
                    idx = idx - 1
                except:
                    print(f'Could not create directory: {os.path.dirname(destination)}')
                pass
            pass
        except PermissionError:
            if args.verbose:
                print(f'Permission denied: {file}')
            pass
        except OSError:
            if args.verbose:
                print(f'OS Error: {file}')
            pass
        except:
            if args.verbose:
                print(f'Unknown Error: {file}')
            pass
        idx = idx + 1

    pass

if __name__ == '__main__':
    main()






