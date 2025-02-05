{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python312Packages;
in
pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pythonPackages.pip
    pythonPackages.virtualenv
  ];

  shellHook = ''
    echo -e "\033[33mCreating the python venv\033[0m"
    if [ ! -d ./.pythonlib/venv ]; then
      python -m venv ./.pythonlib/venv
    fi

    source ./.pythonlib/venv/bin/activate

    echo -e "\033[31mInstalling / updating requirements..\033[0m"
    pip install -r requirements.txt
    echo -e "\033[31mRequirements are installed!\033[0m"

    echo -e "\033[31mCreating .telescopeignore and .gitignore if not done already...\033[0m"

    # Function to check if a line exists in a file
    lineinfile() {
        local file="$1"
        local line="$2"
        
        if [ ! -f "$file" ]; then
            touch "$file"
        fi
        
        if ! grep -q -F "$line" "$file"; then
            echo "$line" >> "$file"
            echo -e "\033[31m    Added '$line' to $file\033[0m"
        else
            echo -e "\033[31m    '$line' already exists in $file, doing nothing."
        fi
    }

    # telescope
    lineinfile ".telescopeignore" "./.pythonlib/"

    # gitignore
    lineinfile ".gitignore" "./.pythonlib/"
    echo -e "\033[33m\nDone!\033[0m"
  '';
}
