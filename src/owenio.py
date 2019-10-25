from PyQt5 import QtCore
from modbus_tk.modbus_rtu import RtuMaster
import modbus_tk.defines as cst
from typing import List, Tuple, Optional, Any, Union
import src.opcua as opcua
import logging
import asyncio

log = logging.getLogger('log')

VERSION = 2.0


def get_bit(value: int, n: int):
    if value is None: value = 0
    return (value >> n) & 1


def set_bit(value: int, n: int):
    if value is None: value = 0
    return (1 << n) | value


def reset_bit(value: int, n: int):
    if value is None: value = 0
    return (~(1 << n)) & value


def override_bit(value: int, n: int, bit_value):
    if bit_value:
        return OwenModule.set_bit(value, n)
    else:
        return OwenModule.reset_bit(value, n)


def to_signed32(n):
    n = n & 0xffffffff
    return n | (-(n & 0x80000000))


def to_signed16(n):
    n = n & 0xffff
    return n | (-(n & 0x8000))


class OwenModule(QtCore.QObject):
    updated = QtCore.pyqtSignal()
    warning = QtCore.pyqtSignal(str)

    def __init__(self, port: RtuMaster, dev: int, name: str = 'Owen module', parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)
        self.value: List[Any] = []
        self.data: Union[List[int], Tuple[int]] = []
        self.error: Optional[Exception] = None
        self.port: RtuMaster = port
        self.dev: int = dev
        self._active: bool = False
        self.name: str = name

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value


class OwenInputModule(OwenModule):
    def read_data(self) -> Tuple[int]:
        pass

    def unpack_data(self) -> list:
        pass

    def update(self):
        if self.active:
            try:
                self.data = self.read_data()
                self.value = self.unpack_data()
                self.updated.emit()
            except Exception as e:
                self.error = e
                self.warning.emit(f'{self.name} warning: {self.error} ,data: {self.data}')


class DI16(OwenInputModule):
    def __init__(self, port: RtuMaster, dev: int, name: str = 'DI16', parent: Optional[QtCore.QObject] = None):
        super().__init__(port=port, dev=dev, name=name, parent=parent)
        self.value = [0] * 16

    def read_data(self) -> Tuple[int]:
        return self.port.execute(self.dev, cst.READ_INPUT_REGISTERS, 51, 1)

    def unpack_data(self) -> List[int]:
        value = []
        for i in range(16):
            value.append(get_bit(self.data[0], i))
        return value


class AI8(OwenInputModule):
    def __init__(self, port: RtuMaster, dev: int, name: str = 'AI8', parent: Optional[QtCore.QObject] = None):
        super().__init__(port=port, dev=dev, name=name, parent=parent)
        self.value = [0] * 8
        self.k = [1] * 8
        self.off = [0] * 8
        self.eps = [1] * 8

    def read_data(self) -> Tuple[int]:
        return self.port.execute(self.dev, cst.READ_INPUT_REGISTERS, 256, 8)

    def unpack_data(self) -> List[float]:
        values = [to_signed16(i) for i in self.data]
        values = [values[i] * self.k[i] + self.off[i] if values[i] > -32768 else 0 for i in range(8)]
        return values


class AI8AC(opcua.DeviceType):
    def __init__(self, port, address: int, parent=None):
        super().__init__(port=port, address=address, parent=parent)
        self.pin = [opcua.AnalogInputType(4, 20, 0, 100, parent=self) for _ in range(8)]
        self.vendor_name = 'OWEN'
        self.model_name = 'MV110.8AC'

    async def update(self):
        res = await self.port.read_input_registers(256, 8, unit=self.address)
        if not res.isError():
            self.retries = self.apdu_retries
            for i in range(8):
                self.pin[i].setValue(res.registers[i])
        else:
            self.retries -= 1
            if self.retries:
                self.warning.emit(self.model_name + ' ' + str(res.function_code))
            else:
                self.error.emit(self.model_name + ' ' + str(res.function_code))

