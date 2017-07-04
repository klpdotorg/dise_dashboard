CREATE OR REPLACE FUNCTION getslug(texte varchar) RETURNS VARCHAR AS
$$
DECLARE
    result varchar;
BEGIN
    result := replace(texte , 'æ', 'ae');
    result := replace(result , 'œ', 'oe');
    result := replace(result , '€', 'euros');
    result := replace(result , '$', 'dollars');
    result := replace(result , '£', 'pound');
    result := replace(result , '¥', 'yen');
    result := regexp_replace(translate(replace(lower(result), ' ', '-'),
        'áàâãäåāăąÁÂÃÄÅĀĂĄèééêëēĕėęěĒĔĖĘĚìíîïìĩīĭÌÍÎÏÌĨĪĬóôõöōŏőÒÓÔÕÖŌŎŐùúûüũūŭůÙÚÛÜŨŪŬŮçÇÿ&,.ñÑ',
        'aaaaaaaaaaaaaaaaaeeeeeeeeeeeeeeeiiiiiiiiiiiiiiiiooooooooooooooouuuuuuuuuuuuuuuuccy_--nn'), E'[^\\w -]', '', 'g');
    result := regexp_replace(result, E'-+', '-', 'g');
    result := trim(both '-' from result);
    RETURN result;
END;
$$
LANGUAGE PLPGSQL;

UPDATE dise_1516_basic_data
SET cluster_name = 'D.J.HALLI'
WHERE school_code=29280600330;

