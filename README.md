# Masterblog API - DE

Eine REST-API für Blogbeiträge, entwickelt mit Flask.

## Funktionen

- Blogbeiträge abrufen
- Blogbeiträge nach Titel oder Inhalt sortieren
- Neue Blogbeiträge erstellen
- Blogbeiträge anhand ihrer ID aktualisieren
- Blogbeiträge anhand ihrer ID löschen
- Blogbeiträge nach Titel und/oder Inhalt durchsuchen
- Cross-Origin Resource Sharing (CORS) mit Flask-CORS aktivieren

## Voraussetzungen

- Python 3
- `pip`

## Installation

1. Repository klonen und in das Projektverzeichnis wechseln.
2. Eine virtuelle Umgebung erstellen und aktivieren:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Abhängigkeiten installieren:

   ```bash
   pip install -r requirements.txt
   ```

## Anwendung starten

Die Flask-Anwendung starten:

```bash
python backend_app.py
```

Die API ist anschließend lokal unter `http://127.0.0.1:5003` erreichbar.

## API-Endpunkte

| Methode | Endpunkt | Beschreibung |
| --- | --- | --- |
| `GET` | `/api/posts` | Alle Blogbeiträge abrufen |
| `GET` | `/api/posts?sort=title&direction=asc` | Beiträge nach Titel sortieren |
| `GET` | `/api/posts?sort=content&direction=desc` | Beiträge nach Inhalt absteigend sortieren |
| `POST` | `/api/posts` | Einen neuen Blogbeitrag erstellen |
| `PUT` | `/api/posts/<post_id>` | Einen Blogbeitrag aktualisieren |
| `DELETE` | `/api/posts/<post_id>` | Einen Blogbeitrag löschen |
| `GET` | `/api/posts/search?title=first` | Beiträge nach Titel durchsuchen |
| `GET` | `/api/posts/search?content=first` | Beiträge nach Inhalt durchsuchen |

### Blogbeitrag erstellen

Beispiel für einen JSON-Request an `POST /api/posts`:

```json
{
  "title": "Mein Blogbeitrag",
  "content": "Das ist der Inhalt meines Blogbeitrags."
}
```

Die ID wird automatisch vergeben.

### Blogbeitrag aktualisieren

Beispiel für einen JSON-Request an `PUT /api/posts/1`:

```json
{
  "title": "Aktualisierter Titel"
}
```

Es können `title`, `content` oder beide Felder übergeben werden.

### Sortierung

Die Query-Parameter `sort` und `direction` sind optional:

- `sort`: `title` oder `content`
- `direction`: `asc` oder `desc`

Ohne `sort` werden die Beiträge in ihrer ursprünglichen Reihenfolge zurückgegeben. Ungültige Sortierfelder oder Sortierrichtungen führen zu einer Fehlermeldung mit HTTP-Status `400`.

### Suche

Die Suche ist nicht zwischen Groß- und Kleinschreibung unterscheidend. Die Parameter `title` und `content` können einzeln oder gemeinsam angegeben werden. Ein Beitrag wird höchstens einmal in der Ergebnisliste aufgeführt.

## Hinweise

Die Blogbeiträge werden aktuell in einer Python-Liste im Arbeitsspeicher gespeichert. Änderungen gehen daher verloren, wenn die Anwendung neu gestartet wird.
