# analisi_dati_fair

Analizza il metadato "Dati FAIR" di IRIS e fornisce un grafico dei repository linkati nei metadati URL e DOI.

```clean.py```

* importa i dati dell'estrazione di IRIS
* rimuove i caratteri usati come placeholder
* se il doi esiste, rimuove le URL, se presenti
* esplode le liste di doi e url separate da punto e virgola
* estrae i prefissi dei DOI e i domini delle URL
* conta i DOI e le URL uniche

```enrich.py``` interroga DataCite (e, di risulta, Crossref) per individuare i le organizzazioni a cui si riferiscono i DOI

```combined.py``` combina le tabelle di doi e domini

```map.csv``` è una mappatura realizzata manualmente per normalizzare i nomi dei domini e delle organizzazioni responsabili dei prefissi DOI. I doi e i domini relativi a riviste ed editori sono mappati come `None`, e verranno rimossi con l'esecuzione di ```normalize.py```

```normalize.py``` normalizza la conta dei DOI utilizzando i nomi contenuti in map.csv

```draw_graph.py``` disegna il grafico a blocchi.
