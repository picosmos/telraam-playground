# Secrets

- API Keys und andere Authentifizierungsmethoden sollten nicht mit im Repository landen, daher sind diese in der `our_secrets.py` enthalten. Lediglich eine Version ohne konkrete Keys ist im Repo verfügbar. Diese sind entsprechend vor dem Ausführen zu ergänzen.
- Die `our_secrets.py` ist außerdem in der `.gitignore` eingetragen.

# Telraam

Die Daten werden von folgendem Endpunkt abgerufen: https://documenter.getpostman.com/view/8210376/TWDRqyaV#476370b0-48be-4092-8930-11be1990b35c

Wir rufen uns lediglich die Daten ab, die innerhalb der Boundaries der Gemeinden liegen. D.h. auch, dass wir u.U. Daten aus Nachbargemeinden bekommen. Der einfachheit halber ignorieren wir das aber.

Namen, code style etc. sind alle unglaublich unordentlich...das aufzuräumen ist dem Leser überlassen