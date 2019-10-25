from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class ObjectType(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


class DeviceType(ObjectType):
    error = pyqtSignal(str)
    warning = pyqtSignal(str)
    updated = pyqtSignal()

    def __init__(self, port, address: int = 1, retries: int = 3, parent=None):
        super().__init__(parent=parent)
        self.vendor_name: str = ''
        self.model_name: str = ''
        self.firmware_version: str = ''
        self.application_software_version: str = '0.1'
        self.protocol_version: str = 'Modbus RTU'
        self.port = port
        self.address: int = address
        self.apdu_retries: int = retries
        self.retries: int = retries
        self.pin: list = []
        self.obj: dict = {}
        self.out_of_service: bool = False


class AnalogType(ObjectType):
    out_of_range = pyqtSignal(float)
    updated = pyqtSignal(float)
    change_of_value = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.value: float = 0
        self.min_value: float = 0
        self.max_value: float = 0
        self.low: float = 0
        self.high: float = 0
        self.engineering_unit: str = ''
        self.alarm: bool = False
        self.fault: bool = False
        self.out_of_service: bool = False
        self.resolution: int = 6
        self.frm_str = '{:f}'
        self.cov_increment: float = 0

    def textValue(self) -> str:
        return self.frm_str.format(self.value)

    def textValueWithUnit(self) -> str:
        return self.textValue() + ' ' + self.engineering_unit


class AnalogInputType(AnalogType):
    def __init__(self, min_value: float = 4, max_value: float = 20,
                 low: float = 0, high: float = 100, parent=None):
        super().__init__(parent=parent)
        self.min_value = min_value
        self.max_value = max_value
        self.low = low
        self.high = high
        self.value = self.low
        self.old_value = self.value

    @pyqtSlot(float)
    def setValue(self, value: float):
        if self.out_of_service:
            return

        self.value = (value - self.min_value) * (self.high - self.low) / (
                self.max_value - self.min_value) + self.low
        self.value = round(self.value, self.resolution)

        if self.min_value > value or value > self.max_value:
            self.out_of_range.emit(self.value)
        if abs(self.value - self.old_value) >= self.cov_increment:
            self.old_value = self.value
            self.change_of_value.emit(self.value)
        self.updated.emit(self.value)
