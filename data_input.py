import abc
import copy
import csv
import json

from utils import check_host


class InputReadError(Exception):
    pass


class Reader(abc.ABC):
    """Default super class of all readers.

    This class will be used in case if you need to read input data from
    multiple source. e.g. CSV, EXCEL, JSON, TOML etc.

    """
    _connection_string: str = ''

    def __init__(self, *args):
        """Init for reader class.
        Every subclass must accept something like `source` as str
        """
        pass

    def get_validated_data(self) -> dict[int, dict]:
        """Function to separate valid and invalid data"""
        raise NotImplementedError

    def _read_all(self) -> list[dict]:
        """Function to read all data to process inside class"""
        raise NotImplementedError

    @classmethod
    def get_reader(cls, connection_string):
        """Returns reader for provided connection_string"""
        classes = cls.__subclasses__()
        try:
            con_type, source, *_ = connection_string.split(':')
        except ValueError:
            raise InputReadError(
                'Connection string must look like con_type:source.'
                ' For example: csv:./input.csv'
            )
        connector = [class_ for class_ in classes if
                     class_._connection_string == con_type]
        if len(connector) and con_type != '':
            return connector[0](source)
        else:
            raise InputReadError(f'Can\'t find datasource for '
                                 f'connection type {con_type}')

    @classmethod
    def get_all_protocols(cls):
        """Returns all available connection types"""
        classes = cls.__subclasses__()
        protocols = filter(None,
                           [class_._connection_string for class_ in classes])
        return list(protocols)

    @classmethod
    def read(cls, connection_string: str):
        reader = cls.get_reader(connection_string)
        return reader.get_validated_data()


class CsvReader(Reader):
    """Reads data from csv file. takes filename as input."""
    _connection_string = 'csv'

    def get_validated_data(self) -> dict[int, dict]:
        valid = []
        invalid = []
        if self._data is None:
            self._read_all()
        data = self._data[:]
        if self._title:
            data = self._data[1:]
        for idx, row in enumerate(data):  # type: int, list
            if not check_host(row[0]):
                invalid.append({
                    'host': row[0],
                    'ports': row[1].split(','),
                    'idx': idx
                })
                continue
            try:
                if row[1] == '':
                    valid.append({
                        'host': row[0],
                        'ports': [],
                        'idx': idx
                    })
                    continue
                ports = [int(port.strip()) for port in
                         row[1].strip().split(',')]
                valid.append({
                    'host': row[0],
                    'ports': ports,
                    'idx': idx
                })
            except (ValueError, IndexError):
                try:
                    invalid.append({
                        'host': row[0],
                        'ports': [row[1]],
                        'idx': idx
                    })
                except IndexError:
                    raise InputReadError('Csv is absolutely invalid.')
        res = {}
        for item in valid:
            res.update({item['idx']: {**item, 'valid': True}})
        for item in invalid:
            res.update({item['idx']: {**item, 'valid': False}})
        return res

    def _read_all(self, force_update: bool = False):
        """Reads data from csv file or returns already read if it already was"""
        if self._data is not None and not force_update:
            return copy.deepcopy(self._data)
        _reader = csv.reader(
            self.file,
            delimiter=self._delimiter,
            quotechar=self._quotechar
        )
        self._data = list(_reader)
        return copy.deepcopy(self._data)  # Return copy of read list.

    def __init__(self, filename: str, delimiter=';', quotechar='"',
                 encoding='utf-8', title: bool = True):
        super().__init__()  # unnecessary. Just for IDE
        self._data = None
        self._delimiter = delimiter
        self._quotechar = quotechar
        self._title = title
        try:
            self.filename = filename
            self.file = open(filename, encoding=encoding)
        except (FileNotFoundError, OSError) as exc:
            raise exc

    def __del__(self):
        """To be sure that file is closed.

        In CPython files closes automatically, but no one guarantee that this is
        will work in PyPy or IronPython. So we use __del__ to be sure that
        is True.

        """
        try:
            if self.file and not self.file.closed:
                self.file.close()
        except AttributeError:
            pass


class JsonReader(Reader):
    """Reads input from json.

    This class is same as CsvReader, but for json files. I added this
    just to show, how easily we can add more input types.
    (Я ЗНАЮ,ЧТО ДЛЯ ИСХОДНОГО ЗАДАНИЯ ЭТО НЕ ТРЕБОВАЛОСЬ)
    You just need to create new class. Reader.get_reader will handle the rest.

    """
    _connection_string = 'json'

    def get_validated_data(self) -> dict[int, dict]:
        """Separate valid and invalid data."""
        if self._data is None:
            self._read_all()
        valid = []
        invalid = []
        for idx, row in enumerate(self._data):  # type: int, dict
            if host := (row.get('host')):
                if not check_host(host):
                    invalid.append({
                        'host': host,
                        'ports': row.get('ports'),
                        'idx': idx
                    })
                    continue
                if ports := row.get('ports', []):
                    try:
                        ports = [int(port) for port in ports]
                        if len(ports) < 1:
                            invalid.append({
                                'host': host,
                                'ports': row.get('ports'),
                                'idx': idx
                            })
                            continue
                        valid.append({
                            'host': host,
                            'ports': ports,
                            'idx': idx
                        })
                    except ValueError:
                        invalid.append({
                            'host': host,
                            'ports': row.get('ports'),
                            'idx': idx
                        })
            else:
                invalid.append({
                    'host': '',
                    'ports': row.get('ports'),
                    'idx': idx
                })
        res = {}
        for item in valid:
            res.update({item['idx']: {**item, 'valid': True}})
        for item in invalid:
            res.update({item['idx']: {**item, 'valid': False}})
        return res

    def _read_all(self):
        pass
        if self._data is not None:
            return copy.deepcopy(self._data)
        try:
            self._data = json.load(self.file)
            if not isinstance(self._data, list):
                raise json.JSONDecodeError
            return copy.deepcopy(self._data)  # Return copy of read list.
        except json.JSONDecodeError as exc:
            raise InputReadError('Ошибка при считывании файла, json не валиден')

    def __init__(self, filename: str, encoding='utf-8'):
        super().__init__()
        try:
            self.filename = filename
            self.file = open(filename, encoding=encoding)
            self._data = None
        except (FileNotFoundError, OSError, json.JSONDecodeError) as exc:
            raise InputReadError('Ошибка при считывании файла, файл недоступен')

    def __del__(self):
        try:
            if self.file and not self.file.closed:
                self.file.close()
        except AttributeError:
            pass


if __name__ == '__main__':
    # Just simple tests.
    test_reader = Reader.get_reader('csv:input.csv')
    print(type(test_reader))
    print(*test_reader.get_validated_data(), sep='\n')
    del test_reader
