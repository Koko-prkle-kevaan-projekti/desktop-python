# Tassututka työpöytä- sekä palvelinsovellus

Katso karttoja ja ihmettele piskisi aivoituksia. Tämä repository sisältää palvelin-
ja työpöytäohjelmat.

## Asennus

Asenna ensin python tulkki osoitteesta [python.org](https://python.org). Asennuksen
aikana huomaa lisätä raksi ruutuun, jossa tulkin sijainti lisätään PATH
ympäristömuuttujaan. Asennuksen jälkeen avaa PowerShell, ja kirjoita PowerShellissä
komento `pip install git+https://github.com/Koko-prkle-kevaan-projekti/desktop-python`.

## Käyttöönotto

Työpöytäohjelman pystyy ajamaan komennolla
`ttutka.exe client --server-address <ip> --server-port <port> gui`. Ensimmäisellä
käynnistyskerralla palvelimen osoite sekä portti tallennetaan, eikä kyseisiä vipuja
tarvitse antaa enää seuraavilla käynnistyskerroilla. Serveriohjelman käynnistämisessä
mahdollisiin vipuihin saa ohjeet komennolls `ttutka server -h`. Portit ja IP-osoitteet
ovat vapaaehtoisia. Oletusportit ovat 65000 GPS-laitetta varten, sekä 8000
työpöytäohjelmaa varten.

## Muuta huomioitavaa

Käyttääksesi tätä ohjelmaa tarvitset myös GPS-laitteen, jolla on pääsy internetiin,
ja jonka voit laittaa lähettämään NMEA RMC-viestejä haluamaasi osoitteeseen TCP-yhteyttä
käyttäen. Katso [projektin kotisivuilta](https://soisenniemi.net/tassututka/index.htm)
yksi vaihtoehto GPS-laitteeksi.


## Lopuksi

Ohjelma toimii tarpeeksi hyvin ollakseen sivujuonne kurssilla, jossa tarkoituksena on
tutustua sulautettuihin järjestelmiin. Siinä on bugeja, testejä on liian vähän ja
muutenkin ohjelmaa voisi parannella monella tavoin. Se ei kuitenkaan ole kurssille
varatun tuntimäärän puitteissa järkevää. Luultavasti se menee hieman ohi kurssin
tavoitteista. Tarkoituksena lienee tutustua sulautettuihin järjestelmiin, ja oppia
projektiviestintää. Siispä edes ohjelman tunnettuja vikoja ei tulla näillä näkymin
korjaamaan.
