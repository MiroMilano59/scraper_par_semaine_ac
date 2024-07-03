# Diagramme de Films

```mermaid
classDiagram
  class Film {
    +String titre
    +String genre
    +String acteurs
    +int anneeSortie
    +float note
    +String realisateur
    +String descriptif
    +int duree
    +String paysOrigine
  }
  Film "1" -- "0..*" Genre
  Film "1" -- "0..*" Acteur
  Film "1" -- "0..*" Realisateur
  Film "1" -- "0..1" PaysOrigine

  class Genre {
    +String nom
  }

  class Acteur {
    +String nom
  }

  class Realisateur {
    +String nom
  }

  class PaysOrigine {
    +String nom
  }
