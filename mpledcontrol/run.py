#!/usr/bin/env python

from __future__ import print_function
from multiprocessing import Process, Queue
import logging

from lib.procs import (
    button_monitor,
    dispatcher,
    led_controller,
)


def main():
    logging.basicConfig(level=logging.DEBUG)
    event_queue = Queue()
    led_control_queue = Queue()

    monitor = Process(target=button_monitor.run, args=(event_queue,))
    monitor.daemon = True
    monitor.start()

    lcon = Process(target=led_controller.run, args=(
        event_queue, led_control_queue))
    lcon.daemon = True
    lcon.start()

    eloop = Process(target=dispatcher.run, args=({
        'events': event_queue,
        'led_control': led_control_queue,
    },))
    eloop.daemon = True
    eloop.start()

    try:
        monitor.join()
        eloop.join()
        lcon.join()
    except KeyboardInterrupt:
        pass

    logging.info('Successfully quit')


if __name__ == '__main__':
    main()
