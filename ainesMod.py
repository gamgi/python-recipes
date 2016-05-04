#from dateutil.parser import * as dateutilI#
#import dateutil.parser as dateutil
#from datetime import *
import time
import unittest

class AinesParseError(Exception):
  def __init__(self, message):
    self.message = message
    #def __init__(self, message):
        #super(AinesParseError, self).__init__(message)

class ruokaAines:
  def __init__( self, nimi):
    self.nimi = nimi
  def __str__( self):
    return self.nimi


def parsiAllergiat( allergiaData):
  #Vähälaktoosinen, Laktoositon, Gluteeniton, Maidoton, Allergeenit, Kasvis, Pähkinä, Soija, Vegaani
  flags = ['VL','L','G','M','A','K','P','S','V']
  parts = allergiaData.upper().split(',')
  #parts might have whitespace left, so take it out
  parts = list(map( str.strip, parts))
  #chek that all allergy flags are valid
  for i in parts:
    if (i not in flags):
      raise AinesParseError('allergy flag '+i+' unknown')
  return parts


class ainesOsa( ruokaAines):
  #def __init__( self, name, amount, unit, realAmount = None, allergies = None, date = None):
  def __init__( self, parts):
    # Basic data
    if (not parts[0] or not parts[1] or not parts[2]):
      raise AinesParseError('name, amount or unit missing.')
    self.nimi = parts[0]
    self.maara = parts[1]
    self.yksikko = parts[2]
    try:
      # More specific amount
      if (parts[4]):
        self.todMaara = parts[4]
      else:
        self.todMaara = Null
      # Allergy data
      if (parts[5]):
        self.allergiat = parsiAllergiat(parts[5])
      # Date (parasta ennen)
      if (parts[6]):
        #print(dateutil.parse(parts[5]))
        try:
          self.aika = time.strptime(parts[6], "%d.%m.%y")
        except ValueError:
          try:
            self.aika = time.strptime(parts[6], "%d.%m.%Y")
          except ValueError:
            raise AinesParseError('date in incompatible format. must be like 22.12.2016')
    except IndexError as e:
      #kaikkia parametrejä ei siis aseteta
      pass
  def __str__(self):
    out = self.nimi+"\t"+self.maara+" "+self.yksikko
    try:
      out += "\t"+self.todMaar
      out += "\t"+",".join(self.allergiat)
    except AttributeError:
      pass
    return out

""" UNIT TESTS """
class Test( unittest.TestCase):
  def test_parseAllergy( self):
    test_data = "VL, G"
    parsiAllergiat( test_data)
    #self.assertRaises(AinesParseError, parseAllergy, test_data)
    test_data = "P, Q"
    self.assertRaises(AinesParseError, parsiAllergiat, test_data)
