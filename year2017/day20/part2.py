import collections

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate3D
from aoc.runner import Part

from year2017.day20.shared import Particle


class Part2(Part):
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

        t = 0
        escapees = 0
        while particles:
            # Determine which particles are in the same position (colliding)
            particle_positions: dict[Coordinate3D, list[Particle]] = collections.defaultdict(list)
            found_collision = False
            for particle in particles:
                particle_positions[particle.p].append(particle)
                found_collision |= len(particle_positions[particle.p]) > 1
            if found_collision:
                particles = [particle for particle in particles if len(particle_positions[particle.p]) == 1]
                log.log(log.INFO, f't={t}: After removing collisions, particles remaining: {len(particles)}')

            if t > max_time_all_moving_outward:
                # Once particles are all moving away from the origin,
                # sort them by the magnitude of their accel/vel/pos.
                particles.sort()

                # Find which particles are furthest from the origin.
                positions = [particle.manhattan_distance() for particle in particles]
                positions.sort()

                # Any particle that has the maximum magnitude of accel/vel/pos
                # and is also the furthest from the origin can never be caught
                # by any other particle, so it has escaped.
                found_escapee = particles[-1].manhattan_distance() == positions[-1]
                while particles and particles[-1].manhattan_distance() == positions[-1]:
                    log.log(log.DEBUG, f'Escapee: {particles[-1].magnitude()} {particles[-1]}')
                    particles.pop()
                    positions.pop()
                    escapees += 1
                if found_escapee:
                    log.log(log.INFO, f't={t} After removing escapees, particles remaining: {len(particles)}')

            # Simulate movement to the next time tick.
            for particle in particles:
                particle.advance(1)
            t += 1

        log.log(log.RESULT, f'After {t} ticks, particles escaped: {escapees}')
        return escapees


part = Part2()

part.add_result(1, """
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
""")

part.add_result(404)
