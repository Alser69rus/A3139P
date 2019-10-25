import unittest

loader = unittest.TestLoader()
test = loader.discover('tests')
runner = unittest.TextTestRunner(verbosity=2)
runner.run(test)
