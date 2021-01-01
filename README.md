<h1 align="center">Arma 3 Workshop Cleaner</h1>
<p align="center">Unsubscribes from addons that aren't in any installed modlists.</p>
<p align="center"><img src=https://i.imgur.com/plbQJff.gif width="70%" /></p>

I ran into a lot of trouble with disk space after having to switch out modlists for short campaigns with wildly different themes, so I made this.
It finds all the currently-installed addons, compares them to the contents of each modlist, and unsubscribes from any mods that aren't in any of them. Simple.

**This will only unsubscribe from addons**. I have made an effort to avoid missions since they're nice to keep around and don't take up too much extra space.

It also assumes that you:
1. are running Windows, and
2. have Steam installed under `C:\Program Files (x86)\Steam\`

It will try to automatically find where your Arma 3 install is based on `steamapps/libraryfolders.vdf` in your initial Steam install folder.

# Installation
Clone the repo (as below) or [download it as a zip](https://github.com/thomotron/arma-3-workshop-cleaner/archive/master.zip) and extract it somewhere:
```sh
git clone https://github.com/thomotron/arma-3-workshop-cleaner.git
```

Install the dependencies with pip:
```sh
python -m pip install -Ur requirements.txt
```

# Usage
Run the script:
```sh
python main.py
```

It will prompt you for your Steam username, password, and optionally Steam Guard code. This is to authorise it to unsubscribe from items on the workshop.
