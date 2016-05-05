import unittest
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
    ('makaroni','g',True, 0.5)
  ]
  tilavuudet = {'l':1, 'dl':0.1, 'cl':0.01, 'ml':0.001, 'rkl':0.015, 'tl':0.005}
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
    pohjaYksikko = kaappiAine.yksikko
    pohjaMaara = int(kaappiAine.maara)

  if (reseptiAine[2] == pohjaYksikko):
    erotus = max(0, int(reseptiAine[1]) - pohjaMaara)
    return (erotus, pohjaYksikko)
  else:
    # Yksiköt eivät täsmää. On tehtävä muunnos, tai ilmoitetava virheestä
    # Jos kyseessä on painoyksikkö
    if (reseptiAine[2] in tilavuudet):
      # etsi ainetta vastaava muunnos
      muunnosLista = [määre for määre in esimääreet if wordSimilarity(määre[1], reseptiAine[2])>0.7]
      # valitaan nyt tässä tapauksessa ensimmäinen tulos
      if (len(muunnosLista) == 3):
        muunnos = muunnosLista[0]
        if (muunnos[3] == reseptiAine[2]): #mikäli löytyy sopiva muunnos, niin muunnetaan
          print("Converting", reseptiAine[2],"to",muunnos[3])
        
      #return ('asd','derå')
      raise BaseException #TODO
    else:
      # Tässä voisi käyttää hyväksi esimääriteltyjä tauluja, mutta tämän tehtävän pointti ei ole tehdä tarkkoja muunnoksia vaan toteuttaa reseptihakua.
      raise ainesMod.AinesParseError('The comparison between '+pohjaYksikko+' and '+reseptiAine[2]+' failed on item "'+reseptiAine[0].nimi+'"')
    
  #print("\ntämöne:",reseptiAine[2],"asd", kaappiAine.yksikko, pohjaYksikko)



""" UNIT TESTS """
class Test( unittest.TestCase):
  def test_wordsimilarity( self):
    self.assertEqual(0.4 , wordSimilarity("France", "french"))
    self.assertNotEqual(0 , wordSimilarity("Makarooni", "Makaroonit"))


if __name__ == '__main__':
  unittest.main()
