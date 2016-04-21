import unittest
#from io import StringIO
import errno
import glob
import re #regular expressions
import ainekset

class resepti:
  def __init__(self, nimi, annokset, ainekset, ohjeet):
    self.nimie = nimi
    self.annokset = annokset
    self.ainekset = ainekset
    self.ohjeet = ohjeet

class ReseptiKirja:
  """ Luokka reseptien säilytykselle"""
  # Receipes stored as touples in a set: set(("Milk", "1dl"), ("Sugar", "1tbsp"))
  reseptit = set()
  def lataaResepti( self, buf):
    otsikko = 'header'
    ainesLista = set()
    rivi = buf.readline()
    if (rivi.split()[0] != 'Reseptitiedosto'):
      raise BufferError('File format not resepti-format, Must start with "Reseptitiedosto"')
      return False
    name = buf.readline()
    portions = buf.readline()
    #sitten itse ohje
    while (rivi):
      #interpret headings
      command = rivi.strip().upper()
      if (command == "RAAKA-AINEET"):
        if( otsikko != 'header'):
          raise BufferError('Order of jääkaappi-file should be header-contents-instructions (RAAKA-AINEET out of place)')
        otsikko = 'contents'
        rivi = buf.readline()
      elif (command == "OHJEET"):
        if( otsikko != 'contents'):
          raise BufferError('Order of jääkaappi-file should be header-contents-instructions (OHJEET out of place)')
        otsikko = 'instructions'
        rivi = buf.readline()
      #depending on what we read, do different stuff
      if (otsikko == 'contents'):
        try:
          aines = self.parseLine(rivi)
          if (aines):
            ainesLista.add( aines)
        except AinesParseError as e:
          print('Error parsing :'+e.message)
      rivi = buf.readline()
    # Kun rivit luettu, luodaan reseptiolio
    uusiResepti = resepti( name, portions, ainesLista, "")
    self.reseptit.add( uusiResepti)

  def parseLine( self, rivi):
    # parses lines like: "Maitoa   1dl" into parts and returns them as tuple
    parts = re.findall(r"\s?(\w+)\s*([0-9]+)?(\w+)?(?:\n|$)", rivi)[0] #findall returns list of sets, but only one set per line...so slice
    aines = ainekset.ruokaAines( parts[0])
    return tuple( [aines, parts[1], parts[2]]) #Using a tuple here is clearer because it is not for iteration




  def lataaKansio( self, path):
    # add the file extension required by "glob"
    if (path.endswith("/")):
      path += "*.txt"
    else:
      path += "/*.txt"
    # fin all files in directory
    files = glob.glob( path)
    for name in files:
      try:
        buf = open( name)
        self.lataaResepti( buf)
        buf.close()
      except IOError as e:
        if (e.errno != errno.EISDIR): #it is not a directory, it's a real error
          raise


""" UNIT TESTS """
class Test( unittest.TestCase):
  #dummy test
  def test_testing( self):
    self.assertEqual( True, True)
  def test_loading( self):
    kirja = ReseptiKirja()
    kirja.lataaKansio("./reseptit/")


if __name__ == '__main__':
  unittest.main()

