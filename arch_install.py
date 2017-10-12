#!/bin/python
# arch_install

import getopt
import subprocess
import sys

main_menu_points = ['Add WIFI', 'Add Office', 'Add Dev Tools', 'Configure Remote Help', 'DO IT!!!']
dev_tools = ['jdk8-openjdk', 'jdk9-openjdk', 'jdk', 'jetbrains-toolbox']

gnome = []
gnome_extra = []

added_menu_points = []

programs_to_install = ['htop', 'grub']

# Settings
install_path = None
efi_install = False

# Errors
ERR_NO_INSTALL_PATH = 2
ERR_SYS_NOT_EFI = 3
ERR_WRONG_ARGUMENT_OPTION = 10


def ask_for_continue(prompt, default_yes):
	if default_yes:
		user_input = input(prompt + ' [Y/n] ')
		if user_input in ('Y', 'y', ''):
			return True
	else:
		user_input = input(prompt + ' [y/N] ')
		if user_input in ('N', 'n', ''):
			return False
		else:
			return True

	return False


def ask_for_choice(points):
	is_valid = False
	while not is_valid:
		try:
			choice = int(input('Enter choice [1-%i] : ' % points.__len__())) - 1  # "- 1" -> zero based indexing
			is_valid = True
		except ValueError as e:
			print("%s is not a valid integer." % e.args[0].split(": ")[1])
	return choice


def print_menu_points(points):
	print('Menu')
	for i in range(points.__len__()):
		print('%i) %s' % (i + 1, points[i]))


def add_programs(programs_to_add):
	for program in programs_to_add:
		programs_to_install.append(program)


def remove_programs(programs_to_remove):
	for program in programs_to_remove:
		programs_to_install.remove(program)


def choose_options(menu_points):
	menu_points.append('Back..')
	choice = ask_for_choice(menu_points)

	if menu_points[choice] == 'Back..':
		print_menu_points(main_menu_points)
		return

	elif added_menu_points.count(menu_points[choice]) == 0:
		print('Adding %s...' % menu_points[choice])
		added_menu_points.append(menu_points[choice])
		add_programs([menu_points[choice]])

	else:
		print('%s already added!' % dev_tools[choice])
		if ask_for_continue('Remove?', False):
			print('Removing %s...' % dev_tools[choice])
			added_menu_points.remove(dev_tools[choice])
			remove_programs([dev_tools[choice]])

	menu_points.remove('Back..')
	choose_options(menu_points)


def option_menu(menu_points):
	print_menu_points(menu_points)
	choose_options(menu_points)


def choose_menu_options():
	choice = ask_for_choice(main_menu_points)

	if choice == main_menu_points.index('Add WIFI'):
		wifi_tools = ['iw', 'wireless_tools', 'wpa_supplicant', 'wifi-menu', 'dialog']

		if added_menu_points.count(main_menu_points[choice]) == 0:
			print('Adding %s...' % main_menu_points[choice])
			added_menu_points.append(main_menu_points[choice])
			add_programs(wifi_tools)

		else:
			print('%s already set!' % main_menu_points[choice])
			if ask_for_continue('Remove?', False):
				print('Removing %s...' % main_menu_points[choice])
				added_menu_points.remove(main_menu_points[choice])
				remove_programs(wifi_tools)

		choose_menu_options()

	elif choice == main_menu_points.index('Add Office'):
		office_programs = ['libreoffice-fresh', 'libreoffice-fresh-de']

		if added_menu_points.count(main_menu_points[choice]) == 0:
			print('Adding %s...' % main_menu_points[choice])
			added_menu_points.append(main_menu_points[choice])
			add_programs(office_programs)

		else:
			print('%s already set!' % main_menu_points[choice])
			if ask_for_continue('Remove?', False):
				print('Removing %s...' % main_menu_points[choice])
				added_menu_points.remove(main_menu_points[choice])
				remove_programs(office_programs)

		choose_menu_options()

	elif choice == main_menu_points.index('Add Dev Tools'):
		option_menu(dev_tools)

		choose_menu_options()

	elif choice == main_menu_points.index('Configure Remote Help'):
		if added_menu_points.count(main_menu_points[choice]) == 0:
			print('Setting option configure Remote Help...')
			added_menu_points.append(main_menu_points[choice])
		# TODO

		else:
			print('Option configure Remote Help already set!')
			if ask_for_continue('Remove?', False):
				added_menu_points.remove(main_menu_points[choice])
			# TODO

		choose_menu_options()

	elif choice == main_menu_points.index('DO IT!!!'):
		print(programs_to_install)
		install()

	else:
		print('No such option available.')
		choose_menu_options()


def install():
	print(2 * '\n' + 'Installing...\n')

	if efi_install:
		if subprocess.Popen(['ls', '/sys/firmware/efi/efivars'], stdout=subprocess.PIPE).returncode != 0:
			print('System is not booted in EFI-mode!')
			sys.exit(ERR_SYS_NOT_EFI)

	subprocess.call('dhcpcd', shell=True)
	proc = subprocess.Popen(['ping', '-c', '4', 'google.de'], stdout=subprocess.PIPE)

	subprocess.call(
		'wget -O /tmp/mirrorlist "https://www.archlinux.org/mirrorlist/?country=DE&protocol=http&protocol=https&ip_version=4"',
		shell=True)
	subprocess.call('sed -i \'s/^#Server/Server/\' /etc/pacman.d/mirrorlist.backup', shell=True)
	subprocess.call('rankmirrors -n 16 /tmp/mirrorlist > /etc/pacman.d/mirrorlist', shell=True)
	subprocess.call('pacstrap %s base base-devel tmux vim' % install_path, shell=True)

	subprocess.call(['cp', '/etc/pacman.conf', '/tmp/'], stdout=subprocess.PIPE)
	file = open('/tmp/pacman.conf', 'a')
	file.write('[archlinuxfr]\nSigLevel = Never\nServer = http://repo.archlinux.fr/$arch')
	file.close()

	subprocess.call('pacman --config /tmp/pacman.conf -r %s -Sy yaourt' % install_path, shell=True)

	programs = ''
	for program in programs_to_install:
		programs += ' ' + program
	print(programs)
	run_chroot_command('yaourt --noconfirm -Sayu %s' % programs)

	file = open(install_path + '/etc/hostname', 'w')
	file.write(input('Please insert hostname:'))
	file.close()


def run_chroot_command(command):
	subprocess.call('chroot ' + install_path + ' ' + command, shell=True)


def usage():
	print('usage: arch-install [OPTION] <install-path>')
	print('Convenient way to install Arch Linux. Must run on Arch Linux live USB!\n')

	print('  -e, --efi-install')
	print('  -h, --help')
	print('  -v, --version')

	print('\nReport Bugs to <http://github.com/crapStone/ArchInstaller/issues>.')


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'ehv', ['efi-install', 'help', 'version'])
	except getopt.GetoptError as e:
		print(str(e))
		usage()
		sys.exit(ERR_WRONG_ARGUMENT_OPTION)

	try:
		args[0]
	except IndexError as e:
		print('Please specify installation-path!\n')
		usage()
		sys.exit(ERR_NO_INSTALL_PATH)

	global install_path
	install_path = args[0]

	for o, a in opts:
		if o in ('-v', 'version'):
			print('1.0.0')

		elif o in ('-h', '--help'):
			usage()
			sys.exit()

		elif o in ('-e', '--efi-install'):
			global efi_install
			efi_install = True
			add_programs(['efibootmgr'])

		else:
			assert False, 'unhandled option'

	print_menu_points(main_menu_points)
	choose_menu_options()


if __name__ == '__main__':
	main()
