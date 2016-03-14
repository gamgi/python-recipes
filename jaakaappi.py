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
  def lataaJaakaappi( self, buf):
    line = buf.readline()
    line_s = line.split(' ')
    if (line_s[0] != 'Jääkaappitiedosto'):
      raise BufferError('File format not jääkaappi-format')
      return False
    while (line):
      print( line)
      line = buf.readline()


""" UNIT TESTS """
class Test( unittest.TestCase):
  #dummy test
  def test_testing( self):
    self.assertEqual( True, True)

  #test header
  def test_header( self):
    test_data = u"Moromoro versio 1.0\n"
    self.input_file = StringIO(test_data)
    kaappi = JaaKaappi()
    self.assertRaises(BufferError, kaappi.lataaJaakaappi,self.input_file)


  def test_loading( self):
    test_data = u"Jääkaappitiedosto versio 1.0\n"\
      + u"# Matin jääkaappi\n"\
      + u"JÄÄKAAPIN SISÄLTÖ\n"\
      + u"Maito\t1\tpurkki\ta\t10dl\tVL\3.4.2016"
    self.input_file = StringIO(test_data)
    kaappi = JaaKaappi()
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()

    self.assertNotEqual(None, kaappi.listaaKaikki(), "Loading data failed.")
if __name__ == '__main__':
  unittest.main()
