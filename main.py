import hakuMod
import ainesMod
import jaakaappiMod
import reseptiMod

def paaohjelma( ):
  # LATAA
  try:
    kirja = reseptiMod.ReseptiKirja()
    kirja.lataaKansio("./reseptit/")

    kaappi = jaakaappiMod.JaaKaappi()
    try:
      buf = open( "./jaakaappi.txt")
      kaappi.lataaJaakaappi( buf)
      buf.close()
    except IOError as e:
        raise
  except FileNotFoundError as e:
    print("Tiedostoa ei löytynyt",str(e)[str(e).index("'"):])

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



      # lue uusi komento
      komento = str(input(">:")).upper()
  except KeyboardInterrupt:
    print("\nHyvästi!")
  except EOFError:
    print("\nHyvästi!")
  except:
    raise



if __name__ == '__main__':
  paaohjelma()
