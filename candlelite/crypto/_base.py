from candlelite.io import load, path, save
from typing import Union, Literal
import datetime
import numpy as np
from paux.param import to_local


class IO():
    CANDLE_DATE_BASE_DIR: str
    CANDLE_FILE_BASE_DIR: str
    TIMEZONE: str
    BAR: str

    # 获取candle具备数据的日期序列
    def get_candle_dates(
            self,
            instType: str,
            symbol: str,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return path.get_candle_dates(**to_local(locals()))

    # 获取全部的产品名称
    def get_symbols_all(
            self,
            instType: str,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return path.get_symbols_all(**to_local(locals()))

    # 加载一个产品已有的全部K线
    def load_candle_all(
            self,
            instType: str,
            symbol: str,
            base_dir: str = None,
            start: Union[int, float, str, datetime.date] = None,
            end: Union[int, float, str, datetime.date] = None,
            columns: list = [],
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
    ):
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return load.load_candle_all(**to_local(locals()))

    # 加载全部产品已有的K线
    def load_candle_map_all(
            self,
            instType: str,
            base_dir: str = None,
            symbols: list = [],
            endswith: str = '',
            contains: str = '',
            start: Union[int, float, str, datetime.date] = None,
            end: Union[int, float, str, datetime.date] = None,
            timezone: str = None,
            p_num: int = 1,
            columns: list = [],
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
    ):
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return load.load_candle_map_all(**to_local(locals()))

    # 读取从start~end日期的历史K线数据
    def load_candle_by_date(
            self,
            instType: str,
            symbol: str,
            start: Union[int, float, str, datetime.date],
            end: Union[int, float, str, datetime.date],
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
            columns: list = [],
            valid_interval: bool = True,
            valid_start: bool = True,
            valid_end: bool = True,
    ) -> np.ndarray:
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return load.load_candle_by_date(**to_local(locals()))

    # 按照日期读取candle_map
    def load_candle_map_by_date(
            self,
            instType: str,
            symbols: list,
            start: Union[int, float, str, datetime.date],
            end: Union[int, float, str, datetime.date],
            base_dir: str=None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
            columns: list = [],
            endswith: str = '',
            contains: str = '',
            p_num: int = 1,
            valid_interval: bool = True,
            valid_start: bool = True,
            valid_end: bool = True,
    ) -> dict:
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return load.load_candle_map_by_date(**to_local(locals()))

    # 通过文件地址读取Candle
    def load_candle_by_file(
            self,
            instType: str,
            symbol: str,
            columns: list = [],
            path: str = None,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
            valid_interval: bool = True,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_FILE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return load.load_candle_by_file(**to_local(locals()))

    # 通过文件夹地址读取Candle_map
    def load_candle_map_by_file(
            self,
            instType: str,
            symbols: list = [],
            columns=[],
            path: str = None,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
            valid_interval: bool = True,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_FILE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return load.load_candle_map_by_file(**to_local(locals()))

    # 按照日期保存Candle
    def save_candle_by_date(
            self,
            candle: np.array,
            instType: str,
            symbol: str,
            start: Union[int, float, str, datetime.date],
            end: Union[int, float, str, datetime.date],
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
            replace: bool = True,
            drop_duplicate: bool = True,
            sort: bool = True,
            valid_interval: bool = True,
            valid_start: bool = True,
            valid_end: bool = True,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return save.save_candle_by_date(**to_local(locals()))

    # 按照日期保存candle_map
    def save_candle_map_by_date(
            self,
            candle_map: dict,
            instType: str,
            symbols: list,
            start: Union[int, float, str, datetime.date],
            end: Union[int, float, str, datetime.date],
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
            drop_duplicate: bool = True,
            replace: bool = True,
            sort: bool = True,
            valid_interval: bool = True,
            valid_start: bool = True,
            valid_end: bool = True,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return save.save_candle_map_by_date(**to_local(locals()))

    # 按照文件地址保存Candle
    def save_candle_by_file(
            self,
            candle: np.array,
            instType: str,
            symbol: str,
            path: str = None,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
            replace: bool = True,
            sort=True,
            drop_duplicate=True,
            valid_interval=True,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_FILE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return save.save_candle_by_file(**to_local(locals()))

    # 按照文件地址保存Candle_map
    def save_candle_map_by_file(
            self,
            candle_map: dict,
            instType: str,
            symbols: list,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
            replace: bool = True,
            sort: bool = True,
            drop_duplicate: bool = True,
            valid_interval: bool = True,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_FILE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return save.save_candle_map_by_file(**to_local(locals()))

    # 获取某一个天candle的路径
    def get_candle_date_path(
            self,
            instType: str,
            symbol: str,
            date: datetime.date,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return path.get_candle_date_path(**to_local(locals()))

    # 获取candle文件的地址（一般不以天切割，必须缓存数据与1d数据可以储存在一个文件中）
    def get_candle_file_path(
            self,
            instType: str,
            symbol: str,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_FILE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return path.get_candle_file_path(**to_local(locals()))

    # 检查candle从start到end日期数据文件是否齐全（仅检查文件是否存在，并不验证文件的准确性）
    def check_candle_date_path(
            self,
            instType: str,
            symbol: str,
            start: Union[int, float, str, datetime.date],
            end: Union[int, float, str, datetime.date],
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_DATE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return path.check_candle_date_path(**to_local(locals()))

    # 检查candle文件是否存在（不验证数据的准确性）
    def check_candle_file_path(
            self,
            instType: str,
            symbol: str,
            base_dir: str = None,
            timezone: str = None,
            bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = None,
    ):
        if base_dir == None:
            base_dir = self.CANDLE_FILE_BASE_DIR
        if timezone == None:
            timezone = self.TIMEZONE
        if bar == None:
            bar = self.BAR
        return path.check_candle_file_path(**to_local(locals()))
