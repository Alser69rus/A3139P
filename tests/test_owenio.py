from unittest import TestCase
from unittest.mock import Mock
from src.owenio import DI16, AI8


class TestDI16(TestCase):
    def setUp(self):
        self.port = Mock()
        self.port.execute.return_value = (0b0101010101010101,)
        self.di = DI16(port=self.port, dev=1, name='di', parent=None)

    def test_init(self):
        self.assertEqual(self.di.name, 'di')
        self.assertEqual(self.port, self.di.port)
        self.assertEqual(self.di.dev, 1)
        self.assertIs(self.di.parent(), None)
        self.assertEqual(self.di.value, [0] * 16)

    def test_read_data(self):
        self.assertEqual(self.di.read_data(), (0b0101010101010101,))

    def test_unpack_data(self):
        self.di.data = (0b0101010101010101,)
        self.assertEqual(self.di.unpack_data(), [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    def test_active(self):
        self.di.active = True
        self.assertEqual(self.di.active, True)

    def test_update(self):
        self.di.update()
        self.assertEqual(self.di.value, [0] * 16)
        self.di.active = True
        self.di.update()
        self.assertEqual(self.di.value, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        self.port.execute.return_value = Exception()
        self.di.update()
        self.assertIsInstance(self.di.error, Exception)


class TestAI8(TestCase):
    def setUp(self):
        self.port = Mock()
        self.port.execute.return_value = (32768, 65535, 3, 4, 5, 6, 7, 8)
        self.ai = AI8(port=self.port, dev=1, name='ai', parent=None)

    def test_init(self):
        self.assertEqual(self.ai.name, 'ai')
        self.assertEqual(self.port, self.ai.port)
        self.assertEqual(self.ai.dev, 1)
        self.assertIs(self.ai.parent(), None)
        self.assertEqual(self.ai.value, [0] * 8)
        self.assertEqual(self.ai.k, [1] * 8)
        self.assertEqual(self.ai.off, [0] * 8)
        self.assertEqual(self.ai.eps, [1] * 8)

    def test_read_data(self):
        self.assertEqual(self.ai.read_data(), (32768, 65535, 3, 4, 5, 6, 7, 8))

    def test_unpack_data(self):
        self.ai.k = [1, 2, 3, 4, 5, 6, 7, 8]
        self.ai.off = [0, 1, 2, 3, 4, 5, 6, 7]
        self.ai.data = (1, 2, 3, 4, 5, 6, 7, 8)
        self.assertEqual(self.ai.unpack_data(), [1.0, 5.0, 11.0, 19.0, 29.0, 41.0, 55.0, 71.0])

    def test_active(self):
        self.ai.active = True
        self.assertEqual(self.ai.active, True)

    def test_update(self):
        self.ai.update()
        self.assertEqual(self.ai.value, [0] * 8)
        self.ai.active = True

        self.ai.update()

        self.assertEqual(self.ai.value, [0, -1, 3, 4, 5, 6, 7, 8])
        self.port.execute.return_value = Exception()
        self.ai.update()
        self.assertIsInstance(self.ai.error, Exception)