# class OwenOutputModule(OwenModule):
#     def __init__(self, port=None, dev=None, name=None, parent=None):
#         super().__init__(port=port, dev=dev, name=name, parent=parent)
#     @abstractmethod
#     def pack_data(self, data: List[Any]) -> List[int]:
#         pass
#
#     @abstractmethod
#     def write_data(self, pack: List[int]) -> bool:
#         pass
#
#     def update(self):
#         if self.active:
#             Maybe(self.value)(self._pack_data)(self._write_data)(self._read_data)(self._check_data)(self._emit_updated)(
#                 self._write_done).or_else(
#                 self._emit_warning)
#
#     def _emit_updated(self, data):
#         if self.active:
#             self.changed.emit()
#         self.updated.emit()
#         return data
#
#     def _write_done(self, data):
#         self.setActive(False)
#         return data
#
#     def setValue(self, value, n=-1):
#         if n >= 0:
#             self.value[n] = value
#         else:
#             self.value = value
#         self.setActive()
#
#
# class DI16(OwenInputModule):
#     def __init__(self, port=None, dev=None, name='DI', parent=None):
#         super().__init__(port=port, dev=dev, name=name, parent=parent)
#         self.value = [0] * 16
#
#     def _read_data(self, port):
#         return port.execute(self.dev, cst.READ_INPUT_REGISTERS, 51, 1)
#
#     def _unpack_data(self, pack):
#         value = []
#         for i in range(16):
#             value.append(bitwise.get(pack[0], i))
#         return value
#
#
# class AI8(OwenInputModule):
#     def __init__(self, port=None, dev=None, name='AI', parent=None):
#         super().__init__(port=port, dev=dev, name=name, parent=parent)
#         self.value = [0] * 8
#         self.k = [1] * 8
#         self.off = [0] * 8
#         self.eps = [1] * 8
#
#     def _read_data(self, port):
#         return port.execute(self.dev, cst.READ_INPUT_REGISTERS, 256, 8)
#
#     def _unpack_data(self, data):
#         values = [i if i < 32768 else 655536 - i for i in data]
#         values = [values[i] * self.k[i] + self.off[i] for i in range(8)]
#         values = [i if i != 32768 else None for i in values]
#         return values
#
#     def _emit_updated(self, values):
#         if any([abs(self.value[i] - values[i]) > self.eps[i] for i in range(8)]):
#             self.value = values
#             self.changed.emit()
#         self.updated.emit()
#         return values
#
#
# class DO32(OwenOutputModule):
#
#     def __init__(self, port=None, dev=None, name='DO', parent=None):
#         super().__init__(port=port, dev=dev, name=name, parent=parent)
#         self.value = [0] * 32
#
#     def _pack_data(self, data):
#         pack = [0, 0]
#         for i in range(16):
#             pack[0] = bitwise.override(pack[0], i, data[i + 16])
#             pack[1] = bitwise.override(pack[1], i, data[i])
#         return pack
#
#     def _write_data(self, pack):
#         self.thread().msleep(2)
#         return self.port.execute(self.dev, cst.WRITE_MULTIPLE_REGISTERS, 97, output_value=pack)
#
#     def _read_data(self, data):
#         self.thread().msleep(2)
#         return self.port.execute(self.dev, cst.READ_HOLDING_REGISTERS, 97, 2)
#
#     def _check_data(self, data):
#         v = [0] * 32
#         for i in range(16):
#             v[i] = bitwise.get(data[1], i)
#             v[i + 16] = bitwise.get(data[0], i)
#         if v == self.value:
#             return v
#         return None
#
#
# class AO8I(OwenOutputModule):
#
#     def __init__(self, port=None, dev=None, name='AO', parent=None):
#         super().__init__(port=port, dev=dev, name=name, parent=parent)
#         self.value = [0] * 8
#
#     def _pack_data(self, data):
#         return [int(i) for i in data]
#
#     def _write_data(self, data):
#         self.thread().msleep(2)
#         return self.port.execute(self.dev, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=data)
#
#     def _read_data(self, data):
#         self.thread().msleep(2)
#         v = self.port.execute(self.dev, cst.READ_HOLDING_REGISTERS, 0, 8)
#         return v
#
#     def _check_data(self, data):
#         if list(data) == self.value:
#             return data
#         return None
