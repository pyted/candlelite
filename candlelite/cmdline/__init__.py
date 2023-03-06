import sys


def cmd():
    msg_fmt = '{cmd:<30}{note}'
    command = sys.argv[1]
    if command == '--help':
        msgs = [
            msg_fmt.format(cmd='candlelite show_settings', note='Current settings file information'),
            msg_fmt.format(cmd='candlelite console_settings', note='Modify the settings file in the terminal'),
            msg_fmt.format(cmd='candlelite settings_path', note='Get settings file path'),
        ]
        print('\n'.join(msgs))
    elif command == 'show_settings':
        from candlelite.settings import show_settings
        show_settings()
    elif command == 'console_settings':
        from candlelite.settings import console_settings
        console_settings()
    elif command == 'settings_path':
        from candlelite.settings import get_settings_filepath
        print(get_settings_filepath())
    else:
        pmt = 'Error command. You can input [candlelite --help] to view the supported commands'
        print(pmt)
