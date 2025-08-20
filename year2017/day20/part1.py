from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day20.shared import Particle

class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        particles: list[Particle] = []
        for i, line in enumerate(input):
            particles.append(Particle(i, line))

        # Eventually, all particles will be forever moving away from the origin.
        max_time_all_moving_outward = 0
        for particle in particles:
            time_moving_outward = particle.when_moving_outward()
            if time_moving_outward > max_time_all_moving_outward:
                max_time_all_moving_outward = time_moving_outward
                log.log(log.INFO, f'Latest time for all moving outeward is now {max_time_all_moving_outward} due to particle {particle.num}')

        # Advance all particles to that time.
        for particle in particles:
            particle.advance(max_time_all_moving_outward)
            assert particle.moving_outward(), particle

        # Once particles are all forever moving away from the origin,
        # sort them by the magnitude of their accel/vel/pos. The
        # slowest will eventually be the closest to the origin.
        particles.sort()
        log.log(log.DEBUG, 'Slowest 10 particles:', particles[:10])

        log.log(log.RESULT, f'The slowest particle: {particles[0]}')
        return particles[0].num


part = Part1()

part.add_result(0, """
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
""")

part.add_result(344)
