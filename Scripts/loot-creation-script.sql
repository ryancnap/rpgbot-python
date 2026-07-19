-- Config 1/2: Set base loot values
SET @LootName = 'Test Loot';
SET @LootDescription = 'Test Loot Description';
SET @LootType = 'Test Loot Type';
SET @LootBaseVariance = 0;
SET @LootRarity = 'Test Loot Rarity';

-- Config 2/2: Set values to build this loot's `baseEffects` properties
SET @Heal = 0;
SET @Type = '';
SET @MaxAP = 0;
SET @MaxHP = 0;
SET @Evasion = 0;
SET @CritChance = 0;
SET @SpellDamage = 0;
SET @AttackRating = 0;
SET @DamageReduction = 0;
SET @UseList = JSON_ARRAY('', '');

-- Do not config: builds JSON object for `baseEffects` record from Config 2/2 above
SET @LootBaseEffects = JSON_OBJECT(
                       'Use', JSON_EXTRACT(@UseList, '$'),
                       'Heal', @Heal,
                       'Type', @Type,
                       'MaxAP', @MaxAP,
                       'MaxHP', @MaxHP,
                       'Evasion', @Evasion,
                       'CritChance', @CritChance,
                       'SpellDamage', @SpellDamage,
                       'AttackRating', @AttackRating,
                       'DamageReduction', @DamageReduction
                       );

DROP PROCEDURE IF EXISTS create_loot;
DELIMITER //
CREATE PROCEDURE create_loot()
    BEGIN
        DECLARE LootName VARCHAR(32);
        DECLARE LootDescription VARCHAR(1000);
        DECLARE LootType VARCHAR(11);
        DECLARE LootBaseVariance INT;
        DECLARE LootRarity VARCHAR(11);
        DECLARE LootBaseEffects JSON;
        DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                RESIGNAL;
            END;
        SET LootName = @LootName;
        SET LootDescription = @LootDescription;
        SET LootType = @LootType;
        SET LootBaseVariance = @LootBaseVariance;
        SET LootRarity = @LootRarity;
        SET LootBaseEffects = @LootBaseEffects;

        START TRANSACTION;
            INSERT INTO loot (name, description, type, baseEffects, baseVariance, rarity)
            VALUES (LootName, LootDescription, LootType, LootBaseEffects, LootBaseVariance, LootRarity);
        COMMIT;

    END//
DELIMITER ;
CALL create_loot();
DROP PROCEDURE IF EXISTS create_loot;