#!/bin/python
# arch_install

import getopt, sys

menu_points = ['Add Office', 'Add Dev Tools', 'Configure Remote Help', 'DO IT!!!']
added_menu_points = []

programs_to_install = ['tmux', 'htop', 'vim', 'grub']


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


def ask_for_choice():
	is_valid = False
	while not is_valid:
		try:
			choice = int(input('Enter choice [1-%i] : ' % menu_points.__len__())) - 1  # "- 1" -> zero based indexing
			is_valid = True
		except ValueError as e:
			print("%s is not a valid integer." % e.args[0].split(": ")[1])
	return choice


def print_menu():
	print('Menu')
	for i in range(menu_points.__len__()):
		print('%i) %s' % (i + 1, menu_points[i]))


def add_programs(programs_to_add):
	for program in programs_to_add:
		programs_to_install.append(program)


def remove_programs(programs_to_remove):
	for program in programs_to_remove:
		programs_to_install.remove(program)


def choose_menu_options():
	choice = ask_for_choice()

	if choice == menu_points.index('Add Office'):
		office_programs = ['libreoffice-fresh', 'libreoffice-fresh-de']

		if added_menu_points.count(menu_points[choice]) == 0:
			print('Adding %s...' % menu_points[choice])
			added_menu_points.append(menu_points[choice])
			add_programs(office_programs)

		else:
			print('%s already added!' % menu_points[choice])
			if ask_for_continue('Remove?', False):
				added_menu_points.remove(menu_points[choice])
				remove_programs(office_programs)
		choose_menu_options()

	elif choice == menu_points.index('Add Dev Tools'):
		dev_tools = []

		if added_menu_points.count(menu_points[choice]) == 0:
			print('Adding %s...' % menu_points[choice])
			added_menu_points.append(menu_points[choice])
			add_programs(dev_tools)

		else:
			print('%s already added!' % menu_points[choice])
			if ask_for_continue('Remove?', False):
				added_menu_points.remove(menu_points[choice])
				remove_programs(dev_tools)
		choose_menu_options()

	elif choice == menu_points.index('Configure Remote Help'):
		if added_menu_points.count(menu_points[choice]) == 0:
			print('Setting option configure Remote Help...')
			added_menu_points.append(menu_points[choice])
		# TODO

		else:
			print('Option configure Remote Help already set!')
			if ask_for_continue('Remove?', False):
				added_menu_points.remove(menu_points[choice])
			# TODO
		choose_menu_options()

	elif choice == menu_points.index('DO IT!!!'):
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
	except getopt.GetoptError as err:
		print(str(err))  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	for o, a in opts:
		if o in ('-v', 'version'):
			print('1.0.0')
		elif o in ('-h', '--help'):
			usage()
			sys.exit()
		else:
			assert False, 'unhandled option'

	print_menu()
	choose_menu_options()


if __name__ == '__main__':
	main()
