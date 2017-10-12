#!/bin/python
# arch_install

import getopt
import sys

main_menu_points = ['Add Office', 'Add Dev Tools', 'Configure Remote Help', 'DO IT!!!']
dev_tools = ['jdk8-openjdk', 'jdk9-openjdk', 'jdk', 'jetbrains-toolbox', 'Back..']
added_menu_points = []

programs_to_install = ['tmux', 'htop', 'vim', 'grub']

install_path = None
efi_install = False

ERR_NO_INSTALL_PATH = 2
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


def choose_dev_tools():
	choice = ask_for_choice(dev_tools)

	if dev_tools[choice] == "Back..":
		print_menu_points(main_menu_points)
		return

	elif added_menu_points.count(dev_tools[choice]) == 0:
		print('Adding %s...' % dev_tools[choice])
		added_menu_points.append(dev_tools[choice])
		add_programs([dev_tools[choice]])

	else:
		print('%s already added!' % dev_tools[choice])
		if ask_for_continue('Remove?', False):
			print('Removing %s...' % dev_tools[choice])
			added_menu_points.remove(dev_tools[choice])
			remove_programs([dev_tools[choice]])

	choose_dev_tools()


def choose_menu_options():
	choice = ask_for_choice(main_menu_points)

	if choice == main_menu_points.index('Add Office'):
		office_programs = ['libreoffice-fresh', 'libreoffice-fresh-de']

		if added_menu_points.count(main_menu_points[choice]) == 0:
			print('Adding %s...' % main_menu_points[choice])
			added_menu_points.append(main_menu_points[choice])
			add_programs(office_programs)

		else:
			print('%s already added!' % main_menu_points[choice])
			if ask_for_continue('Remove?', False):
				print('Removing %s...' % main_menu_points[choice])
				added_menu_points.remove(main_menu_points[choice])
				remove_programs(office_programs)

		choose_menu_options()

	elif choice == main_menu_points.index('Add Dev Tools'):
		print_menu_points(dev_tools)
		choose_dev_tools()

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
		print('DONE')
		print(programs_to_install)

	else:
		print('No such option available.')
		choose_menu_options()


def install():
	print(3 * '\n' + 'Installing...')


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
