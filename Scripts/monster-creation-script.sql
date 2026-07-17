

set @MonsterName = '';
set @MonsterType = '';
set @MonsterFloor = 0;
set @MonsterBaseVariance = 0;
set @MonsterHP = 0;
set @MonsterAttackRating = 0;
set @MonsterDamageReduction = 0;
set @MonsterEvasion = 0;
set @MonsterCritChance = 0;
set @MonsterWeakness = JSON_ARRAY('', '');
set @MonsterResistance = JSON_ARRAY('', '');

set @DropXP = 0;
set @DropGold = 0;
set @DropLoot = JSON_ARRAY('', '');
set @DropRaidLoot = JSON_ARRAY('', '');
set @DropSpecialLoot = JSON_ARRAY('', '');

set @AIActionsList = JSON_ARRAY('', '');
set @AIHPThresholdLower = 0;
set @AIHPThresholdUpper = 0;

set @MonsterAI =
    JSON_OBJECT(
        'Actions', JSON_ARRAY(
            JSON_OBJECT(
                'Action', @AIActionsList,
                'HPThresholdLower', @AIHPThresholdLower,
                'HPThresholdUpper', @AIHPThresholdUpper
       )
   )

);

set @DropTable = JSON_OBJECT(
     'XP', @DropXP,
     'Gold', @DropGold,
     'Loot', @DropLoot,
     'RaidLoot', @DropRaidLoot,
     'SpecialLoot', @DropSpecialLoot
);

DELIMITER //
CREATE PROCEDURE create_monster()
    BEGIN
        Declare EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            ROLLBACK;
        END;
        START TRANSACTION;
            INSERT INTO monster (
                                 floor,
                                 type,
                                 name,
                                 weakness,
                                 resistance,
                                 baseVariance,
                                 hp,
                                 attackRating,
                                 damageReduction,
                                 evasion,
                                 critChance,
                                 ai,
                                 dropTable
                                )
            VALUES              (
                                @MonsterFloor,
                                @MonsterType,
                                @MonsterName,
                                @MonsterWeakness,
                                @MonsterResistance,
                                @MonsterBaseVariance,
                                @MonsterHP,
                                @MonsterAttackRating,
                                @MonsterDamageReduction,
                                @MonsterEvasion,
                                @MonsterCritChance,
                                @MonsterAI,
                                @DropTable
                                );
            COMMIT;
    END//
DELIMITER ;

CALL create_monster();
DROP PROCEDURE create_monster;

