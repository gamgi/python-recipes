import unittest
import re #regular expressions
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


def erotus( reseptiAine, kaappiAine):
  #esimääreet (nimi, preferenssiyksikkö, jatkuva, tiheys)
  esimääreet = [
    ('Maito','dl',True,1.044),
    ('Sipuli','kpl',False),
    ('Kananmuna','kpl',False),
    ('Makaroni','g',True, 0.5)
  ]
  tilavuudet = {'l':1, 'dl':0.1, 'cl':0.01, 'ml':0.001, 'rkl':0.015, 'tl':0.005}
  #v * ro = massa

  # Löytyykö aineesta tietoja?
  tulos_määrä = 0
  tulos_yksikkö = 0
  #for määre in esimääreet:
    #if (wordSimilarity( määre[0], aine) > 0.7):
  #    pass
  # Täsmäävätkö yksiköt?
  pohjaYksikko = re.sub("\d","",kaappiAine.todMaara)
  pohjaMaara = int(re.sub("\D","",kaappiAine.todMaara[::-1])[::-1])
  if (reseptiAine[2] == pohjaYksikko):
    erotus = max(0, int(reseptiAine[1]) - pohjaMaara)
    return (erotus, pohjaYksikko)
  #print("\ntämöne:",reseptiAine[2],"asd", kaappiAine.yksikko, pohjaYksikko)



""" UNIT TESTS """
class Test( unittest.TestCase):
  def test_wordsimilarity( self):
    self.assertEqual(0.4 , wordSimilarity("France", "french"))
    self.assertNotEqual(0 , wordSimilarity("Makarooni", "Makaroonit"))


if __name__ == '__main__':
  unittest.main()
