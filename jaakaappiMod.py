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
    self.allergiat = []
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
      if (otsikko == "TUOTTEIDEN MÄÄREET"):
        lukee = 'defs'
        rivi = buf.readline()
      elif (otsikko == "JÄÄKAAPIN SISÄLTÖ"):
        if( lukee != 'header' and lukee != 'defs'):
          raise BufferError('Order of jääkaappi-file should be header-defs-contents')
        lukee = 'contents'
        rivi = buf.readline()
      #depending on what we read, do differetn stuff
      if (lukee == 'defs'):
        d = re.split('\s+', rivi.rstrip().lower())
        # TODO
      elif (lukee == 'contents'):
        try:
          uusi = self.parseLine(rivi)
          if (uusi):
            self.ruokaAineet.append( uusi)
        except ainesMod.AinesParseError as e:
          print('Error parsing :'+e.message)
      rivi = buf.readline()
      #if not rivi:
      #  break
  def parseLine( self, rivi):
    #one rivi can conatin many items (10 prk maioa ex)
    #parts = rivi.strip().split("\t")
    parts = re.split('\s+', rivi.rstrip().lower())
    aines = ainesMod.ainesOsa( parts)
    return aines
    #print(parts)

  def onkoTuotetta( self, haettava):
    """Tarkistaa onko tuotetta jääkapissa, ja palauttaa kokonaismäärän, jos sattusi olemaan useaan kertaan
    Tämä mahdollista esim jos maitoa on useampi purkki"""
    tulos = []
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


  def lapaiseeAllergiat( self, resepti, allergiat):
    """tarkistaako läpäiseekö resepti allergiavaatimukset"""
    if (allergiat == None):
      return True
    ainekset = list(resepti.ainekset)
    for aines in ainekset: #NB aines is tuple
      """
      jaakaapissa = self.onkoTuotetta( aines[0])
      if (jaakaapissa != False):
        try:
          #print(jaakaapissa.allergiat)
          #Magic hack to check if any of allergies match
          if( any((True for x in jaakaapissa.allergiat if x in allergiat)) ):
            return False

        except:
          pass
      else:
        #hae tiedot jostain muualta TODO
        return True
        pass
      """
      for allergia in self.allergiat:
        if (functionsMod.wordSimilarity(allergia[0], aines[0].nimi) >= 0.8):
          #löytyis samankaltainen aine
          return False
    # Näyttää läpäisevän allergiat
    return True



  def lataaAllergiat( self, buf):
    """Lataa allergiatiedot tiedostosta"""
    self.allergiat = []
    rivi = buf.readline()
    if (rivi.split()[0] != 'Allergiatiedot'):
      raise BufferError('File format not allergiatiedot-format, Must start with "Allergiatiedot"')
      return False
    rivi = buf.readline()
    while (rivi):
      if (rivi[0:1] != '#'): #jos ei kommentti
        tiedot = re.split('\s+', rivi.rstrip().lower())
        if (len(tiedot) == 2):
          aine = tiedot[0]
          liput = ",".join(tiedot[1:])
          try:
            parsitut = ainesMod.parsiAllergiat(liput)
          except:
            raise
          else:
          #self.allergiat.append((tiedot[0],tiedot[1].upper()))
            self.allergiat.append((aine,parsitut))
      rivi = buf.readline()


  def mitaPuuttuu( self, resepti):
    """Kertoo puuttuuko reseptin valmistamiseen vaadittavista aineista jotain"""
    puuttuu = []
    eipuutu = []
    ainekset = list(resepti.ainekset)
    #print("reseptissä",ainekset,"puuttuu")
    for aines in ainekset: #NB aines is tuple
      jaakaapissa = self.onkoTuotetta( aines[0])
      if (jaakaapissa == False):
        #ainesosa puuttuu
        puuttuu.append( (aines[0],aines[1],aines[2], "", True)) #tuple of <object aines>, 20, dl, True/False "missing completely" 
        #print("puuttuu", aines[0], "(kokonaan)")
      else:
        #print( aines, jaakaapissa, "On kaappis")
        # Tuotetta on, mutta puuttuuko silti jokin määrä
        try:
          erotus,pohjaYksikko = functionsMod.erotus( aines, jaakaapissa)
          if (erotus > 0):
            puuttuu.append( (aines[0], erotus, pohjaYksikko, "(kaapissa oleva määrä "+jaakaapissa.maara+" "+aines[2]+" riittää pieneen erään)",False))
            #print("puuttuu",erotus,pohjaYksikko)
          else:
            #ainetta on tarpeeksi
            eipuutu.append( (jaakaapissa, aines[1],aines[2]))
        except ainesMod.AinesParseError as e:
          puuttuu.append( (aines[0], aines[1], aines[2], '(jääkaapissa on '+jaakaapissa.maara+' '+jaakaapissa.yksikko+', yksiköitä "'+aines[2]+'" ja "'+jaakaapissa.yksikko+'" ei voitu verrata)',False))
        except BaseException:
          #muunnos epäonnistui
          #print('virhe')
          puuttuu.append( (aines[0], aines[1], aines[2], '(jääkaapissa on '+jaakaapissa.maara+' '+jaakaapissa.yksikko+', yksiköitä "'+aines[2]+'" ja "'+jaakaapissa.yksikko+'" ei voitu verrata)',False))

          #print('Error in :'+e.message)
        #except BaseException as e:
          #print("oho",aines+":"+jaakaapissa)
        #  print("oho",e)
        #  pass
          

      #print(self.onkoTuotetta(aines.nimi))
      #todo käyttää onkoTuotetta ja palauttaa määrät
    
    return (puuttuu, eipuutu)


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
    #self.assertEqual(0, kaappi.onkoTuotetta( sipuli), "onkoTuotetta does not function as intended") 
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
    kirja = reseptiMod.ReseptiKirja()
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
      + u"Makarooni\t500\tg"
    self.input_file = StringIO(test_data)
    kaappi = JaaKaappi()
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()
    # Mitä puuttuu
    #print(resepti,"reseptinä")
    puuttuu = kaappi.mitaPuuttuu( resepti) # TODO
    self.assertEqual("Sipulia", puuttuu[0][0].nimi, "identifying missing failed")
    self.assertEqual(1, len(puuttuu), "identifying missing amount failed")
    # TODO lisää sipuli ja tarkista uudestaan
  
    #Lisätään sipuli
    sipuli = ainesMod.ruokaAines("sipuli")
    test_data += u"\nSipuli\t150\tg"
    self.input_file = StringIO(test_data)
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    #puuttuuko vielä?
    puuttuu = kaappi.mitaPuuttuu( resepti) # TODO
    self.assertEqual(0, len(puuttuu), "identifying missing amount failed")

  def test_lataaAllergiat( self):
    test_data = u"Allergiatiedot\n"\
      + u"# test comment\n"\
      + u"Maito\t\tL\n"\
      + u"Snickers\tP"
    self.input_file = StringIO(test_data)
    kaappi = JaaKaappi()
    try:
      kaappi.lataaAllergiat(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()
    vertailulista = [('maito',['L']),('snickers',['P'])]
    self.assertEqual(vertailulista, kaappi.allergiat, "Loading data failed.")


if __name__ == '__main__':
  unittest.main()
