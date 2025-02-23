import queue
import threading
import time

from aoc import log

from year2019 import intcode


class NonblockingQueue(queue.Queue[int]):
    """A wrapper for an intcode input queue that never blocks."""

    def __init__(self, nic: int):
        super().__init__()
        self.nic = nic
        self.lock = threading.Lock()
        self.idle = True

    def empty(self) -> bool:
        return False
    
    def get(self, block: bool = True, timeout: float | None = None) -> int:
        with self.lock:
            try:
                return super().get(block=False)
            except queue.Empty as _:
                if not self.idle:
                    log.log(log.DEBUG, f'  NIC-{self.nic} is now idle')
                self.idle = True
        time.sleep(0.001)
        return -1

    def get_blocking(self) -> int:
        return super().get()
    
    def put_xy(self, x: int, y: int) -> None:
        """Ensures x and y are in the queue, so -1 is never returned for y."""
        with self.lock:
            if self.idle:
                log.log(log.DEBUG, f'  NIC-{self.nic} no longer idle')
            self.idle = False
            self.put(x)
            self.put(y)


class BatchingQueue(queue.Queue[int]):
    """A wrapper for an intcode output queue that batches 3 outputs together."""

    def __init__(self, nic: int, router_queue: queue.Queue[tuple[int, int, int]]):
        super().__init__()
        self.nic = nic
        self.router_queue = router_queue
        self.batched: list[int] = []

    def put(self, item: int, block: bool = True, timeout: float | None = None) -> None:
        self.batched.append(item)
        if len(self.batched) == 3:
            log.log(log.DEBUG, f'  NIC-{self.nic} sent to {self.batched[0]}: x={self.batched[1]},y={self.batched[2]}')
            self.router_queue.put((self.batched[0], self.batched[1], self.batched[2]))
            self.batched = []

    def is_idle(self) -> bool:
        return len(self.batched) == 0


class NicRouter(threading.Thread):
    def __init__(self, intcode_input: list[int], num_nics: int):
        super().__init__(name='ROUTER', daemon=True)
        self.intcode_input = intcode_input
        self.num_nics = num_nics
        self._nic_queues: dict[int, NonblockingQueue] = {}
        self.nic_queues_lock: threading.Lock = threading.Lock()
        self.nics: dict[int, intcode.Program] = {}
        self._router_queue: queue.Queue[tuple[int, int, int]] = queue.Queue()
        self._router_queues: dict[int, BatchingQueue] = {}

    def get_queue(self, nic: int) -> NonblockingQueue:
        with self.nic_queues_lock:
            if nic not in self._nic_queues:
                self._nic_queues[nic] = NonblockingQueue(nic)
        return self._nic_queues[nic]
        
    def get_router_queue(self, nic: int) -> BatchingQueue:
        with self.nic_queues_lock:
            if nic not in self._router_queues:
                self._router_queues[nic] = BatchingQueue(nic, self._router_queue)
        return self._router_queues[nic]

    def run(self) -> None:
        log.log(log.INFO, f'{self.name}: is starting')
        with self.nic_queues_lock:
            for nic in range(self.num_nics):
                nic_queue = NonblockingQueue(nic)
                nic_queue.put_nowait(nic)
                self._nic_queues[nic] = nic_queue
                self._router_queues[nic] = BatchingQueue(nic, self._router_queue)
            for nic in range(self.num_nics):
                nic_program = intcode.Program(f'NIC-{nic}', self.intcode_input)
                nic_program.execute(self._nic_queues[nic], self._router_queues[nic])
        log.log(log.INFO, f'{self.name}: done starting NICs')
        while True:
            destination, x, y = self._router_queue.get()
            if destination == -1:
                break
            with self.nic_queues_lock:
                nic_queue = self._nic_queues[destination]
                nic_queue.put_xy(x, y)
        log.log(log.INFO, f'{self.name}: is done')
    
    def is_idle(self) -> bool:
        with self.nic_queues_lock:
            if not self._router_queue.empty():
                return False
            for nic in range(self.num_nics):
                if nic not in self._nic_queues:
                    # Still starting up
                    return False
            for nic_queue in self._nic_queues.values():
                if not nic_queue.idle:
                    return False
            for router_queue in self._router_queues.values():
                if not router_queue.is_idle():
                    return False
        return self._router_queue.empty()


class NAT(threading.Thread):
    def __init__(self, router: NicRouter):
        super().__init__(name='NAT', daemon=True)
        self.router = router
        self.last_packet_sent: tuple[int, int] | None = None

    def run(self) -> None:
        log.log(log.INFO, f'{self.name}: is starting')
        nat_queue = self.router.get_queue(255)
        router_queue = self.router.get_router_queue(255)
        last_packet_received: tuple[int, int] | None = None
        while True:
            x = nat_queue.get()
            if x != -1:
                y = nat_queue.get()
                last_packet_received = (x,y)
                log.log(log.INFO, f'NAT received packet {last_packet_received}')
            else:
                log.log(log.DEBUG, f'NAT checking for idle')
                if last_packet_received and self.router.is_idle():
                    log.log(log.INFO, f'NAT sending to 0: {last_packet_received}')
                    router_queue.put(0)
                    router_queue.put(last_packet_received[0])
                    router_queue.put(last_packet_received[1])
                    if self.last_packet_sent and self.last_packet_sent[1] == last_packet_received[1]:
                        break
                    self.last_packet_sent = last_packet_received
            
        log.log(log.INFO, f'{self.name}: is done')
