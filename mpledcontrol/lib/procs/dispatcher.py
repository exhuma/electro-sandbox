import logging

from ..events import (
    ButtonStateChange,
    MonitorStateChange,
)


LOG = logging.getLogger(__name__)


def run(queues):
    LOG.info('Event dispatcher started')
    while True:
        try:
            event = queues['events'].get()
            if isinstance(event, MonitorStateChange):
                LOG.debug('Ignoring event: %r', event)
            elif isinstance(event, ButtonStateChange):
                LOG.debug('Sending: %r to LED control', event)
                queues['led_control'].put(event)
            else:
                LOG.debug('Unknown event: %r', event)
        except KeyboardInterrupt:
            break
