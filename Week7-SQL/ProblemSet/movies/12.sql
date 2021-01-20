SELECT
  title
FROM
  movies
  JOIN (
    SELECT
      s1.movie_id,
      s1.person_id,
      s2.person_id
    FROM
      (
        stars AS s1
        JOIN stars AS s2 ON s1.movie_id = s2.movie_id
      )
    WHERE
      s1.person_id = (
        SELECT
          id
        FROM
          people
        WHERE
          name = "Johnny Depp"
      )
      AND s2.person_id = (
        SELECT
          id
        FROM
          people
        WHERE
          name = "Helena Bonham Carter"
      )
  ) AS starsJoined ON movies.id = starsJoined.movie_id;
