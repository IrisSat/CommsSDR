#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Telemetry parser component example
# Author: Daniel Estevez
# GNU Radio version: 3.9.4.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import satellites.components.datasinks
import satellites.components.deframers
import satellites.components.demodulators




class telemetry_parser(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Telemetry parser component example", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.satellites_u482c_deframer_0 = satellites.components.deframers.u482c_deframer(syncword_threshold = 4, options="")
        self.satellites_telemetry_parser_0 = satellites.components.datasinks.telemetry_parser('gomx_1', file = '/home/jonathan/gr-satellites/examples/components/output_telemetry_parser.txt', options="")
        self.satellites_afsk_demodulator_0_0 = satellites.components.demodulators.afsk_demodulator(baudrate = 4800, samp_rate = samp_rate, iq = False, af_carrier = 3600, deviation = -1200, options="")
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/jonathan/Desktop/testrecording.wav', False)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_u482c_deframer_0, 'out'), (self.satellites_telemetry_parser_0, 'in'))
        self.connect((self.blocks_wavfile_source_0, 0), (self.satellites_afsk_demodulator_0_0, 0))
        self.connect((self.satellites_afsk_demodulator_0_0, 0), (self.satellites_u482c_deframer_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=telemetry_parser, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
