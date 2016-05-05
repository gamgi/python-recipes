from io import StringIO
import unittest
import reseptiMod
import jaakaappiMod
import re #regular expressions

import ainesMod
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

class NotFoundError(Exception):
  def __init__(self, message = ''):
    self.message = message
    #def __init__(self, message):
        #super(AinesParseError, self).__init__(message)
class LoadingError(Exception):
  def __init__(self, message = ''):
    self.message = message
    #def __init__(self, message):
        #super(AinesParseError, self).__init__(message)

def erotus( reseptiAine, kaappiAine):
  """ Laskee riittääkö kaapissa oleva aine reseptin tarpeisiin """
  #esimääreet (nimi, preferenssiyksikkö, jatkuva, tiheys)
  esimääreet = [
    ('maito','dl',True,1.044),
    ('sipuli','kpl',False),
    ('kananmuna','kpl',False),
    ('makaroni','g',True, 0.5), # 0.5 * 0.1L = 0.05kG = 50g
    ('jauhot','dl',True, 0.65) # 65g = 0.065kG / 0.65 = 1dl
  ]
  tilavuudet = {'l':1, 'dl':0.1, 'cl':0.01, 'ml':0.001, 'rkl':0.015, 'tl':0.005}
  massat = {'kg':1, 'g':0.001}
  #v * ro = massa

  # Löytyykö aineesta tietoja?
  tulos_määrä = 0
  tulos_yksikkö = 0
  #for määre in esimääreet:
    #if (wordSimilarity( määre[0], aine) > 0.7):
  #    pass
  # Onko tod.Maara määritetty, jos on voidaan sen perusteella vertailla
  try:
    # Täsmäävätkö yksiköt?
    pohjaYksikko = re.sub("\d","",kaappiAine.todMaara)
    pohjaMaara = int(re.sub("\D","",kaappiAine.todMaara[::-1])[::-1])
  except AttributeError:
    #todMaara ei ole määritelty, täytyy tyytyä ensimmäiseen määriteltyyn yksikköön joka voi olal "kpl","purkki" tms.
    pohjaYksikko = kaappiAine.yksikko.lower()
    pohjaMaara = int(kaappiAine.maara)
  pohjaNimi = kaappiAine.nimi

  reseptiYksikko = reseptiAine[2].lower()
  reseptiMaara = int(reseptiAine[1])
  reseptiNimi = reseptiAine[0].nimi
  if (reseptiYksikko == pohjaYksikko):
    erotus = max(0, reseptiMaara - pohjaMaara)
    return (erotus, pohjaYksikko)
  else:
    # TODO tarkista ovatko molemmat esim tilavuuksia, jolloin voidaan toteuttaa ilman tietoja
    # Yksiköt eivät täsmää. On tehtävä muunnos, tai ilmoitetava virheestä

    # Seuraava mielenkiintoinen rivi tarkistaa onko tiheys tiedossa ja lisää sen "muunnoslistaan"
    muunnosLista = [määre for määre in esimääreet if wordSimilarity(pohjaNimi, määre[0])>0.7]
    if (len(muunnosLista) != 0):
      try:
        tiheys = muunnosLista[0][3]
        tiheysMuunnosYksikko = muunnosLista[0][1]
        #löytynyt siis massan yksikkö, tilavuudemn yksikkö ja jopa tiheys
      except IndexError:
        #ei trunnettua tiheyttä
        return (0,'?')
    #v * ro = massa
    #('makaroni','g',True, 0.5), # 0.5 * 0.1L = 0.05kG = 50g
    #('jauhot','dl',True, 0.65) # 65g = 0.065kG / 0.65 = 1dl
    #Halutaan muuttaa joko kaapin muotoon jai reseptin muotoon
    #erotukset lasketaan perusyksiköisää, ja muunnetaan lopuksi "preferoituun" yksikköön
    if (reseptiYksikko in tilavuudet):
      if(pohjaYksikko in massat):
        #reseptissä tilavuus ja kaapissa massa
        if(tiheysMuunnosYksikko in tilavuudet):
          #print("muunnos tilavuuteen (kaappi->resepti)")
          muunnos = pohjaMaara * massat[pohjaYksikko] / tiheys
          erotus = max(0, reseptiMaara * tilavuudet[reseptiYksikko] - muunnos)
          #muutetaan toivottuun yksikköön (muunostaulukosta)
          erotus = erotus / tilavuudet[tiheysMuunnosYksikko]
          erotus = round(erotus,2)
          return (erotus,tiheysMuunnosYksikko)
        elif (tiheysMuunnosYksikko in massat):
          #print("muunnos massaan (kaappi->resepti)")
          #resepti: dl, kaappi: g, muunnos: g
          muunnos = reseptiMaara * tilavuudet[reseptiYksikko] * tiheys
          erotus = max(0, muunnos - pohjaMaara * massat[pohjaYksikko])
          #muutetaan toivottuun yksikköön (muunostaulukosta)
          erotus = erotus / massat[tiheysMuunnosYksikko]
          erotus = round(erotus,2)
          return (erotus,tiheysMuunnosYksikko)
    elif (reseptiYksikko in massat):
      return (0,reseptiYksikko)
      #paranneltavaa on
      #if(pohjaYksikko in massat):
        #reseptissä massa ja kaapissa tilavuus
      #  pass

      """
      print("muunoslistassa")
      # etsi ainetta vastaava muunnos
      muunnosLista = [määre for määre in esimääreet if wordSimilarity(määre[1], reseptiYksikko)>0.7]
      print(muunnosLista)
      # valitaan nyt tässä tapauksessa ensimmäinen tulos
      if (len(muunnosLista) == 3):
        muunnos = muunnosLista[0]
        if (muunnos[3] == reseptiYksikko): #mikäli löytyy sopiva muunnos, niin muunnetaan
          print("Converting", reseptiYksikko,"to",muunnos[3])
        
      #return ('asd','derå')
      return (0, '?')
      #raise BaseException #TODO
    else:
      return (0, '??')
      # Tässä voisi käyttää hyväksi esimääriteltyjä tauluja, mutta tämän tehtävän pointti ei ole tehdä tarkkoja muunnoksia vaan toteuttaa reseptihakua.
      
      raise ainesMod.AinesParseError('The comparison between '+pohjaYksikko+' and '+reseptiAine[2]+' failed on item "'+reseptiAine[0].nimi+'"')
      """
    
  #print("\ntämöne:",reseptiAine[2],"asd", kaappiAine.yksikko, pohjaYksikko)



