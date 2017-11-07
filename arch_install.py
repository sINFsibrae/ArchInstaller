#!/bin/python
# arch_install

import getopt
import subprocess
import sys

# Settings
install_path = None
efi_install = False
editor = None

# Errors
ERR_NO_INSTALL_PATH = 2
ERR_SYS_NOT_EFI = 3
ERR_WRONG_ARGUMENT_OPTION = 10
ERR_PACSTRAP_FAILED = 11

# Programs
main_menu_points = ["Add WIFI", "Add Office", "Add Dev Tools", "Gnome", "Configure Remote Help", "DO IT!!!"]
dev_tools = ["jdk8-openjdk", "jdk9-openjdk", "jdk", "jetbrains-toolbox"]

gnome = ["adwaita-icon-theme", "baobab", "empathy", "eog", "evince", "gdm", "gnome-backgrounds", "gnome-calculator",
		 "gnome-contacts", "gnome-control-center", "gnome-dictionary", "gnome-disk-utility", "gnome-font-viewer",
		 "gnome-keyring", "gnome-screenshot", "gnome-session", "gnome-settings-daemon", "gnome-shell",
		 "gnome-shell-extensions", "gnome-system-monitor", "gnome-terminal", "gnome-themes-standard", "gnome-user-docs",
		 "gnome-user-share", "grilo-plugins", "gtk3-print-backends", "gucharmap", "gvfs", "gvfs-afc", "gvfs-goa",
		 "gvfs-google", "gvfs-gphoto2", "gvfs-mtp", "gvfs-nfs", "gvfs-smb", "mousetweaks", "mutter", "nautilus",
		 "networkmanager", "sushi", "tracker", "tracker-miners", "vino", "xdg-user-dirs-gtk", "yelp"]
gnome_extra = ["gnome-initial-setup", "bijiben", "brasero", "cheese", "dconf-editor", "evolution", "file-roller",
			   "gedit", "gedit-code-assistance", "gnome-calendar", "gnome-characters", "gnome-clocks",
			   "gnome-color-manager", "gnome-documents", "gnome-getting-started-docs", "gnome-logs", "gnome-nettool",
			   "gnome-photos", "gnome-todo", "gnome-tweak-tool", "gnome-weather", "nautilus-sendto", "polari", "rygel",
			   "seahorse", "vinagre"]

added_menu_points = []

programs_to_install = ["tmux", "htop", "grub"]


def exit_with_message(promt, status):
	print(promt)
	exit(status)


def exit(status):
	sys.exit(status)


def ask_for_continue(prompt, default_yes):
	if default_yes:
		user_input = input(prompt + " [Y/n]")
		if user_input in ("Y", "y", ""):
			return True
	else:
		user_input = input(prompt + " [y/N]")
		if user_input in ("N", "n", ""):
			return False
		else:
			return True

	return False


def ask_for_choice(points):
	is_valid = False
	while not is_valid:
		try:
			choice = int(input("Enter choice [1-%i] : " % points.__len__())) - 1  # "- 1" -> zero based indexing
			is_valid = True
		except ValueError as e:
			print("%s is not a valid integer." % e.args[0].split(": ")[1])
	return choice


def add_programs(programs_to_add):
	for program in programs_to_add:
		programs_to_install.append(program)


def remove_programs(programs_to_remove):
	for program in programs_to_remove:
		programs_to_install.remove(program)


def print_menu_points(points, message):
	print(message)
	lines = 25
	length = points.__len__()
	columns = range(round(length / lines))
	if length <= lines:
		rows = length
	else:
		rows = lines

	for i in range(rows):
		print("%i) %s" % (i + 1, points[i]), end="")
		for j in columns:
			if j > 0 and j * lines + i + 1 < length:
				print("%s %i) %s" % (
					(lines - points[j * i].__len__()) * " ", j * lines + i + 1, points[j * lines + i + 1]), end="")
		print()


def choose_options(menu_points):
	choice = ask_for_choice(menu_points)

	if choice > menu_points.__len__():
		print("No such option available.")
		choose_options(menu_points)

	elif menu_points[choice] == "Back..":
		return

	elif added_menu_points.count(menu_points[choice]) == 0:
		print("Adding %s..." % menu_points[choice])
		added_menu_points.append(menu_points[choice])
		add_programs([menu_points[choice]])

	else:
		print("%s already added!" % dev_tools[choice])
		if ask_for_continue("Remove?", False):
			print("Removing %s..." % dev_tools[choice])
			added_menu_points.remove(dev_tools[choice])
			remove_programs([dev_tools[choice]])

	choose_options(menu_points)


