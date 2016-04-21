import unittest
from io import StringIO
import ainekset
#from ainekset import AinesParseError
#from ainekset import *



class JaaKaappi:
  """ Luokka ruoka-aineiden säilytykselle"""
  ruokaAineet = []
  def listaaKaikki( self):
    print("Jääkaapin sisältö:")
    for aines in self.ruokaAineet:
      print( aines)
    return len(self.ruokaAineet) #returns nr of items
  def lataaJaakaappi( self, buf):
    reading = 'header'
    line = buf.readline()
    if (line.split()[0] != 'Jääkaappitiedosto'):
      raise BufferError('File format not jääkaappi-format, Must start with "Jääkaappitiedosto"')
      return False
    while (line):
      #print( line)
      #interpret headings
      command = line.strip().upper()
      if (command == "JÄÄKAAPIN SISÄLTÖ"):
        if( reading != 'header'):
          raise BufferError('Order of jääkaappi-file should be header-defs-contents')
        reading = 'contents'
        line = buf.readline()
      #depending on what we read, do differetn stuff
      if (reading == 'contents'):
        try:
          uusi = self.parseLine(line)
          if (uusi):
            self.ruokaAineet.append( uusi)
        except AinesParseError as e:
          print('Error parsing :'+e.message)
      line = buf.readline()
  def parseLine( self, line):
    #one line can conatin many items (10 prk maioa ex)
    parts = line.strip().split("\t")
    aines = ainekset.ainesOsa( parts)
    return aines
    #print(parts)


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
      + u"Maito\t1\tpurkki\ta\t10dl\tVL\t3.4.2016"
    self.input_file = StringIO(test_data)
    kaappi = JaaKaappi()
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()

    self.assertNotEqual(0, kaappi.listaaKaikki(), "Loading data failed.")


  def test_parseAllergy( self):
    test_data = "VL, G"
    ainekset.parseAllergy( test_data)
    #self.assertRaises(AinesParseError, parseAllergy, test_data)
    test_data = "P, Q"
    self.assertRaises(ainekset.AinesParseError, ainekset.parseAllergy, test_data)
if __name__ == '__main__':
  unittest.main()
