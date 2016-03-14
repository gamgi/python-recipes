import unittest
from io import StringIO

class ruokaAines:
  dikreetti = False
  yksikko = None
  allergiat = []
  nimi = None
  def __init__( self, nimi):
    self.name = nimi



class JaaKaappi:
  """ Luokka ruoka-aineiden säilytykselle"""
  ruokaAineet = []
  def listaaKaikki( self):
    print("Jääkaapin sisältö:")
    for aines in self.ruokaAineet:
      print( aines)
  def lataaJaakaappi( self, tiedosto):
    pass

""" UNIT TESTS """
class Test( unittest.TestCase):
  #dummy test
  def test_testing( self):
    self.assertEqual( True, True)

  def test_loading( self):
    test_data = u"Jääkaappitiedosto versio 1.0"\
      + u"# Matin jääkaappi"\
      + u"JÄÄKAAPIN SISÄLTÖ"\
      + u"Maito\t1\tpurkki\ta\t10dl\tVL\3.4.2016"
    self.input_file = StringIO(test_data)
    kaappi = JaaKaappi()
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except CorruptedChessFileError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()

    self.assertNotEqual(None, kaappi.listaaKaikki(), "Loading data failed.")
if __name__ == '__main__':
  unittest.main()
