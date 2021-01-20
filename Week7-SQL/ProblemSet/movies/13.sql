SELECT
  DISTINCT name
FROM
  people
  JOIN (
    SELECT
      s1.movie_id,
      s1.person_id AS p1_id,
      s2.person_id AS p2_id
    FROM
      stars AS s1
      JOIN stars AS s2 ON s1.movie_id = s2.movie_id
    WHERE
      s1.person_id = (
        SELECT
          id
        FROM
          people
        WHERE
          name = "Kevin Bacon"
      )
      AND
      s2.person_id != (
        SELECT
            id
        FROM
            people
        WHERE
            name = "Kevin Bacon"
      )
  ) AS together ON people.id = together.p2_id;