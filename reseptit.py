import unittest
from io import StringIO
import errno
import glob
import re #regular expressions
import ainekset


def wordSimilarity( word1, word2):
  """Olen suuresti ihastunut Simon Whiten Strike-a-match algoritmiin"""
  pairs1 = letterPairs( word1.lower())
  pairs2 = letterPairs( word2.lower())
  intersection = 0
  union = len(pairs1) + len(pairs2)
  for pair1 in pairs1:
    for pair2 in pairs2:
      if (pair1 == pair2):
        intersection += 1
        pairs2.remove(pair2)
  return (2 * intersection) / union


def letterPairs( word):
  pairs = []
  for c in range(len(word)-1):
    pairs.append(word[c:c+2])
  return pairs

class resepti:
  def __init__(self, nimi, annokset, ainekset, ohjeet):
    self.nimi = nimi
    self.annokset = annokset
    self.ainekset = ainekset
    self.ohjeet = ohjeet
  def __str__( self):
    return self.nimi

class ReseptiKirja:
  """ Luokka reseptien säilytykselle"""
  # Receipes stored as touples in a set: set(("Milk", "1dl"), ("Sugar", "1tbsp"))
  #reseptit = [] # a set would be great, but the issue of amounts in arithmetic operatiosn is unsolved
  # note to self:  never use immutable as defautl argument...will be aref in all instances of reseptikirja
  def __init__( self):
    self.reseptit = []
  def lataaResepti( self, buf):
    lukee = 'header'
    ainesLista = set()
    rivi = buf.readline()
    if (rivi.split()[0] != 'Reseptitiedosto'):
      raise BufferError('File format not resepti-format, Must start with "Reseptitiedosto"')
      return False
    nimi = buf.readline().strip().lower()
    annokset = buf.readline()
    #sitten itse ohje
    while (rivi):
      #interpret headings
      otsikko = rivi.strip().upper()
      if (otsikko == "RAAKA-AINEET"):
        if( lukee != 'header'):
          raise BufferError('Order of recipe-file should be header,RAAKA-AINEET,OHJEET (RAAKA-AINEET out of place)')
        lukee = 'contents'
        rivi = buf.readline()
      elif (otsikko == "OHJEET"):
        if( lukee != 'contents'):
          raise BufferError('Order of recipe-file should be header,RAAKA-AINEET,OHJEET (OHJEET out of place)')
        lukee = 'instructions'
        rivi = buf.readline()
      #depending on what we read, do different stuff
      if (lukee == 'contents'):
        try:
          aines = self.parseLine(rivi)
          if (aines):
            ainesLista.add( aines)
        except AinesParseError as e:
          print('Error parsing :'+e.message)
      rivi = buf.readline()
    # Kun rivit luettu, luodaan reseptiolio
    uusiResepti = resepti( nimi, annokset, ainesLista, "")
    self.reseptit.append( uusiResepti)

  def parseLine( self, rivi):
    # parses lines like: "Maitoa   1dl" into parts and returns them as tuple
    parts = re.findall(r"\s?(\w+)\s*([0-9]+)?(\w+)?(?:\n|$)", rivi)[0] #findall returns list of sets, but only one set per line...so slice with [0]. Regexp finds tab delimited gorups and separates the numbers from letters in "9dl"
    aines = ainekset.ruokaAines( parts[0])
    return tuple( [aines, parts[1], parts[2]]) #Using a tuple here is clearer because it is not for iteration

  def listaaKaikki( self):
    for resepti in self.reseptit:
      print( resepti)
    return len(self.reseptit) # returns nr of recipes

  def haeNimi( self, nimi):
    nimi = nimi.strip().lower()
    for resepti in self.reseptit:
      if (resepti.nimi == nimi):
        return resepti


  def haeAinesosalla( self, haettu_aines):
    tulos = []
    for resepti in self.reseptit:
      ainekset = list( resepti.ainekset)
      #print(resepti.nimi, ainekset)
      for aines in ainekset:
        similarity = wordSimilarity( aines[0].nimi, haettu_aines)
        #print(haettu_aines,"/",aines[0].nimi,similarity)
        if (similarity > 0.7):
          tulos.append( resepti)
    return tulos





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


  def test_loading_nofile( self):
    test_data = u"Reseptitiedosto\n"\
      + u"Makaroonilaatikko\n"\
      + u"RAAKA-AINEET\n"\
      + u"\tSipulia\t150g\n"\
      + u"\tMakaronia\t150g\n"\
      + u"\tMaitoa\t3dl\n"
    self.input_file = StringIO(test_data)
    kirja = ReseptiKirja()
    try:
      kirja.lataaResepti(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()
    self.assertNotEqual(0, kirja.listaaKaikki(), "Loading data failed.")

  def test_loading( self):
    kirja = ReseptiKirja()
    kirja.lataaKansio("./reseptit/")
  def test_name_search( self):
    kirja = ReseptiKirja()
    kirja.lataaKansio("./reseptit/")
    tulos = kirja.haeNimi("Makaroonilaatikko")
    self.assertEqual("makaroonilaatikko" , tulos.nimi)
  def test_wordsimilarity( self):
    self.assertEqual(0.4 , wordSimilarity("France", "french"))
    self.assertNotEqual(0 , wordSimilarity("Makarooni", "Makaroonit"))


  def test_search_by_ingredient( self):
    kirja = ReseptiKirja()
    kirja.lataaKansio("./reseptit/")
    tulos = kirja.haeAinesosalla( "Sipuli")
    self.assertEqual(tulos[0].nimi , "makaroonilaatikko")

if __name__ == '__main__':
  unittest.main()

