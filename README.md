At the Kali boot menu, press <tab>.
Edit the command line and replace the below

	preseed/url=/cdrom/simple-cdd/default.preseed simple-cdd/profiles=kali,offline desktop=xfce
	
with

	auto=true url=https://raw.githubusercontent.com/FatEarthler/kali-preseed/main/preseed.cfg priority=critical


Resources:
https://www.linuxjournal.com/content/preseeding-full-disk-encryption
https://superuser.com/questions/1730951/debian-11-preseed-with-luks-and-lvm
https://wikitech.wikimedia.org/wiki/PartMan



TODOS:
- ensure that /etc/apt/sources.list contains the following content:
 	# See https://www.kali.org/docs/general-use/kali-linux-sources-list-repositories/
	deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware

	# Additional line for source packages
	# deb-src http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware
- add nuke password
- create proper user and hash the passwords
- hash the disk encryption password


DONE, testing required
- ...


DONE
- rename files for easier boot-parameter modification
- create a minimal installation preseed file (only minimal packages installed). this should be used for testing purposes, when you want to minimize installation duration
- automated, forced GRUB installation
