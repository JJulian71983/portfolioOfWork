CREATE SCHEMA michael_jordan;
CREATE TABLE practice_db.michael_jordan.basketball_statistics
(
    row_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    year VARCHAR,
    team VARCHAR,
    games_played NUMERIC(2,0),
    minutes_per_game NUMERIC(3,1),
    points_per_game NUMERIC(3,1),
    rebounds_per_game NUMERIC(3,1),
    assists_per_game NUMERIC(3,1),
    steals_per_game NUMERIC(3,1)
);
INSERT INTO practice_db.michael_jordan.basketball_statistics
(
    year,
    team,
    games_played,
    minutes_per_game,
    points_per_game,
    rebounds_per_game,
    assists_per_game,
    steals_per_game
)
VALUES
('1984-85','Bulls',82,38.3,28.2,6.5,5.9,2.4),
('1985-86','Bulls',18,25.1,22.7,3.6,2.9,2.1),
('1986-87','Bulls',82,40.0,37.1,5.2,4.6,2.9),
('1987-88','Bulls',82,40.4,35.0,5.5,5.9,3.2),
('1988-89','Bulls',81,40.2,32.5,8.0,8.0,2.9),
('1989-90','Bulls',82,39.0,33.6,6.9,6.3,2.8),
('1990-91','Bulls',82,37.0,31.5,6.0,5.5,2.7),
('1991-92','Bulls',80,38.8,30.0,6.4,6.1,2.3),
('1992-93','Bulls',78,39.3,32.6,6.7,5.5,2.8),
('1994-95','Bulls',17,39.3,26.9,6.9,5.3,1.8),
('1995-96','Bulls',82,37.7,30.4,6.6,4.3,2.2),
('1996-97','Bulls',82,37.9,29.6,5.9,4.3,1.7),
('1997-98','Bulls',82,38.8,28.7,5.8,3.5,1.7);
SELECT
    year,
    points_per_game,
    assists_per_game,
    steals_per_game
FROM
    practice_db.michael_jordan.basketball_statistics;