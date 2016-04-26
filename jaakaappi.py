import unittest
from io import StringIO
import ainekset
import re #regular expressions
#from ainekset import AinesParseError
#from ainekset import *



class JaaKaappi:
  """ Luokka ruoka-aineiden säilytykselle"""
  def __init__( self):
    self.ruokaAineet = []
  def listaaKaikki( self):
    print("Jääkaapin sisältö:")
    for aines in self.ruokaAineet:
      print( aines)
    return len(self.ruokaAineet) #returns nr of items


  def lataaJaakaappi( self, buf):
    #reset ruokaAineet
    self.ruokaAineet = []
    lukee = 'header'
    rivi = buf.readline()
    if (rivi.split()[0] != 'Jääkaappitiedosto'):
      raise BufferError('File format not jääkaappi-format, Must start with "Jääkaappitiedosto"')
      return False
    while (rivi):
      #print( rivi)
      #interpret headings
      otsikko = rivi.strip().upper()
      if (otsikko == "JÄÄKAAPIN SISÄLTÖ"):
        if( lukee != 'header'):
          raise BufferError('Order of jääkaappi-file should be header-defs-contents')
        lukee = 'contents'
        rivi = buf.readline()
      #depending on what we read, do differetn stuff
      if (lukee == 'contents'):
        try:
          uusi = self.parseLine(rivi)
          if (uusi):
            self.ruokaAineet.append( uusi)
        except AinesParseError as e:
          print('Error parsing :'+e.message)
      rivi = buf.readline()
  def parseLine( self, rivi):
    #one rivi can conatin many items (10 prk maioa ex)
    #parts = rivi.strip().split("\t")
    parts = re.split('\s+', rivi.rstrip().lower())
    aines = ainekset.ainesOsa( parts)
    return aines
    #print(parts)

  def onkoTuotetta( self, haettava):
    #print(self.ruokaAineet)
    for aines in self.ruokaAineet:
      if (aines.nimi == haettava.nimi):
        return True #TODO return amount
    return False

  def mitaPuuttuu( self, resepti):
    puuttuu = []
    for aines in resepti.ainekset:
      print(self.onkoTuotetta(aines.nimi))


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


  def test_loading_nofile( self):
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

    self.assertEqual(1, kaappi.listaaKaikki(), "Loading data failed.") #TODO uncomment

  def test_onkoTuotetta( self):
    test_data = u"Jääkaappitiedosto versio 1.0\n"\
      + u"# Matin jääkaappi\n"\
      + u"JÄÄKAAPIN SISÄLTÖ\n"\
      + u"Maito\t1\tpurkki\ta\t10dl\tVL\t3.4.2016\n"\
      + u"Sitruuna\t1\tkpl"
    self.input_file = StringIO(test_data)
    kaappi = JaaKaappi()
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()
    sipuli = ainekset.ruokaAines("sipuli")
    self.assertEqual(False, kaappi.onkoTuotetta( sipuli), "onkoTuotetta does not function as intended") 

    #Lisätään sipuli
    test_data += u"\nSipuli\t1\tkpl"
    self.input_file = StringIO(test_data)
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.assertEqual(True, kaappi.onkoTuotetta( sipuli), "onkoTuotetta does not function as intended") 

  def test_parseAllergy( self):
    test_data = "VL, G"
    ainekset.parsiAllergiat( test_data)
    #self.assertRaises(AinesParseError, parseAllergy, test_data)
    test_data = "P, Q"
    self.assertRaises(ainekset.AinesParseError, ainekset.parsiAllergiat, test_data)
if __name__ == '__main__':
  unittest.main()
