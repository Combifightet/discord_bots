# Standard Curicula Plans

Found at the [examination office](https://www.fin.ovgu.de/Studium/Während+des+Studiums/Prüungsamt/Studiendokumente/Regelstudienpl%C3%A4ne.html) (for bachelors only)

> further important [documents](https://www.fin.ovgu.de/Studium/Während+des+Studiums/Prüfungsamt/Studiendokumente.html) from the examination office (for both masters and bachelors)

## Degrees

### Bachelor of Science (B.Sc)

**Main ones:**

- Computervisualistik _(`CV`)_
- Informatik _(`INF`)_
- Ingenieursinformatik _(`IngINF`)_
- Wirtschaftsinformatik _(`WIF`)_

**Others:**

- Ai Engineering _(`AiEng`)_ (in kooperatin mit der Fakultät für Maschienen Bau)
- Bilinguale Informatik _(`BiBa INF`)_

### Master of Science (M.Sc)

**Main ones:**

- Informatik _(`INF`)_
- Ingenieursinformatik _(`IngINF`)_
- Visual Computing _(`VC`)_
- Wirtschaftsinformatik _(`WIF`)_

**Others:**

- Data and Knowledge Engineering _(`DKE`)_
- Digital Engineering _(`DE`)_
- Computervisualistik _(`CV`)_ (propably discontuined)

## Json Format

```json
{

  "spo": 2024,
  "degree": "CV",
  "isMaster": false,
  "isWinter": true,
  "totalSemesters": 7,
  "totalCredits": 210,
  "moduleGroups": [
    {
      ...
    },
    {
      ...
    },
    ...
  ]
}
```

Eeach moduleGroups is its own json object as follows:

```json
{
  "category": "pf",
  "totalCredits": 10,
  "minGradedCredits": 5,
  "weight": 50,
  "modules": [
    {
      ...
    },
    ...
  ]
}
```

And each module looks as follows:

```json
{
  "id": "EinfInf",
  "credits": 10,
  "semester": 1,
  "altSemester": 2
}
```

> category can be `null`, if it doesnt have one (like the thesis)

| name | category | relevant bachelors |
|------|:--------:|------------------|
| **Informatik Pflicht**           | `'pf'`    | _cv_ \| _inf_ \| _inginf_ |
| **Informatik Pflicht 2**         | `'pf2'`   | _inf_ \| _inginf_ |
| **Informatik Wahlpflicht**       | `'wpf'`   | _cv_ \| _inf_ \| _inginf_ |
| **Technische Informatik**        | `'tech'`  | _inf_ \| _inginf_ |
| **Computervisualistik**          | `'cv'`    | _cv_ |
| **Mathematik / Logik**           | `'m'`     | _cv_ \| _inf_ \| _inginf_ |
| **Mathematik /<br>Theoretische Informatik**  | `'theo'`  | _cv_ \| _inf_ \| _inginf_ |
| **Ingeneiurbereich (IB)**        | `'ib'`    | _inginf_ |
| **Anwendungsfach**               | `'apl'`   | _cv_ |
| **Allgemeine Visualistik**       | `'allgv'` | _cv_ |
| **Nebenfach**                    | `'minor'` | _inf_ |
| **Verstehen**                    | `'ver'`   | _wif_ |
| **Wahlpflicht Verstehen<br>und Gestalten**   | `'ve_ge'` | _wif_ |
| **Gestalten**                    | `'ges'`   | _wif_ |
| **Wahlpflicht Gestalten<br>und Anwenden**    | `'ge_an'` | _wif_ |
| **Anwenden**                     | `'anw'`   | _wif_ |
| **Schlüssel- und <br> Methoden kompetenzen** | `'smk'`   | _cv_ \| _inf_ \| _inginf_ |
