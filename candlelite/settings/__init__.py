import os

__all__ = [
    'get_settings_filepath',
    'save_settings',
    'init_settings',
    'read_settings',
    'show_settings',
    'console_settings'
]
# 配置文件编码，解决跨平台问题
ENCODING = 'UTF-8'
# 初始化的配置文件内容 key:[value,note]
INIT_DATA = {
    "CANDLE_BASE_DIR": ["'CANDLELITE_DATA'", '历史K线数据根目录'],

    "OKX_DATE_DIRNAME": ["'OKX'", 'OKX以日期为单位的存储目录'],
    "OKX_FILE_DIRNAME": ["'OKX_FILE'", 'OKX以文件为单位的存储目录'],
    "OKX_TIMEZONE": ["'Asia/Shanghai'", 'OKX的默认时区'],
    "OKX_DEFAULT_BAR": ["'1m'", 'OKX的默认时间粒度'],

    "BINANCE_DATE_DIRNAME": ["'BINANCE'", 'BINANCE以日期为单位的存储目录'],
    "BINANCE_FILE_DIRNAME": ["'BINANCE_FILE'", 'BINANCE以文件为单位的存储目录'],
    "BINANCE_TIMEZONE": ["'America/New_York'", 'BINANCE的默认时区'],
    "BINANCE_DEFAULT_BAR": ["'1m'", 'BINANCE的默认时间粒度'],

}


# 获取配置文件路径
def get_settings_filepath(filename: str = 'SETTINGS.config'):
    '''
    :param filename: 配置文件的名字
    :return: 配置文件路径
    '''
    dirpath = os.path.dirname(os.path.dirname(__file__))
    settings_path = os.path.join(dirpath, filename)
    return settings_path


# 保存到配置文件
def save_settings(data: dict, settings_path: str = None) -> None:
    content = ''
    for key, (value, note) in data.items():
        line = '# {note}\n{key} = {value}\n'.format(
            note=note,
            key=key,
            value=value,
        )
        content += line
    content = content.strip()
    if not settings_path:
        settings_path = get_settings_filepath()
    with open(settings_path, 'w', encoding=ENCODING) as f:
        f.write(content)


# 初始化配置文件
def init_settings(settings_path: str = None) -> None:
    save_settings(data=INIT_DATA, settings_path=settings_path)
    print('init settings complete')


# 读取配置文件
def read_settings(settings_path: str = None) -> dict:
    '''
    :param settings_path: 配置文件路径，不填写用默认
    :return: 配置文件字典 如果没有配置文件，会返回空字典
    '''
    if not settings_path:
        settings_path = get_settings_filepath()
    # 无文件 初始化文件
    if not os.path.isfile(settings_path):
        init_settings()
    with open(settings_path, 'r', encoding=ENCODING) as f:
        content = f.read().strip()
        content_list = content.split('#')
    data = {}
    for line in content_list:
        line = line.strip()
        if not line:
            continue
        note, kv = line.split('\n')
        k, v = kv.split('=')
        note = note.strip()
        k = k.strip()
        v = v.strip()
        if v.startswith("'") or v.startswith('"'):
            v = v[1:]
        if v.endswith("'") or v.endswith('"'):
            v = v[:-1]
        data[k] = [v, note]
    return data


# 展示配置文件内容
def show_settings(settings_path: str = None) -> None:
    if not settings_path:
        settings_path = get_settings_filepath()
    msg = f'settings_path={settings_path}\nYou can use a text editor to modify the settings file, or you can use candlelite.settings.console_settings to modify\n'
    print(msg)
    with open(settings_path, 'r', encoding=ENCODING) as f:
        content = f.read()
        print(content)


# 在终端中修改配置文件
def console_settings(settings_path: str = None) -> None:
    '''
    :param settings_path: 配置文件路径，不填写用默认
    '''
    setting = read_settings(settings_path)
    for keyword in setting.keys():
        while True:
            value = setting[keyword][0]
            note = setting[keyword][1]
            msg = f'#{note}\n{keyword}={value} (Y/N)'
            command = input(msg)
            if command.upper() == 'N':
                msg = f'{keyword}='
                command = input(msg).strip()
                # 转化为字符串格式，收尾添加引号
                if not command.startswith("'"):
                    command = "'" + command
                if not command.endswith("'"):
                    command = command + "'"
                setting[keyword][0] = command
                break
            elif command.upper() == 'Y':
                break
            else:
                msg = 'please enter Y (YES) or N (NO)'
                print(msg)
    save_settings(data=setting, settings_path=settings_path)
