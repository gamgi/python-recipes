import unittest
#from io import StringIO
import errno
import glob
import re #regular expressions
import ainekset

class resepti:
  def __init__(self, name, portions, ingredients, instructions):
    self.name = name
    self.portions = portions
    self.ingredients = ingredients
    self.instructions = instructions

class ReseptiKirja:
  """ Luokka reseptien säilytykselle"""
  # Receipes stored as touples in a set: set(("Milk", "1dl"), ("Sugar", "1tbsp"))
  recipes = set()
  def loadRecipe( self, buf):
    reading = 'header'
    ingredientList = set()
    line = buf.readline()
    if (line.split()[0] != 'Reseptitiedosto'):
      raise BufferError('File format not resepti-format, Must start with "Reseptitiedosto"')
      return False
    name = buf.readline()
    portions = buf.readline()
    #sitten itse ohje
    while (line):
      #interpret headings
      command = line.strip().upper()
      if (command == "RAAKA-AINEET"):
        if( reading != 'header'):
          raise BufferError('Order of jääkaappi-file should be header-contents-instructions (RAAKA-AINEET out of place)')
        reading = 'contents'
        line = buf.readline()
      elif (command == "OHJEET"):
        if( reading != 'contents'):
          raise BufferError('Order of jääkaappi-file should be header-contents-instructions (OHJEET out of place)')
        reading = 'instructions'
        line = buf.readline()
      #depending on what we read, do different stuff
      if (reading == 'contents'):
        try:
          ingredient = self.parseLine(line)
          if (ingredient):
            ingredientList.add( ingredient)
        except AinesParseError as e:
          print('Error parsing :'+e.message)
      line = buf.readline()
    # Kun rivit luettu, luodaan reseptiolio
    newRecipe = resepti( name, portions, ingredientList, "")
    self.recipes.add( newRecipe)

  def parseLine( self, line):
    # parses lines like: "Maitoa   1dl" into parts and returns them as tuple
    parts = re.findall(r"\s?(\w+)\s*([0-9]+)?(\w+)?(?:\n|$)", line)[0] #findall returns list of sets, but only one set per line...so slice
    aines = ainekset.ruokaAines( parts[0])
    return tuple( [aines, parts[1], parts[2]]) #Using a tuple here is clearer because it is not for iteration




  def loadFolder( self, path):
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
        self.loadRecipe( buf)
        buf.close()
      except IOError as e:
        if (e.errno != errno.EISDIR): #it is not a directory, it's a real error
          raise


""" UNIT TESTS """
class Test( unittest.TestCase):
  #dummy test
  def test_testing( self):
    self.assertEqual( True, True)
  def test_loading( self):
    kirja = ReseptiKirja()
    kirja.loadFolder("./reseptit/")


if __name__ == '__main__':
  unittest.main()
