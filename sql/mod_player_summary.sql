ALTER TABLE player_summary
  DROP COLUMN IF EXISTS efficiency_score;

ALTER TABLE player_summary
  ADD COLUMN efficiency_score
  numeric GENERATED ALWAYS AS (achievement_count::numeric / NULLIF(playtime_forever, 0)) STORED;

BEGIN;

ALTER TABLE player_summary
  ADD COLUMN IF NOT EXISTS max_survive_minutes int,
  ADD COLUMN IF NOT EXISTS max_zombie_kills int,
  ADD COLUMN IF NOT EXISTS max_player_kills int,
  ADD COLUMN IF NOT EXISTS max_travel int,
  ADD COLUMN IF NOT EXISTS max_level int,
  ADD COLUMN IF NOT EXISTS max_fortitude int,
  ADD COLUMN IF NOT EXISTS max_die_days int;

UPDATE player_summary ps
SET
  max_survive_minutes = GREATEST(
    COALESCE(p."Life60Minute",0)*60,
    COALESCE(p."Life180Minute",0)*180,
    COALESCE(p."Life600Minute",0)*600,
    COALESCE(p."Life1680Minute",0)*1680,
    0
  ),
  max_zombie_kills = GREATEST(
    COALESCE(p."Zombies10",0)*10,
    COALESCE(p."Zombies100",0)*100,
    COALESCE(p."Zombies500",0)*500,
    COALESCE(p."Zombies2500",0)*2500,
    0
  ),
  max_player_kills = GREATEST(
    COALESCE(p."Players1",0)*1,
    COALESCE(p."Players5",0)*5,
    COALESCE(p."Players10",0)*10,
    COALESCE(p."Players25",0)*25,
    0
  ),
  max_travel = GREATEST(
    COALESCE(p."Travel10",0)*10,
    COALESCE(p."Travel50",0)*50,
    COALESCE(p."Travel250",0)*250,
    COALESCE(p."Travel1000",0)*1000,
    0
  ),
  max_level = GREATEST(
    COALESCE(p."Level7",0)*7,
    COALESCE(p."Level28",0)*28,
    COALESCE(p."Level70",0)*70,
    COALESCE(p."Level140",0)*140,
    COALESCE(p."Level300",0)*300,
    0
  ),
  max_fortitude = GREATEST(
    COALESCE(p."Fortitude4",0)*4,
    COALESCE(p."Fortitude6",0)*6,
    COALESCE(p."Fortitude8",0)*8,
    COALESCE(p."Fortitude10",0)*10,
    0
  ),
  max_die_days = GREATEST(
    COALESCE(p."Die1",0)*1,
    COALESCE(p."Die7",0)*7,
    COALESCE(p."Die14",0)*14,
    COALESCE(p."Die28",0)*28,
    0
  )
FROM players_7dtd p
WHERE p.steamid = ps.steamid;

COMMIT;
