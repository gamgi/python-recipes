import unittest
from io import StringIO
import ainesMod
import jaakaappiMod
import reseptiMod
#ä


def haeValmistettavat( kirja, jaakaappi):
  valmistettavat = []
  for aines in jaakaappi.ruokaAineet:
    #print("Searching by",aines.nimi)
    tulos = kirja.haeAinesosalla( aines.nimi)
    for t in tulos:
      if (t.nimi not in valmistettavat):
        valmistettavat.append(t.nimi)
  #valmistettavat = list(valmistettavat)
  #print(valmistettavat)
  #mitä aineksia puuttuu näistä valmistetavista
  vertailulista = []
  for resepti_nimi in valmistettavat:
    #print(resepti_nimi,"*")
    puuttuu = jaakaappi.mitaPuuttuu( kirja.haeNimi(resepti_nimi)) # TODO pitäisi käydä kaikki läpi ja sortata
    if (len(puuttuu) > 4): #puuttuu liikaa aineksia
      continue
    vertailulista.append((resepti_nimi, len(puuttuu), puuttuu)) #TODO tulevaisuuden paranteluun: ei puuttuvien aineiden määrä ole paras tapa verrata?
  # Sort vertailulista
  return sorted(vertailulista, key=lambda x: x[1])
  


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
      + u"Maito\t1\tpurkki\ta\t10dl\tVL\t3.4.2016\n"\
      + u"Sipuli\t1\tkpl" #TODO fix when no todMaara is defined
      #+ u"Sipuli\t1\tkpl\ta\t100g"
    self.input_file = StringIO(test_data)
    kaappi = jaakaappiMod.JaaKaappi()
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
    kirja = reseptiMod.ReseptiKirja()
    try:
      kirja.lataaResepti(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()

    # SUORITA HAKU
    tulos = haeValmistettavat( kirja, kaappi)
    # TULOSTA
    for t in tulos:
      print (t[0], "puuttuu",t[1],"ainesta")
      puuttuvat = []
      for a in t[2]:
        print("\t",a[0],a[1],a[2])
        puuttuvat.append(a[0])
      #print("\t",puuttuvat)
    # Puuttuu makaronit ja sipuli, eli kaksi asiaa.
    self.assertEqual( tulos[0][0:2], ("makaroonilaatikko",2))


if __name__ == '__main__':
  unittest.main()

