import hakuMod
import ainesMod
import functionsMod
import jaakaappiMod
import reseptiMod
import re #regular expressions

def valikko( viesti, eka, vika):
  while True:
    print(viesti)
    try:
      vastaus = int(input(">:(numero)"))
    except ValueError:
      print("Numero ei kelpaa")
    else:
      if (vastaus<eka or vastaus>vika):
        print("valitse y.o. vaihtoehdoista")
      else:
        #all OK
        return vastaus

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
  """print ("X==================X")
  print ("|   RESEPTIKIRJA   | HAE")
  print ("|       0.7        | OHJEET")
  print ("|                  | LISTAA")
  print ("|                  | ASETUKSET")
  print ("|                  | LOPETA")
  print ("X==================X")"""
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
        # Valikko
        vastaus = valikko(
          'Haluatko hakea:\n'\
              +'1) Jääkaapin sisällön perusteella\n'\
              +'2) Ainesosan perusteella\n'\
              +'2) Nimen perusteella\n', 1,3)
        #print("Haetaanko jääkaapin sisällön perusteella?")
        #vastaus = str(input(">:(K/E)")).upper()

        if (vastaus == 1):
          print("Kuinka monta puuttuvaa ainesta saa olla?")
          vastaus = str(input(">:(numero)")).upper()
          try:
            puuttuvia = int(vastaus)
          except ValueError:
            print("Numero ei kelpaa, oletetaan 0")
            puuttuvia = 0
          valmistettavat = hakuMod.haeValmistettavat( kirja, kaappi, puuttuvia)
          if (len(valmistettavat) == 0):
            print("Et voi valmistaa mitään jääkaapin sisällöllä (ei löytynyt yhtään reseptiä jonka aineista on väh. yksi aines)")
          else:
            print("Löytyi",len(valmistettavat),"kpl tuloksia:")
            for resepti in valmistettavat:
              print("\t",resepti[0],"(Puuttuu",resepti[1],"ainesosaa)")
              #print(resepti[2])
              print("\t\tPuuttuvat:")
              for p in resepti[2]: #puuttuvat
                print("\t\t  {0:23} {1} {2} {3}".format(p[0].nimi, p[1], p[2], p[3]))
                #print("\t\t",p[0].nimi,"\t\t\t"+p[1],p[2],p[3])
              print("\t\tEi puutu:")
              #print(resepti[4])
              for p in resepti[4]: #puuttuvat
                try:
                  print("\t\t  {0:23} {1} {2} ( Kaapissa {3} )".format(p[0].nimi, p[1], p[2], p[0].todMaara))
                except:
                  print("\t\t  {0:23} {1} {2} ( Kaapissa {3} {4})".format(p[0].nimi, p[1], p[2], p[0].maara, p[0].yksikko))
        elif (vastaus == 2):
          print("Anna hakusana")
          vastaus = str(input(">:"))
          try:
            tulos = kirja.haeNimella(vastaus, 0.6)
          except functionsMod.NotFoundError:
            print("Ei tuloksia")
          else:
            print("Löytyi",len(tulos),"kpl tuloksia:")
            for t in tulos:
              print(" "+t[0].nimi)
          
        elif (vastaus == 3):
          print("Anna ainesosa")
          vastaus = str(input(">:"))
          try:
            tulos = kirja.haeNimella(vastaus, 0.6)
          except functionsMod.NotFoundError:
            print("Ei tuloksia")
          else:
            print("Löytyi",len(tulos),"kpl tuloksia:")
            for t in tulos:
              print(" "+t[0].nimi)
          
        else:
          pass
           
      elif (komento == 'LISTAA'):
        vastaus = valikko(
          'Haluatko listata:\n'\
              +'1) Jääkaapin\n'\
              +'2) Reseptit\n'\
              +'3) Tietyn reseptinsisällön\n', 1,3)
        if (vastaus == 1):
          kaappi.listaaKaikki()
        elif (vastaus == 2):
          kirja.listaaKaikki()
        elif (vastaus == 3):
          print("Anna reseptin nimi")
          vastaus = str(input(">:"))
          #autocorrect :D
          try:
            nimi = kirja.haeNimi(vastaus, 0.6).nimi
          except functionsMod.NotFoundError:
            nimi = vastaus
          # itse haku 
          try:
            tulos = hakuMod.haeReseptiPuuttuvat( kirja, kaappi, nimi)
          except functionsMod.NotFoundError:
            print("Ei tuloksia")
          else:
            print("\t",nimi)
            print("\t\tPuuttuvat:")
            for p in tulos[2]: #puuttuvat
              print("\t\t  {0:23} {1} {2} {3}".format(p[0].nimi, p[1], p[2], p[3]))
            print("\t\tEi puutu:")
            for p in tulos[4]: #puuttuvat
              try:
                print("\t\t  {0:23} {1} {2} ( Kaapissa {3} )".format(p[0].nimi, p[1], p[2], p[0].todMaara))
              except:
                print("\t\t  {0:23} {1} {2} ( Kaapissa {3} {4})".format(p[0].nimi, p[1], p[2], p[0].maara, p[0].yksikko))
            #for aines in tulos.ainekset:
            #  print("\t",aines[0].nimi+"\t"+aines[1]+" "+aines[2])
          """
          try:
            tulos = kirja.haeNimi(vastaus, 0.6)
          except functionsMod.NotFoundError:
            print("Ei tuloksia")
          else:
            print(tulos.nimi)
            for aines in tulos.ainekset:
              print("\t",aines[0].nimi+"\t"+aines[1]+" "+aines[2])
          """
      elif (komento == 'OHJE'):
        print("""Reseptiohjelma v.10 2016
              Ohjelma lataa reseptit ja jääkaapin ja kertoo mitä voidaan valmistaa.

              Asetukset tiedostossa asetukset.txt 
              """)
        print("""
            HAE
              Ohjelma siiryy hakutilaan.
              Mikäli et ole määrittänyt allergioita, tulee ohjelma kysymään allergiatietosi. Ne tallennetaan asetustiedostoon.

              Käyttäjä voi hakea:
              (1)Jääkaapin sisällön perusteella
              (2)Ainesosan perusteella
              (3)Nimen perusteella

              Hauissa otetaan allergiatiedot huomioon.

              (1) Kohdassa listataan myös mitä reseptin aineista puuttuu ja kuinka paljon.

            OHJE
              Tulostaa ohjeen

            LISTAA
              Ohjelma siiryy listaustilaan.

              Käyttäjälle voi listata:
              (1)jääkaapin sisällön
              (2)ladatut resptit
              (3)Tietyn reseptin sisällön

              (3) Kohdassa listataan myös mitä reseptin aineista puuttuu ja kuinka paljon.

            ASETUKSET
              Ohjelma tulostaa ladatut asetukset

          LOPETA
              Ohjelman suoritus loppuu.
              Ohjelmasta voi myös poistua ctrl+d yhdistelmällä""")
          


              
      elif (komento == 'ASETUKSET'):
        print('Asetukset ladataan ohjelman käynnistyessä "asetukset.txt"-tiedostosta')
        print('Nykyiset asetukset')
        print(' allergiat\t\t',", ".join(asetukset.allergiat))
        print(' allergiatiedosto\t',asetukset.allergiatiedosto)
        print(' jaakaappitiedosto\t',asetukset.jaakaappitiedosto)
        print(' reseptikansio\t\t',asetukset.reseptikansio)
      elif (komento == 'LOPETA'):
        break
      else:
        print ("X==================X")
        print ("|   RESEPTIKIRJA   | HAE")
        print ("|       0.7        | OHJEET")
        print ("|                  | LISTAA")
        print ("|                  | ASETUKSET")
        print ("|                  | LOPETA")
        print ("X==================X")



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
