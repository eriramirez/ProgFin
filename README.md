# ProgFin
Financial modeling course in Python


## Setting up the environment
For creating code we need to set up the computer with a few programs that will allow us to code more effectively. We will install the following software.

### Windows Subsystem for Linux (WSL)
Allows us to use a Linux OS in the background. Linux is more commonly used used among developers and some of the tools are easier achieve on linux. We will install Ubuntu, the most common distribution for linux.
Follow this step only if you have Windows. MacOS is already well suited for our purposes.

1. Open `Powershell` as administrator and run the following command.
    ```
    wsl --install
    ```


### Git
Version control of our files.
```
git config --global user.email "cuenta.personal@gmail.com"
git config --global user.name "github_username"
```


### Conda
Python environments
1. Download installer from
1. After installing run the following command 
    ```
    conda init bash
    ```
1. close the terminal and open it again
1. create a new python environment
    ```
    conda create -n progfin python=3.9 jupyter
    conda activate progfin
    ```

### VSCode
IDE for modifying files, use git and run our programs.

Install extensions
  - Python

Configure default terminal to be bash or ubuntu