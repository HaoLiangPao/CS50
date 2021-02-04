SELECT
  DISTINCT movie_stars.title
FROM
  (
    SELECT
      movies.id AS id, movies.title AS title
    FROM
      movies
      JOIN stars ON movies.id = stars.movie_id
    WHERE
      stars.person_id = (
        SELECT
          id
        FROM
          people
        WHERE
          name = "Chadwick Boseman"
      )
  ) AS movie_stars
  JOIN ratings ON movie_stars.id = ratings.movie_id
ORDER BY
  ratings.rating DESC
LIMIT
  5;
