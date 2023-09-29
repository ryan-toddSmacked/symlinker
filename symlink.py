
import argparse as ap
import os
import glob
import errno


def main():

    parser = ap.ArgumentParser(prog="symlink", description='Create symlinks of files to a specified directory.')
    parser.add_argument('-b', metavar="--base-dir", type=str, nargs=1, required=True, help='The base directory to search for files.')
    parser.add_argument('-t', metavar="--token", type=str, nargs='+', required=True, help='A glob token to search for in the filenames.')
    parser.add_argument('-d', metavar="--dest-dir", type=str, nargs=1, required=True, help='The destination directory to create the symlinks in.')
    parser.add_argument('--recursive', action="store_true", help='Whether to search subdirectories.')
    parser.add_argument('--prune', action="store_true", help='Whether to prune the destination directory of intermediate sub-directories from the base directory, just keeping the files.')
    parser.add_argument('--verbose', action="store_true", help='Whether to print verbose output.')

    args = parser.parse_args()

    # Get the base directory
    base_dir = args.b[0]

    # Get the glob tokens
    glob_tokens = args.t

    # Get the destination directory
    dest_dir = args.d[0]

    # Get the recursive flag
    recursive = args.recursive

    # Get the prune flag
    prune = args.prune

    # Get the verbose flag
    verbose = args.verbose

    if (verbose):
        print("Base directory: {}".format(base_dir))
        print("Glob tokens: {}".format(glob_tokens))
        print("Destination directory: {}".format(dest_dir))
        print("Recursive: {}".format(recursive))
        print("Prune: {}".format(prune))

    # Get the files
    files = []

    for token in glob_tokens:
        if (recursive):
            files.extend(glob.glob(os.path.join(base_dir, "**", token), recursive=True))
        else:
            files.extend(glob.glob(os.path.join(base_dir, token)))
        
        if (verbose):
            print("Found {} files matching token: {}".format(len(files), token))
            for f in files:
                print(f)
        
        # sift out the unique files
        files = list(set(files))

    # Run through the files and create symlinks, attempting to create directories as needed
    for f in files:
        # Get the filename
        filename = os.path.basename(f)

        # Get the directory
        directory = os.path.dirname(f)

        # Get the destination directory
        if (prune):
            dest_directory = dest_dir
        else:
            dest_directory = os.path.join(dest_dir, os.path.relpath(directory, base_dir))

        # Create the destination directory if it doesn't exist
        if not os.path.exists(dest_directory):
            try:
                os.makedirs(dest_directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    # Display the error, and continue
                    print("Error creating directory: {}".format(dest_directory))
                    print(e)
                    continue

        # Create the symlink
        symlink = os.path.join(dest_directory, filename)
        if (verbose):
            print("Creating symlink: {} -> {}".format(symlink, f))
        try:
            os.symlink(f, symlink)
        except OSError as e:
            if e.errno != errno.EEXIST:
                # Display the error, and continue
                print("Error creating symlink: {} -> {}".format(symlink, f))
                print(e)
                continue
            else:
                # The symlink already exists, so continue
                continue

    pass


if __name__ == '__main__':
    main()
