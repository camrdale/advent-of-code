from pathlib import Path
import sqlite3

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        with sqlite3.connect(str(Path(__file__).parent.resolve() / 'increases.db')) as con:
            cur = con.cursor()
            cur.execute('DROP TABLE IF EXISTS depths;')
            cur.execute("""
                    CREATE TABLE depths (
                        depth INTEGER,
                        depthID INTEGER PRIMARY KEY AUTOINCREMENT);""")
            cur.executemany('INSERT INTO depths (depth) VALUES(?)', [(val,) for val in input])

            sum_increasing: tuple[int] = cur.execute("""
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
                    ;""").fetchone()

        log(RESULT, 'Number of increasing three-measurement sliding windows:', sum_increasing[0])
        return sum_increasing[0]


part = Part2()

part.add_result(5, """
199
200
208
210
200
207
240
269
260
263
""")

part.add_result(1065)
