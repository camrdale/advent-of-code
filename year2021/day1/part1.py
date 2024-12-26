from pathlib import Path
import sqlite3

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part1(Part):
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
                            depth,
                            (CASE WHEN LAG (depth) OVER (ORDER BY depthID) < depth
                             THEN 1
                             ELSE 0
                             END) AS increasing
                        FROM depths
                    ) AS s
                    ;""").fetchone()

        log(RESULT, 'Number of increasing measurements:', sum_increasing[0])
        return sum_increasing[0]


part = Part1()

part.add_result(7, """
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

part.add_result(1121)
