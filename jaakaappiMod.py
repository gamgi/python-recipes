import unittest
from io import StringIO
import ainesMod
import reseptiMod
import functionsMod
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
    aines = ainesMod.ainesOsa( parts)
    return aines
    #print(parts)

  def onkoTuotetta( self, haettava):
    tulos = []
    #print(self.ruokaAineet)
    for aines in self.ruokaAineet:
      if (functionsMod.wordSimilarity( aines.nimi, haettava.nimi) > 0.7):
      #if (aines.nimi == haettava.nimi):
        #huomaa että voi olla useampi sama tuote jääkaapissa
        tulos.append(aines)
    if (len(tulos) == 1):
      return tulos[0]
    # Summaa jos usea tulos
    if (len(tulos) > 1):
      pohja_yksikko = tulos[0].yksikko
      pohja_todYksikko = re.sub("\d","",tulos[0].todMaara)
      pohja = tulos[0]
      for aine in tulos:
        if (aine == tulos[0]):
          continue
        if (aine.yksikko == pohja_yksikko and re.sub("\d","",aine.todMaara) == pohja_todYksikko):
          pohja.maara += aine.maara
        else:
            raise ainesMod.AinesParseError('The Jaakaappi-tiedosto has multiple instances of '+aine.nimi+' with different base units')
          
      return pohja 

    return False

  def mitaPuuttuu( self, resepti):
    puuttuu = []
    ainekset = list(resepti.ainekset)
    #print("reseptissä",ainekset,"puuttuu")
    for aines in ainekset: #NB aines is tuple
      jaakaapissa = self.onkoTuotetta( aines[0])
      # määrien  vertailu TODO
      if (jaakaapissa == False):
        #ainesosa puuttuu
        puuttuu.append( (aines[0],aines[1],aines[2], "")) #tuple of <object aines>, 20, dl
        #print("puuttuu", aines[0], "(kokonaan)")
      else:
        #print( aines, jaakaapissa)
        # Tuotetta on, mutta puuttuuko silti jokin määrä
        try:
          erotus,pohjaYksikko = functionsMod.erotus( aines, jaakaapissa)
          if (erotus > 0):
            puuttuu.append( (aines[0], erotus, pohjaYksikko, ""))
            #print("puuttuu",erotus,pohjaYksikko)
        except ainesMod.AinesParseError as e:
          puuttuu.append( (aines[0], aines[1], aines[2], '(jääkaapissa on '+jaakaapissa.maara+' '+jaakaapissa.yksikko+', yksiköitä "'+aines[2]+'" ja "'+jaakaapissa.yksikko+'" ei voitu verrata)'))
          #print('Error in :'+e.message)
          

      #print(self.onkoTuotetta(aines.nimi))
      #todo käyttää onkoTuotetta ja palauttaa määrät
    
    return puuttuu


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
    sipuli = ainesMod.ruokaAines("sipuli")
    self.assertEqual(False, kaappi.onkoTuotetta( sipuli), "onkoTuotetta does not function as intended when returning false") 

    #Lisätään sipuli
    test_data += u"\nSipuli\t1\tkpl"
    self.input_file = StringIO(test_data)
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    #self.assertEqual(, kaappi.onkoTuotetta( sipuli), "onkoTuotetta does not function as intended") 
    #TODO testit
    # TODO funktion pitää myös palauttaa märä


  def test_mitaPuuttuu( self):
    # Resepti
    test_data = u"Reseptitiedosto\n"\
      + u"Makaroonilaatikko\n"\
      + u"1 Vuoka\n"\
      + u"RAAKA-AINEET\n"\
      + u"\tSipulia\t150g\n"\
      + u"\tMakaronia\t150g\n"\
      + u"\tMaitoa\t3dl\n"\
      + u"OHJEET\n"\
      + u"vlablalsa\n"\
      + u"asdasd"
    self.input_file = StringIO(test_data)
    kirja = reseptit.ReseptiKirja()
    try:
      kirja.lataaResepti(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()
    resepti = kirja.haeNimi("makaroonilaatikko")

    # Jääkaapin sisältö
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
    # Mitä puuttuu
    #self.assertEqual(False, kaappi.onkoTuotetta( sipuli), "onkoTuotetta does not function as intended") 
    print(resepti,"reseptinä")
    kaappi.mitaPuuttuu( resepti) # TODO
  
    #Lisätään sipuli
    sipuli = ainesMod.ruokaAines("sipuli")
    test_data += u"\nSipuli\t1\tkpl"
    self.input_file = StringIO(test_data)
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    #self.assertEqual(True, kaappi.onkoTuotetta( sipuli), "onkoTuotetta does not function as intended") 
    # TODO testit



  def test_parseAllergy( self):
    test_data = "VL, G"
    ainesMod.parsiAllergiat( test_data)
    #self.assertRaises(AinesParseError, parseAllergy, test_data)
    test_data = "P, Q"
    self.assertRaises(ainesMod.AinesParseError, ainesMod.parsiAllergiat, test_data)
if __name__ == '__main__':
  unittest.main()
