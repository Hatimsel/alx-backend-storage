-- a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.


DELIMITER //


CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE id INT;
	DECLARE sum_of_scores INT;
	DECLARE sum_of_weights INT;
	DECLARE avg_score INT;
	DECLARE counter INT;
	DECLARE max_count INT;

	SET id = user_id;
	CREATE TEMPORARY student_corrections AS
	SELECT * FROM corrections
	WHERE user_id = id;

	SELECT SUM(score) INTO sum_of_scores FROM student_corrections;

	ALTER TABLE student_corrections DROP PRIMARY KEY;
	ALTER TABLE student_corrections AUTO_INCREMENT = 1;
	ALTER TABLE student_corrections ADD PRIMARY KEY (id) AUTO_INCREMENT;

	SELECT MAX(id) INTO max_count FROM student_corrections;

	CREATE TABLE student_projects (
		id INT NOT NULL AUTO_INCREMENT,
		name VARCHAR(255) NOT NULL,
		weight INT DEFAULT 1,
		PRIMARY KEY (id)
	);
	SET counter = 1;
	WHILE counter < max_count DO
		DECLARE name VARCHAR(255) NOT NULL;
		DECLARE weight INT DEFAULT 1;

		SELECT name, weight INTO name, weight
		FROM student_corrections
		WHERE id = counter;

		INSERT INTO student_projects (name, weight) VALUES (name, weight);

		SET counter = counter + 1;
	END WHILE;

	SET counter = 1;

	WHILE counter < max_count DO
		CREATE TABLE score_weight(
			score INT,
			weight INT
		)

		INSERT INTO score_weight (score) VALUES (
			SELECT score
			FROM student_corrections
			WHERE id = counter)
		INSERT INTO score_weight (weight) VALUES (
			SELECT weight
			FROM student_projects
			WHERE id = counter)

		SET counter = counter + 1;
	END WHILE;

	SELECT score * weight AS result FROM score_weight;
	SELECT SUM(result) INTO sum_of_scores FROM score_weight;
	SELECT SUM(weight) INTO sum_of_weights FROM student_projects;

	SET avg_score = sum_of_scores / sum_of_weights;
	UPDATE users SET average_score = avg_score WHERE id = user_id;

END;

//

DELIMITER ;
