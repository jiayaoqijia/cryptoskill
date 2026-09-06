# SPDX-License-Identifier: LicenseRef-Blockscout
import os
import sys


def is_binary(file_path):
    """Checks if a file is binary by looking for null bytes in the first 1024 bytes."""
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            if b"\0" in chunk:
                return True
    except Exception:
        return True
    return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 read_temp_file.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Resolve absolute paths
    cwd = os.getcwd()
    # Ensure we strictly target the 'temp' directory in the project root
    temp_dir = os.path.join(cwd, "temp")
    abs_file_path = os.path.abspath(file_path)

    # Security check: must be inside temp dir
    # Using os.path.commonpath to verify ancestry safely
    try:
        if os.path.commonpath([temp_dir, abs_file_path]) != temp_dir:
            print(f"Error: Security violation. File '{file_path}' is not within the allowed 'temp/' directory.")
            sys.exit(1)
    except ValueError:
        print(f"Error: Security violation. File '{file_path}' is not within the allowed 'temp/' directory.")
        sys.exit(1)

    if not os.path.exists(abs_file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(abs_file_path):
        print(f"Error: '{file_path}' is not a file.")
        sys.exit(1)

    if is_binary(abs_file_path):
        print(f"Error: File '{file_path}' appears to be binary and cannot be read.")
        sys.exit(1)

    # Line count check and read
    try:
        with open(abs_file_path, encoding="utf-8") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= 2000:
                    print(f"Error: File '{file_path}' exceeds the 2000 line limit.")
                    sys.exit(1)
                lines.append(line)

            print("".join(lines))
    except UnicodeDecodeError:
        print(f"Error: File '{file_path}' is not valid UTF-8 text.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
