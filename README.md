# Rome’s treasures unveiled:an insider’s journey

Progetto di ingegneria della conoscenza 2022-2023. 
Componenti del team di sviluppo:
 - Daniele Guerra           (mat. 744399)
 - Nicola Lassandro         (mat. 735968)

# Installazione
Per procedere all'installazione, si prega di seguire i passaggi indicati di seguito.
In base al sistema operativo in uso (***è consigliato scaricare la versione 8***):

`https://www.swi-prolog.org/download/stable?show=all`

Posizionarsi all'interno della root principale:

`cd progetto_icon_guerra_lassandro`

Installare le dipendenze:

`pip install -r requirements.txt`

# Guida all'utilizzo
## 

I tre file eseguibili sono i seguenti:
- Preprocessor.py: script necessario per la raccolta dei dati mediante API di Google, attualmente l'API key inserita è scaduta poichè terminato il periodo di prova.
- KbManager: script necessario per la rielaborazione dei dati grezzi ottenuti con lo script precedente, mappandoli nelle istanze della classe utilizzata.
- MainSearch.py: main dell'applicazione, richiede l'inserimento di dati interi di budget e tempo per effettuare la ricerca mediante Searcher base e A* Searcher, infine richiede l'inserimento del feedback su una porzione dei punti di interesse consigliati.
