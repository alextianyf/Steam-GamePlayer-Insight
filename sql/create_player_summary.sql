-- design to overwrite the previoys player_summary
DROP TABLE IF EXISTS player_summary;

-- create player_summary
CREATE TABLE player_summary AS
SELECT
  steamid, playtime_forever,

  -- calcuate the total count
  (
    ("StoneAxe" + "WoodFrame" + "Bedroll" + "LandClaim"
     + "Items50" + "Items500" + "Items1500" + "Items5000")
  + ("Zombies10" + "Zombies100" + "Zombies500" + "Zombies2500")
  + ("Players1" + "Players5" + "Players10" + "Players25")
  + ("BleedOut" + "LegBreak" + "Kills44Mag")
  + ("Fortitude4" + "Fortitude6" + "Fortitude8" + "Fortitude10")
  + ("Travel10" + "Travel50" + "Travel250" + "Travel1000" + "Height255" + "Height0")
  + ("Die1" + "Die7" + "Die14" + "Die28")
  + ("Level7" + "Level28" + "Level70" + "Level140" + "Level300")
  + ("Life60Minute" + "Life180Minute" + "Life600Minute" + "Life1680Minute" + "SubZeroNaked")
  ) 																					AS achievement_count,

  -- calculate category count
  ("StoneAxe" + "WoodFrame" + "Bedroll" + "LandClaim"
   + "Items50" + "Items500" + "Items1500" + "Items5000")                    			AS crafting_count,

  ("Players1" + "Players5" + "Players10" + "Players25")                      			AS player_killer_count,

  ("BleedOut" + "LegBreak" + "Kills44Mag" + "Zombies10"
  + "Zombies100" + "Zombies500" + "Zombies2500" 
  + "Fortitude4" + "Fortitude6" + "Fortitude8" + "Fortitude10")                       AS combat_count,

  ("Travel10" + "Travel50" + "Travel250" + "Travel1000" + "Height255" + "Height0") 	AS exploration_count,

  ("Die1" + "Die7" + "Die14" + "Die28")                                      			AS death_count,

  ("Level7" + "Level28" + "Level70" + "Level140" + "Level300")              			AS leveling_count,

  ("Life60Minute" + "Life180Minute" + "Life600Minute"
   + "Life1680Minute" + "SubZeroNaked")                                      			AS survival_count

FROM players_7dtd;

