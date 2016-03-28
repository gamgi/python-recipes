#from dateutil.parser import * as dateutilI#
#import dateutil.parser as dateutil
#from datetime import *
import time

class AinesParseError(Exception):
    def __init__(self, message):
        super(AinesParseError, self).__init__(message)


class ruokaAines:
  pass
def parseAllergy( allergyData):
  #Vähälaktoosinen, Laktoositon, Gluteeniton, Maidoton, Allergeenit, Kasvis, Pähkinä, Soija, Vegaani
  flags = ['VL','L','G','M','A','K','P','S','V']
  parts = allergyData.upper().split(',')
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
    self.name = parts[0]
    self.amount = parts[1]
    self.unit = parts[2]
    # More specific amount
    if (parts[3]):
      self.realAmount = parts[3]
    # Allergy data
    if (parts[5]):
      self.allergy = parseAllergy(parts[5])
    # Date (parasta ennen)
    if (parts[6]):
      #print(dateutil.parse(parts[5]))
      try:
        self.time = time.strptime(parts[6], "%d.%m.%y")
      except ValueError:
        try:
          self.time = time.strptime(parts[6], "%d.%m.%Y")
        except ValueError:
          raise AinesParseError('date in incompatible format. must be like 22.12.2016')