def option_menu(menu_points, prompt):
	menu_points.append("Back..")
	print_menu_points(menu_points, prompt)
	choose_options(menu_points)
	menu_points.remove("Back..")


def choose_menu_options():
	choice = ask_for_choice(main_menu_points)

	if choice == main_menu_points.index("Add WIFI"):
		wifi_tools = ["iw", "wireless_tools", "wpa_supplicant", "wifi-menu", "dialog"]

		if added_menu_points.count(main_menu_points[choice]) == 0:
			print("Adding %s..." % main_menu_points[choice])
			added_menu_points.append(main_menu_points[choice])
			add_programs(wifi_tools)

		else:
			print("%s already set!" % main_menu_points[choice])
			if ask_for_continue("Remove?", False):
				print("Removing %s..." % main_menu_points[choice])
				added_menu_points.remove(main_menu_points[choice])
				remove_programs(wifi_tools)

		choose_menu_options()

	elif choice == main_menu_points.index("Add Office"):
		office_programs = ["libreoffice-fresh", "libreoffice-fresh-de"]

		if added_menu_points.count(main_menu_points[choice]) == 0:
			print("Adding %s..." % main_menu_points[choice])
			added_menu_points.append(main_menu_points[choice])
			add_programs(office_programs)

		else:
			print("%s already set!" % main_menu_points[choice])
			if ask_for_continue("Remove?", False):
				print("Removing %s..." % main_menu_points[choice])
				added_menu_points.remove(main_menu_points[choice])
				remove_programs(office_programs)

		choose_menu_options()

	elif choice == main_menu_points.index("Add Dev Tools"):
		option_menu(dev_tools, "Dev Tools")

		print_menu_points(main_menu_points, "Main Menu")
		choose_menu_options()

	elif choice == main_menu_points.index("Gnome"):
		add_programs(gnome)
		add_programs(gnome_extra)

		for program in gnome:
			added_menu_points.append(program)

		for program in gnome_extra:
			added_menu_points.append(program)

		option_menu(gnome, "Gnome\nremove components")
		option_menu(gnome_extra, "Gnome Extras\nremove components")

		print_menu_points(main_menu_points, "Main Menu")
		choose_menu_options()

	elif choice == main_menu_points.index("Configure Remote Help"):
		if added_menu_points.count(main_menu_points[choice]) == 0:
			print("Setting option configure Remote Help...")
			added_menu_points.append(main_menu_points[choice])
		# TODO

		else:
			print("Option configure Remote Help already set!")
			if ask_for_continue("Remove?", False):
				added_menu_points.remove(main_menu_points[choice])
			# TODO

		choose_menu_options()

	elif choice == main_menu_points.index("DO IT!!!"):
		install()

	else:
		print("No such option available.")
		choose_menu_options()


def get_choice(prompt, choices):
	choices.append("Input own value..")

	print_menu_points(choices, prompt)
	choice = ask_for_choice(choices)

	if choices[choice] == "Input own value..":
		return input("Insert value")
	else:
		return choices[choice]


def run_command(command):
	subprocess.call(command, shell=True)


def run_chroot_command(command):
	run_command("chroot " + install_path + " " + command)


def setup_chroot():
	global mounts
	run_command("mount proc {}/proc -t proc -o nosuid,noexec,nodev".format(install_path))
	run_command("mount sys {}/sys -t sysfs -o nosuid,noexec,nodev,ro".format(install_path))
	run_command("mount udev {}/dev -t devtmpfs -o mode=0755,nosuid".format(install_path))
	run_command("mount devpts {}/dev/pts -t devpts -o mode=0620,gid=5,nosuid,noexec".format(install_path))
	run_command("mount shm {}/dev/shm -t tmpfs -o mode=1777,nosuid,nodev".format(install_path))
	run_command("mount run {}/run -t tmpfs -o nosuid,nodev,mode=0755".format(install_path))
	run_command("mount tmp {}/tmp -t tmpfs -o mode=1777,strictatime,nodev,nosuid".format(install_path))
	run_command("mount -B /etc/resolv.conf {}/etc/resolv.conf".format(install_path))

	mounts = "{0}/proc {0}/sys {0}/dev {0}/dev/pts {0}/dev/shm {0}/run {0}/tmp".format(install_path)

	if efi_install:
		run_command("mount efivars {}/sys/firmware/efi/efivars -t efivars -o nosuid,noexec,nodev".format(install_path))
		mounts += " {}/sys/firmware/efi/efivars".format(install_path)


def run_more_commands():
	if ask_for_continue(
			"Do you want to run custom commands before building the kernel?\nPress Ctrl+D to continue with installation.",
			True):
		run_command("/bin/zsh")


