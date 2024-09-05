# Preseed

## Overview
preseed.cfg and preseedmini.cfg do the exact same things, with one big exception:the latter does not install any packages at all, not even a desktop environment. This is mainly used for testing the installation process iteself, as it is much speedier than installing a lot of packages.

## Usage
1. At the Kali boot menu, press the 'tab' key.
2. Edit the command line and replace these boot parameters
```
preseed/url=/cdrom/simple-cdd/default.preseed simple-cdd/profiles=kali,offline desktop=xfce
```
with
```
auto=true url=https://raw.githubusercontent.com/FatEarthler/kali-preseed/main/preseed.cfg priority=critical
```

## Resources:
- <https://www.linuxjournal.com/content/preseeding-full-disk-encryption>
- <https://superuser.com/questions/1730951/debian-11-preseed-with-luks-and-lvm>
- <https://wikitech.wikimedia.org/wiki/PartMan>
- <https://unix.stackexchange.com/questions/556413/how-do-i-set-mirrors-in-etc-apt-sources-list-with-a-debian-preseed-file>


## TODOS:
- add nuke password
- create proper user, and hash the passwords
- user proper disk enryption password and hash it
- uuaa alias
  ```bash
  alias uuaa='echo -e "\e[1;31;40m***********************\\n--- sudo apt update ---\\n***********************\e[0" && sudo apt update && \
                echo -e "\e[1;31;40m********************************\\n--- sudo apt full-upgrade -y ---\\n********************************\e[0" && sudo apt full-upgrade -y && \
                echo -e "\e[1;31;40m******************************\\n--- sudo apt autoremove -y ---\\n******************************\e[0" && sudo apt autoremove -y && \
                echo -e "\e[1;31;40m**************************\\n--- sudo apt autoclean ---\\n**************************\e[0" && sudo apt autoclean'
  
  ``` 
- zsh as default shell for users
- for VM installations, ensure virtualbox guest additions and utils are installed

### DONE, testing required
- ...

### DONE
- rename files for easier boot-parameter modification
- create a minimal installation preseed file (don't install any packages). this should be used for testing purposes, when you want to minimize installation duration
- automated, forced GRUB installation
- ensure that /etc/apt/sources.list contains the following content:
	```
	# See https://www.kali.org/docs/general-use/kali-linux-sources-list-repositories/
	deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware
	
	# Additional line for source packages
	# deb-src http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware
	```

# Custom ISO
TODOS:
- hybrid: live & install
   * might be achievable using both the --live and --installer flags ``` ./build.sh --verbose --live --installer ```
   * might be that with the --live build, you can still install a default kali and just use preseeding for configuration
- maybe use 'netinstaller' installer version, so you always get the latest packages from kali-rolling
- VirtualBox Guest additions
  ```
  virtualbox-guest-utils/kali-rolling
  virtualbox-guest-x11/kali-rolling
  virtualbox-guest-dkms (really? at least under Windows, the two above seem to suffice for VirtualBox under Windows. Source: https://live-team.pages.debian.net/live-manual/html/live-manual/the-basics.en.html#testing-iso-with-virtualbox)
  ```
- uuaa alias
  ```bash
  alias uuaa='echo -e "\e[1;31;40m***********************\\n--- sudo apt update ---\\n***********************\e[0" && sudo apt update && \
                echo -e "\e[1;31;40m********************************\\n--- sudo apt full-upgrade -y ---\\n********************************\e[0" && sudo apt full-upgrade -y && \
                echo -e "\e[1;31;40m******************************\\n--- sudo apt autoremove -y ---\\n******************************\e[0" && sudo apt autoremove -y && \
                echo -e "\e[1;31;40m**************************\\n--- sudo apt autoclean ---\\n**************************\e[0" && sudo apt autoclean'
  
  ```  
- live mode with encrypted persistence
- installation disk encryption
- include aboves preseed (check for conflicts!)
- zsh as default bash
- disable NetworkManager and setup ifupdown
- auto Tor over VPN
- firewall setup to block outgoing traffic to tracker and add sites (do some research first how to properly block ads and trackers using netfilter)
