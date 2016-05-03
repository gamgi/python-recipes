import unittest
from io import StringIO
import ainesMod
import jaakaappiMod
import reseptiMod
import functionsMod
#ä


def haeValmistettavat( kirja, jaakaappi, puuttuvia = 0):#, laiska = False):
  """ Hakee valmistettavat ruoat (tai josta puuttuu 'puuttuvia' kpl ainesosia). Laiskassa tilassa ohjelma myös antaa pienet määrälliset puutteet anteeksi"""
  # NB laiska-ominaisuutta ei toeutettu, koska turhahko

  # hakee ensin jääkaapin sisällön perusteella sopivat reseptit
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
    puuttuu = jaakaappi.mitaPuuttuu( kirja.haeNimi(resepti_nimi))
    #tarkista voidaanko puuttuva aines korvata alireseptillä
    for puuttuva in puuttuu:
      # hae tämän nimistä reseptiä
      try:
        resepti = kirja.haeNimi(puuttuva[0].nimi, 0.7)
      except functionsMod.NotFoundError:
        #print("errnofo",puuttuva[0].nimi)
        continue
        # Interesting bug, if you do Break behavior is udnefined in order
      else:
        print(puuttuva[0].nimi,"puuttuu löytyi korvaava",resepti.nimi)
        # remove from valmistettavat
        valmistettavat.remove(resepti.nimi)
        # remove this puuttuva as missing
        puuttuu.remove(puuttuva)
        #print(valmistettavat)
        alipuuttuu = jaakaappi.mitaPuuttuu( resepti)
        # add missing ingredients of subrecipe to current "puuttuu" list
        puuttuu.extend(alipuuttuu)
    #kun alireseptit on käsitelty, jatketaan vaatimusten tarkastelua
    if (len(puuttuu) > puuttuvia): #puuttuu liikaa aineksia
      continue
    #if (laiska == False and puuttuu[3] == False):
    #  #Suorittaa tiukan haun, eli "osittain" puuttuvat ainekset eiväty ole OK (puttuu[3] = "missing completely")
    #  continue
    vertailulista.append((resepti_nimi, len(puuttuu), puuttuu)) #TODO tulevaisuuden paranteluun: ei puuttuvien aineiden määrä ole paras tapa verrata?
  # Sort vertailulista puttuvien ainesosien määrän mukaan
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
    tulos = haeValmistettavat( kirja, kaappi,4)
    # TULOSTA
    for t in tulos:
      print (t[0], "puuttuu",t[1],"ainesta")
      puuttuvat = []
      for a in t[2]:
        print("\t",a[0],a[1],a[2],a[3])
        puuttuvat.append(a[0])
      #print("\t",puuttuvat)
    # Puuttuu makaronit ja sipuli, eli kaksi asiaa.
    self.assertEqual( tulos[0][0:2], ("makaroonilaatikko",2))



  def test_search_subrecipe_nofile( self):
    # LATAA JÄÄKAAPPI
    test_data = u"Jääkaappitiedosto versio 1.0\n"\
      + u"# Matin jääkaappi\n"\
      + u"JÄÄKAAPIN SISÄLTÖ\n"\
      + u"Maito\t1\tpurkki\ta\t10dl\tVL\t3.4.2016\n"\
      + u"Voi\t1\tpurkki\ta\t400g\tVL\t5.4.2016\n"\
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
    #piiras
    test_data = u"Reseptitiedosto\n"\
      + u"Kombopiiras\n"\
      + u"1 Vuoka\n"\
      + u"RAAKA-AINEET\n"\
      + u"\tSipulia\t150g\n"\
      + u"\tJauhelihaa\t150g\n"\
      + u"\tVoitaikinaa\t1vuoka\n"\
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
    #voitaikina
    test_data = u"Reseptitiedosto\n"\
      + u"Voitaikina\n"\
      + u"1 Vuoka\n"\
      + u"RAAKA-AINEET\n"\
      + u"\tVoi\t150g\n"\
      + u"\tJauhot\t150g\n"\
      + u"OHJEET\n"\
      + u"Tee diipadaa"\
      + u"Ruokaa\n"
    self.input_file = StringIO(test_data)
    try:
      kirja.lataaResepti(self.input_file)
    except IOError:
      self.fail("Loading a correctly structured file caused an exception")
    self.input_file.close()
    #mitäs on kirjassa
    #print(kirja.reseptit, "reseptiejäa")
    # SUORITA HAKU
    tulos = haeValmistettavat( kirja, kaappi,40)
    # TULOSTA
    for t in tulos:
      print (t[0], "puuttuu",t[1],"ainesta")
      puuttuvat = []
      for a in t[2]:
        print("\t",a[0],a[1],a[2],a[3])
        puuttuvat.append(a[0])
      #print("\t",puuttuvat)
    # Puuttuu makaronit ja sipuli, eli kaksi asiaa.
    #self.assertEqual( tulos[0][0:2], ("makaroonilaatikko",2))


if __name__ == '__main__':
  unittest.main()