def install_bootloader():
	command = "grub-install --target="
	if efi_install:
		command.join("x86_64-efi --efi-directory=/boot/efi --bootloader-id=ArchLinux")
	else:
		command.join("i386-pc")

	run_chroot_command(command)
	run_chroot_command("grub-mkconfig -o /boot/grub/grub.cfg")


def tear_down_chroot():
	run_command("umount {}".format(mounts))


def install():
	print(2 * "\n" + "Installing...\n")

	if efi_install:
		if subprocess.run("ls /sys/firmware/efi/efivars").returncode != 0:
			exit_with_message("System is not booted in EFI-mode!", ERR_SYS_NOT_EFI)

	# run_command("dhcpcd")
	# proc = subprocess.run("ping -c 4 google.de", stdout=subprocess.PIPE)

	run_command(
		"wget -O /tmp/mirrorlist 'https://www.archlinux.org/mirrorlist/?country=DE&protocol=http&protocol=https&ip_version=4'")
	run_command("sed -i \"s/^#Server/Server/\" /tmp/mirrorlist")
	print("Ranking mirrors...")
	run_command("rankmirrors -n 16 /tmp/mirrorlist > /etc/pacman.d/mirrorlist")
	if subprocess.run("pacstrap {} base base-devel vim".format(install_path), shell=True).returncode != 0:
		exit_with_message("pacstrap did not run correctly!", ERR_PACSTRAP_FAILED)

	setup_chroot()

	run_command("genfstab -U {0} >> {0}/etc/fstab".format(install_path))

	run_command("cp /etc/pacman.conf /tmp/")
	file = open("/tmp/pacman.conf", "a")
	file.write("[archlinuxfr]\nSigLevel = Never\nServer = http://repo.archlinux.fr/$arch")
	file.close()

	run_command("pacman --config /tmp/pacman.conf --noconfirm -r {} -Sy yaourt".format(install_path))

	programs = ""
	for program in programs_to_install:
		programs += " " + program
	run_chroot_command("yaourt --noconfirm -Sy {}".format(programs))

	timezones = ["Europe/Berlin"]

	localtime = get_choice("Select timezone:", timezones)
	run_command("ln -sf /usr/share/zoneinfo/{} /etc/localtime".format(localtime))

	run_command("hwclock --localtime --systohc")

	editors = ["vi", "vim", "nano"]
	global editor
	editor = get_choice("Select editor:", editors)

	input('Uncomment needed localizations in /etc/locale.gen.. (Press "Enter")')
	run_command(" {}/etc/locale.gen".format(editor + install_path))
	run_command("locale-gen")

	user_input = input("Please insert localization:")
	file = open(install_path + "/etc/locale.conf", "w")
	file.write("LANG=" + user_input)
	file.close()

	user_input = input("Please insert hostname:")
	file = open(install_path + "/etc/hostname", "w")
	file.write(user_input)
	file.close()

	keyboardlayout = ["de-latin1-nodeadkeys"]
	user_input = get_choice("Keyboardlayout", keyboardlayout)
	file = open(install_path + "/etc/vconsole.conf", "w")
	file.write("KEYMAP={}".format(user_input))
	file.close()

	run_more_commands()

	run_chroot_command("mkinitcpio -p linux")

	install_bootloader()

	print("Insert root password:")
	run_chroot_command("passwd")

	run_command("sync")

	tear_down_chroot()


def usage():
	print("usage: arch-install [OPTION] <install-path>")
	print("Convenient way to install Arch Linux. Must run in Arch Linux install environment!\n")

	print("  -e, --efi-install")
	print("  -h, --help")
	print("  -v, --version")

	print("\nReport Bugs to <http://github.com/crapStone/ArchInstaller/issues>.")


def main():
	subprocess.call("timedatectl set-ntp true", shell=True)
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ehv", ["efi-install", "help", "version"])
	except getopt.GetoptError as e:
		print(str(e))
		usage()
		exit(ERR_WRONG_ARGUMENT_OPTION)

	try:
		args[0]
	except IndexError as e:
		print("Please specify installation-path!\n")
		usage()
		exit(ERR_NO_INSTALL_PATH)

	global install_path
	install_path = args[0]

	for o, a in opts:
		if o in ("-v", "version"):
			print("1.0.0")

		elif o in ("-h", "--help"):
			usage()
			exit(0)

		elif o in ("-e", "--efi-install"):
			global efi_install
			efi_install = True
			add_programs(["efibootmgr"])

		else:
			assert False, "unhandled option"

	print(install_path)

	print_menu_points(main_menu_points, "Main Menu")
	choose_menu_options()


if __name__ == "__main__":
	main()
