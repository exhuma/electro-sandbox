from subprocess import check_output
import logging

import pigpio

from constants import LEDS


LOG = logging.getLogger(__name__)


def init(connection):
    '''
    Initialise each LED and turn it off.
    '''
    for led in LEDS:
        connection.set_mode(led, pigpio.OUTPUT)
        connection.write(led, 1)


def reset(connection):
    '''
    Turn each LED off.
    '''
    for led in LEDS:
        connection.write(led, 1)


def visualise(conn, value):
    reset(conn)
    if not (0 <= value <= 255):
        raise ValueError('Value must be between 0 and 255!')

    bitmap = bin(value)[2:]

    # zero-fill to 8 digits
    bitmap = '0' * (8-len(bitmap)) + bitmap
    for i, char in enumerate(bitmap):
        LOG.debug('Setting position #%d to %d', i, int(char))
        conn.write(LEDS[i], 0 if int(char) else 1)


def get_ip():
    output = check_output(['ip', 'addr'])
    inets = [line for line in output.splitlines()
             if 'inet' in line and '127.0.0.1' not in line]
    for line in inets:
        ip = line.split()[1]
        if ':' in ip:
            LOG.debug('Ignoring IPv6 Addresses')
            continue
        break
    else:
        raise RuntimeError('No IP found!')
    address, _, _ = ip.partition('/')  # drop the subnet mask if any
    return address


def run():
    LOG.info('LED controller started')
    pi = pigpio.pi()
    init(pi)
    ip = get_ip()
    octets = [int(octet) for octet in ip.split('.')]
    for octet in octets:
        LOG.info('Visualising %d', octet)
        visualise(pi, octet)
    reset(pi)
    pi.stop()


logging.basicConfig(level=logging.DEBUG)
run()
