DROP TABLE IF EXISTS depths;
CREATE TABLE depths (
  depth INTEGER,
  depthID INTEGER PRIMARY KEY AUTOINCREMENT);

.mode csv
.import input.txt depths

SELECT
  SUM(increasing)
FROM (
  SELECT
    depth,
    (CASE WHEN LAG (depth) OVER (ORDER BY depthID) < depth
     THEN 1
     ELSE 0
     END) AS increasing
  FROM depths
) AS s
;

SELECT
  SUM(increasing)
FROM (
  SELECT
    depth_window,
    (CASE WHEN LAG (depth_window) OVER (ORDER BY depthID) < depth_window
     THEN 1
     ELSE 0
     END) AS increasing
  FROM (
    SELECT
      depth + depth_1 + depth_2 AS depth_window,
      depthID
    FROM (
      SELECT
        depthID,
        depth,
        LAG (depth, 1) OVER (ORDER BY depthID) AS depth_1,
        LAG (depth, 2) OVER (ORDER BY depthID) AS depth_2
      FROM depths
    )
    WHERE
      depth_2 IS NOT NULL
  )
)
;
