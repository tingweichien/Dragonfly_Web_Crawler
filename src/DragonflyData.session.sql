-- SELECT DATE_FORMAT("2009-09-04",' %Y, %m, %d');
-- SELECT * FROM dragonfly_db.aeshnidae01 WHERE Dates BETWEEN '2018-01-01' AND '2020-07-19';
-- SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dragonfly_db';
-- SELECT MONTH(Dates), COUNT(*) FROM dragonfly_db.aeshnidae01 WHERE Dates BETWEEN '2018-01-01' AND '2020-07-19' GROUP BY MONTH(Dates) ORDER BY MONTH(Dates);
-- SELECT YEAR(Dates), MONTH(Dates), COUNT(*) FROM dragonfly_db.aeshnidae01 WHERE Dates BETWEEN '2018-01-01' AND '2020-07-19' GROUP BY YEAR(Dates), MONTH(Dates) ORDER BY YEAR(Dates), MONTH(Dates);
-- SELECT YEAR(Dates), City, COUNT(*) FROM dragonfly_db.coenagrionidae08 WHERE Dates BETWEEN '2010-01-01' AND '2020-07-19' GROUP BY YEAR(Dates),City

-- SELECT COUNT(*) FROM dragonfly_db.aeshnidae01
SELECT DATE(Dates), ID FROM dragonfly_db.aeshnidae01
