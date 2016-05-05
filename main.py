import hakuMod
import ainesMod
import functionsMod
import jaakaappiMod
import reseptiMod
import re #regular expressions
class Asetukset:
  def __init__( self, tiedostopolku):
    #määrittelyjä
    self.allergiat = []

    # Toimintaa
    try:
      # lataa asetukset
      buf = open( tiedostopolku)
      self.lataaAsetukset( buf)
      buf.close()
    except IOError as e:
        raise functionsMod.LoadingError('Asetustiedostoa "asetukset.txt" ei voitu lukea')



  def lataaAsetukset(self, buf):
    """Lataa ohjelman asetukset tiedostosta"""
    self.allergiat = []
    self.allergiatSet = False
    rivi = buf.readline()

    if (rivi.strip() != 'Asetustiedosto'):
      raise BufferError('Asetustiedoston formaatti on virheellinen. Tulee alkaa rivillä "Asetustiedosto"')
      return False
    rivi = buf.readline().strip()
    while (rivi):
      if (rivi[0:1] != '#'): #jos ei kommentti
        tiedot = re.split('\s+', rivi.rstrip().lower())
        if (len(tiedot) == 2):
          komento = tiedot[0].lower()
          if (komento == 'allergiat'):
            if (tiedot[1] != 'None'):
              self.allergiat = ainesMod.parsiAllergiat(tiedot[1])
              self.allergiatSet = True
          elif (komento == 'allergiatiedosto'):
            self.allergiatiedosto = tiedot[1]
          elif (komento == 'jaakaappitiedosto'):
            self.jaakaappitiedosto = tiedot[1]
          elif (komento == 'reseptikansio'):
            self.reseptikansio = tiedot[1]
        elif(len(tiedot))==1:
          #varmaan whitespace rivi
          pass
        else:
          raise functionsMod.LoadingError('Asetustiedostossa virhe rivillä. Muodon tulee olla "asetus<tab>arvo. Rivillä on turhaa whtespacea."')
      rivi = buf.readline()
    #onko tarvittava ladattu?
    try:
      self.allergiatiedosto
    except AttributeError:
      raise BufferError('Asetustiedosto ei aseta "allergiatiedosto" arvoa')
    try:
      self.jaakaappitiedosto
    except AttributeError:
      raise BufferError('Asetustiedosto ei aseta "jaakaappitiedosto" arvoa')
    try:
      self.reseptikansio
    except AttributeError:
      raise BufferError('Asetustiedosto ei aseta "reseptikansio" arvoa')
        


def paaohjelma( ):
  # LATAA
  # Asetukset
  try:
    asetukset = Asetukset('./asetukset.txt')
  except BaseException as e:
    raise
    if (len(e.args) == 1):
      print("Virhe,",e.args[0])
    else:
      print("Virhe",e.message)
    return

  # MUUT
  try:
    # Reseptit
    kirja = reseptiMod.ReseptiKirja()
    kirja.lataaKansio(asetukset.reseptikansio)
    # Jääkaappi
    kaappi = jaakaappiMod.JaaKaappi()
    try:
      # sisältö
      buf = open( asetukset.jaakaappitiedosto)
      kaappi.lataaJaakaappi( buf)
      buf.close()
      # allergiatiedot
      buf = open( asetukset.allergiatiedosto)
      kaappi.lataaAllergiat( buf)
      buf.close()
    except IOError as e:
        raise
  except FileNotFoundError as e:
    print("Virhe, Tiedostoa ei löytynyt",str(e)[str(e).index("'"):])
  except BaseException as e:
    if (len(e.args) == 1):
      print("Virhe,",e.args[0])
    else:
      print("Virhe",e.message)
    return

  # TULOSTA
  print ("X==================X")
  print ("|   RESEPTIKIRJA   | HAE")
  print ("|       0.7        | OHJEET")
  print ("|                  | LISTAA")
  print ("|                  | ASETUKSET")
  print ("|                  | LOPETA")
  print ("X==================X")
  komento = ''
  try:
    while komento != 'lopeta':
      # Käsittele komennot
      if (komento == 'HAE'):
        # Tarkista allergia-asetukset
        if (asetukset.allergiatSet == False):
          print("Et ole määritellyt vielä allergiatietojasi, haluatko asettaa ne?")
          vastaus = str(input(">:(K/E)")).upper()
          if (vastaus == 'K'):
            print("Anna allergiatietosi pilkuilla erotettuna.")
            ok = False
            while( ok == False):
              print("Allergiatiedot annetaan kirjaimin:\n"\
                    +" L = laktoosi\tG = gluteeni\n"\
                    +" P = pähkinä")
              vastaus = str(input(">:")).upper()
              try:
                parsitut = ainesMod.parsiAllergiat( vastaus)
              except ainesMod.AinesParseError as e:
                print("Virhe,",e.message)
              else:
                ok = True
                #Tallennetaan
                print('Allergia-asetuksesi tallennetaan tiedostoon "asetukset.txt", voit muokata niitä myöhemmin')
                with open("asetukset.txt", "a") as tiedosto:
                  tiedosto.write("allergiat "+",".join(parsitut)+"\n")


        print("Haetaanko jääkaapin sisällön perusteella?")
        vastaus = str(input(">:(K/E)")).upper()

        if (vastaus == 'K'):
          print("Kuinka monta puuttuvaa ainesta saa olla?")
          vastaus = str(input(">:(numero)")).upper()
          try:
            puuttuvia = int(vastaus)
          except ValueError:
            print("Numero ei kelpaa, oletetaan 0")
            puuttuvia = 0
          valmistettavat = hakuMod.haeValmistettavat( kirja, kaappi, puuttuvia)
          if (len(valmistettavat) == 0):
            print("Et voi valmistaa mitään jääkaapin sisällöllä")
          else:
            print("Valmistettavat ruoat:")
            for resepti in valmistettavat:
              print("\t",resepti[0],"(Puuttuu",resepti[1],"ainesosaa)")
        else:
          pass
           
      elif (komento == 'ASETUKSET'):
        print('Asetukset ladataan ohjelman käynnistyessä "asetusket.txt"-tiedostosta')
        print('Nykyiset asetukset')
        print(' allergiat\t\t',", ".join(asetukset.allergiat))
        print(' allergiatiedosto\t',asetukset.allergiatiedosto)
        print(' jaakaappitiedosto\t',asetukset.jaakaappitiedosto)
        print(' reseptikansio\t\t',asetukset.reseptikansio)
      elif (komento == 'LOPETA'):
        break



      # lue uusi komento
      komento = str(input(">:")).upper()
  except KeyboardInterrupt:
    print("\nHyvästi!")
  except EOFError:
    print("\nHyvästi!")
  except BaseException as e:
    raise
    if (len(e.args) == 1):
      print("Virhe,",e.args[0])
    else:
      print("Virhe",e.message)
    return



if __name__ == '__main__':
  paaohjelma()
