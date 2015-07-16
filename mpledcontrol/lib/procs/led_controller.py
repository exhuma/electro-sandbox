import logging

import pigpio

from ..constants import LED


LOG = logging.getLogger(__name__)


def run(event_queue, led_control_queue):
    LOG.info('LED controller started')
    pi = pigpio.pi()
    pi.set_mode(LED, pigpio.OUTPUT)
    while True:
        try:
            state = led_control_queue.get()
            if state.new_value:
                pi.write(LED, 1)
            else:
                pi.write(LED, 0)
        except KeyboardInterrupt:
            break
    pi.stop()
