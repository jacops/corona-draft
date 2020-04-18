# Corona Draft

Wsparcie dla piłkarskiego draftu poprzez integracjęz Google Spreadsheets + Twitter.

## Wymagania softwarowe

* Docker (https://docs.docker.com/get-docker/)
* Makefile (opcjonalnie)

> Jeśli nie posiadasz Make, otwórz w edytorze tekstowym plik `Makefile` i skopiuj polecenie danego tasku do lini poleceń.
> Np: `make docker-build` to będzie: `docker-compose build`

## Setup

* Utwórz Google spreadsheet na podstawie `samples/tournament.xlsx`. Nazwa spreadsheetu, będzie nazwą turnieju
* Zbuduj Docker image - `make build` 
* Pobierz plik do głównego katalogu `credentials.json` (https://developers.google.com/sheets/api/quickstart/python -> Step 1)
* Przekonwertuj ściągnięty plik na binarkę: `make generate-token-pickle`
* Utwórz plik `.env` na podstawie `.env.dist`
    * Uzupełnij `SPREADSHEET_ID` wklejając ID Google spreadsheetu, który utworzyłeś na początku
    * Uzupełnij `TOKEN_PICKLE` wartością polecenia `cat token.pickle|base64`
    * Uzupełnij klucze dla Twittera (https://docs.inboundnow.com/guide/create-twitter-application/)
    
* Zacznij turniej `make docker-start-tournament`
* Gracze mogą uzupełniać spreadsheet
* By ogłosić postęp draftu na Tweeterze, uruchom: `make docker-worker`

