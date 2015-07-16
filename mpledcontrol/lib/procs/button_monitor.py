import time
import logging

import pigpio

from ..constants import BUTTON
from ..events import (
    ButtonStateChange,
    MonitorStateChange,
)


LOG = logging.getLogger(__name__)


def run(event_queue):
    LOG.info('Button monitor started')
    pi = pigpio.pi()
    pi.set_mode(BUTTON, pigpio.INPUT)
    old_state = None
    while True:
        try:
            state = pi.read(BUTTON)
            if state != old_state:
                event_queue.put(ButtonStateChange(state))
                old_state = state
            time.sleep(0.1)  # debounce
        except KeyboardInterrupt:
            break
    event_queue.put(MonitorStateChange(0))
    pi.stop()
