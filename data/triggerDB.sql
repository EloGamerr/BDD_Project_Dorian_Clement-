CREATE TRIGGER medailles1
BEFORE INSERT ON LesResultats
WHEN (NOT NEW.gold IS NULL OR NOT NEW.silver IS NULL OR NOT NEW.bronze IS NULL)
    AND (NEW.gold IS NULL OR NEW.silver IS NULL OR NEW.bronze IS NULL)
BEGIN
    SELECT RAISE(ABORT, 'Les 3 medailles doivent etre attribuees en meme temps');
END;
\

CREATE TRIGGER medailles2
BEFORE UPDATE OF gold, silver, bronze
ON LesResultats
WHEN (NOT NEW.gold IS NULL OR NOT NEW.silver IS NULL OR NOT NEW.bronze IS NULL)
    AND (NEW.gold IS NULL OR NEW.silver IS NULL OR NEW.bronze IS NULL)
BEGIN
    SELECT RAISE(ABORT, 'Les 3 medailles doivent etre attribuees en meme temps');
END;
\

CREATE TRIGGER NombreFixSportifs1
BEFORE INSERT
ON LesInscriptions
WHEN (NOT (SELECT nbSportifsEp FROM LesEpreuves WHERE NEW.numEp=numEp) IS NULL) AND ((SELECT nbSportifsEp FROM LesEpreuves WHERE NEW.numEp=numEp) != (SELECT COUNT(numSp) FROM LesEquipiers WHERE NEW.numIn=numEq))
BEGIN
  SELECT RAISE(ABORT, 'La taille de l equipe ne correspond pas a la taille qu il faut pour l epreuve.');
END;
\

CREATE TRIGGER NombreFixSportifs2
BEFORE UPDATE OF numEp, numIn
ON LesInscriptions
WHEN (NOT (SELECT nbSportifsEp FROM LesEpreuves WHERE NEW.numEp=numEp) IS NULL) AND ((SELECT nbSportifsEp FROM LesEpreuves WHERE NEW.numEp=numEp) != (SELECT COUNT(numSp) FROM LesEquipiers WHERE NEW.numIn=numEq))
BEGIN
  SELECT RAISE(ABORT, 'La taille de l equipe ne correspond pas a la taille qu il faut pour l epreuve.');
END;
\

CREATE TRIGGER RespectForme1
BEFORE INSERT
ON LesInscriptions
WHEN (((SELECT formeEp FROM LesEpreuves WHERE numEp=NEW.numEp) != 'individuelle' AND NEW.numIn >= 1000) OR ((SELECT formeEp FROM LesEpreuves WHERE numEp=NEW.numEp) = 'individuelle' AND NEW.numIn < 1000))
BEGIN
	SELECT RAISE(ABORT, 'Ce participant ne respecte pas la forme de l epreuve');
END;
\

CREATE TRIGGER RespectForme2
BEFORE UPDATE
ON LesInscriptions
WHEN (((SELECT formeEp FROM LesEpreuves WHERE numEp=NEW.numEp) != 'individuelle' AND NEW.numIn >= 1000) OR ((SELECT formeEp FROM LesEpreuves WHERE numEp=NEW.numEp) = 'individuelle' AND NEW.numIn < 1000))
BEGIN
	SELECT RAISE(ABORT, 'Ce participant ne respecte pas la forme de l epreuve');
END;
\

CREATE TRIGGER RespectCategorie1
BEFORE INSERT
ON LesInscriptions
WHEN (SELECT categorieEp FROM LesEpreuves WHERE numEp=NEW.numEp) != 'mixte' AND NEW.numIn < 1000
AND (((SELECT categorieEp FROM LesEpreuves WHERE numEp=NEW.numEp) = 'masculin' AND (SELECT COUNT(*) FROM LesEquipes NATURAL JOIN LesEquipiers NATURAL JOIN LesSportifs WHERE numEq=NEW.numIn AND categorieSp='feminin') > 0)
OR ((SELECT categorieEp FROM LesEpreuves WHERE numEp=NEW.numEp) = 'feminin' AND (SELECT COUNT(*) FROM LesEquipes NATURAL JOIN LesEquipiers NATURAL JOIN LesSportifs WHERE numEq=NEW.numIn AND categorieSp='masculin') > 0))
BEGIN
    SELECT RAISE(ABORT, 'Cette equipe ne respecte pas la categorie de l epreuve');
END;
\

CREATE TRIGGER RespectCategorie2
BEFORE UPDATE
ON LesInscriptions
WHEN (SELECT categorieEp FROM LesEpreuves WHERE numEp=NEW.numEp) != 'mixte' AND NEW.numIn < 1000
AND (((SELECT categorieEp FROM LesEpreuves WHERE numEp=NEW.numEp) = 'masculin' AND (SELECT COUNT(*) FROM LesEquipes NATURAL JOIN LesEquipiers NATURAL JOIN LesSportifs WHERE numEq=NEW.numIn AND categorieSp='feminin') > 0)
OR ((SELECT categorieEp FROM LesEpreuves WHERE numEp=NEW.numEp) = 'feminin' AND (SELECT COUNT(*) FROM LesEquipes NATURAL JOIN LesEquipiers NATURAL JOIN LesSportifs WHERE numEq=NEW.numIn AND categorieSp='masculin') > 0))
BEGIN
    SELECT RAISE(ABORT, 'Cette equipe ne respecte pas la categorie de l epreuve');
END;
\