import unittest
from io import StringIO
import ainekset
import jaakaappi
import reseptit

def haeValmistettavat( reseptit, jaakaappi):
  valmistettavat = set()
  for aines in jaakaappi.ruokaAineet:
    #print("Searching by",aines.nimi)
    tulos = reseptit.haeAinesosalla( aines.nimi)
    valmistettavat.update( tulos)
  return list(valmistettavat)

""" UNIT TESTS """
class Test( unittest.TestCase):
  #dummy test
  def test_testing( self):
    self.assertEqual( True, True)


  def test_search_nofile( self):
    # LATAA JÄÄKAAPPI
    test_data = u"Jääkaappitiedosto versio 1.0\n"\
      + u"# Matin jääkaappi\n"\
      + u"JÄÄKAAPIN SISÄLTÖ\n"\
      + u"Maito\t1\tpurkki\ta\t10dl\tVL\t3.4.2016"
    self.input_file = StringIO(test_data)
    kaappi = jaakaappi.JaaKaappi()
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()

    # LATAA RESEPTIT
    test_data = u"Reseptitiedosto\n"\
      + u"Makaroonilaatikko\n"\
      + u"1 Vuoka\n"\
      + u"RAAKA-AINEET\n"\
      + u"\tSipulia\t150g\n"\
      + u"\tMakaronia\t150g\n"\
      + u"\tMaitoa\t3dl\n"\
      + u"OHJEET\n"\
      + u"Tee jotainn"\
      + u"Ruokaa\n"
    self.input_file = StringIO(test_data)
    kirja = reseptit.ReseptiKirja()
    try:
      kirja.lataaResepti(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()

    # SUORITA HAKU
    tulos = haeValmistettavat( kirja, kaappi)


    self.assertEqual( tulos[0].nimi, "makaroonilaatikko")


if __name__ == '__main__':
  unittest.main()

