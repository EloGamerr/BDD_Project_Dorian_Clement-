CREATE TRIGGER medailles
BEFORE INSERT ON LesResultats
WHEN (NOT NEW.gold IS NULL OR NOT NEW.silver IS NULL OR NOT NEW.bronze IS NULL)
    AND (NEW.gold IS NULL OR NEW.silver IS NULL OR NEW.bronze IS NULL)
BEGIN
    SELECT RAISE(ABORT, 'Les 3 medailles doivent etre attribuees en meme temps');
END;
\