""" UNIT TESTS """
class Test( unittest.TestCase):
  def test_wordsimilarity( self):
    self.assertEqual(0.4 , wordSimilarity("France", "french"))
    self.assertNotEqual(0 , wordSimilarity("Makarooni", "Makaroonit"))

  def test_erotus( self):
    # Ladataan resepti
    test_data = u"Reseptitiedosto\n"\
      + u"Makaroonilaatikko\n"\
      + u"1 Vuoka\n"\
      + u"RAAKA-AINEET\n"\
      + u"\tSipulia\t150g\n"\
      + u"\tJauhoja\t2dl\n"\
      + u"\tMakaroni\t4dl\n"
    self.input_file = StringIO(test_data)
    kirja = reseptiMod.ReseptiKirja()
    try:
      kirja.lataaResepti(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()
    # Ladataan Kaappi
    test_data = u"Jääkaappitiedosto versio 1.0\n"\
      + u"# Matin jääkaappi\n"\
      + u"JÄÄKAAPIN SISÄLTÖ\n"\
      + u"Sipuli\t150\tg\n"
      #+ u"Sipuli\t150\tg"
    self.input_file = StringIO(test_data)
    kaappi = jaakaappiMod.JaaKaappi()
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()

    #testit g - g
    kaine = kaappi.ruokaAineet[0]
    raine = kirja.haeNimi('makaroonilaatikko').ainekset[0]

    #print(raine,kaine)
    ero = erotus(raine, kaine)
    self.assertEqual((0,'g') , ero)
    
    # Ladataan Kaappi uudelleen
    test_data = u"Jääkaappitiedosto versio 1.0\n"\
      + u"# Matin jääkaappi\n"\
      + u"JÄÄKAAPIN SISÄLTÖ\n"\
      + u"Sipuli\t50\tg\n"\
      + u"Jauhoja\t1\tkg\n"\
      + u"Makaronia\t150\tg\n"
    self.input_file = StringIO(test_data)
    kaappi = jaakaappiMod.JaaKaappi()
    try:
      kaappi.lataaJaakaappi(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()

    #testit sipuli g - g
    kaine = kaappi.ruokaAineet[0]
    raine = kirja.haeNimi('makaroonilaatikko').ainekset[0]
    #print(raine,kaine)
    ero = erotus(raine, kaine)
    self.assertEqual((100,'g') , ero)

    # NYT jauhoilla dl - kg
    kaine = kaappi.ruokaAineet[1]
    raine = kirja.haeNimi('makaroonilaatikko').ainekset[1]
    ero = erotus(raine, kaine)
    self.assertEqual((0,'dl') , ero)

    # NYT makaroineilla dl - g
    kaine = kaappi.ruokaAineet[2]
    raine = kirja.haeNimi('makaroonilaatikko').ainekset[2]
    ero = erotus(raine, kaine)
    self.assertEqual((50.0,'g') , ero)

if __name__ == '__main__':
  unittest.main()
