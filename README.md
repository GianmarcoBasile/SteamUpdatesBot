# SteamUpdatesBot

Il progetto consiste nella creazione di un bot telegram che permette di:
- Aggiungere e rimuovere giochi di steam ad una lista di preferiti
- Stampare la lista
- Svuotare la lista
- Ottenere le notizie più recenti riguardo i giochi nella propria lista
- Verificare i saldi su ogni gioco della lista

Il bot inoltre invia ogni giorno e automaticamente la notizia più recente per ogni gioco della lista e un messaggio che notifica se un gioco è in sconto o meno.

## Installazione

Prima di procedere, assicurarsi di avere installato la versione di Python 3.10 e di aver installato MongoDB (https://www.mongodb.com/try/download/community).

Per avviare il bot, bisogna innanzitutto installare le dipendenze necessarie, lanciando il seguente comando da terminale:

<code>pip install -r requirements.txt</code>

Se si desidera eseguire i test sul codice, allora bisogna installare anche le dipendenze nel file requirements_dev.txt con il comando:

<code>pip install -r requirements_dev.txt</code>

Una volta installate le dipendenze, basta avviare il bot da terminale con il comando:

<code>python3 .\src\main.py</code>

## Guida all'uso

Una volta avviato il bot, basta aprire la chat del bot  ***SteamUpdatesBot*** e scrivere il comando **/start**.

A questo punto il bot è pronto a ricevere uno dei seguenti comandi:
- /addgame \<game_name\> che permette di aggiungere un gioco alla lista dei preferiti (se il nome non è riconosciuto, viene tornata una lista di suggerimenti)
- /deletegame \<game_name\> che permette di eliminare un gioco dalla lista dei preferiti
- /favoritegames stampa la lista dei preferiti
- /cleargameslist svuota la lista dei preferiti
- /getnews ritorna le 5 notizie più recenti per ogni gioco nella lista dei preferiti
- /checksales verifica se ogni gioco nella lista sia o meno in sconto, a meno che non sia gratuito

All'avvio del bot e ogni 24 ore a partire da quel momento, il bot invierà un messaggio contente la notizia più recente per ogni gioco della lista, così come un messaggio che notifica la presenza di uno sconto o meno.

## Testing 

Per eseguire i test, basta eseguire il seguente comando da terminale:

<code>python -m pytest .\tests\ </code>

Per vedere la code coverage dei test bast invece eseguire il seguente comando da terminale:

<code>python -m pytest --cov src </code>
