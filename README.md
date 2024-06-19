# BionicRead API : Lisez vos ebooks plus vite et plus efficacement
BionicRead est une API qui vous permet de convertir vos ebooks au format .epub en format "lecture bionique". La lecture bionique est une nouvelle méthode de lecture qui vise à améliorer la vitesse et la compréhension de la lecture en utilisant des points de fixation artificiels pour guider les yeux du lecteur à travers le texte.

### Fonctionnement de l'API:

1) Envoyez un requête POST à l'adresse ```/epub-to-bionic``` avec un fichier ebook ```.epub``` en pièce jointe.
2) L'API convertira votre ebook en format "lecture bionique".
3) Le fichier converti sera renvoyé dans la réponse de l'API.

### Technologies utilisées:

- Python: Langage de programmation pour le développement de l'API.
- Flask: Framework web Python pour la création de l'API.
- Docker: Outil de conteneurisation pour l'empaquetage de l'API dans une image docker.

## Qu'est-ce que la lecture bionique ?

La lecture bionique est une nouvelle méthode de lecture qui utilise des points de fixation artificiels pour guider les yeux du lecteur à travers le texte. Ces points de fixation sont généralement les premières lettres de chaque mot, qui sont mises en gras ou en couleur.

L'idée derrière la lecture bionique est que le cerveau humain est plus efficace pour reconnaître les mots lorsqu'il ne se concentre que sur les premières lettres. En guidant les yeux du lecteur vers ces points de fixation, la lecture bionique peut aider à augmenter la vitesse de lecture et à améliorer la compréhension.

## Avantages de la lecture bionique:

- Augmentation de la vitesse de lecture
- Amélioration de la compréhension
- Réduction de la fatigue oculaire
- Meilleure concentration