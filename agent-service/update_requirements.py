import subprocess
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "requirements.txt"


def get_package_current_version(line):
    if "[" in line and "]" in line:
        return line.split("[")[0], line.split("==")[1]
    if "==" in line:
        return line.split("==")[0], line.split("==")[1]
    elif ">=" in line:
        return line.split(">=")[0], line.split(">=")[1]
    elif "<=" in line:
        return line.split("<=")[0], line.split("<=")[1]
    else:
        return line, None


def find_new_version(pkg_name):
    result = subprocess.run(
        [sys.executable, "-m", "pip", "index", "versions", pkg_name],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        versions = result.stdout.splitlines()
        if len(versions) > 3:
            return versions[3].split()[-1]
    return None


def upgrade_packages_in_file(tag_old_version=False):
    new_requirements = ""

    with open(filename, "r") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if not line.strip() or line.startswith("#"):
                new_requirements += line
                continue

            name, version = get_package_current_version(line)

            replace_version = find_new_version(name) + (
                f" #old: {version}" if tag_old_version else "\n"
            )
            new_line = line.replace(version, replace_version)
            new_requirements += new_line

            print(new_line, end="")

    open(filename, "w").write(new_requirements)


if __name__ == "__main__":
    upgrade_packages_in_file()
    print(f"All packages upgraded and {filename} updated!")
