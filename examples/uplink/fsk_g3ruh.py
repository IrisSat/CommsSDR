#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.9.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network



from gnuradio import qtgui

class fsk_g3ruh(gr.top_block, Qt.QWidget):

    def __init__(self, num_postamble_bytes=10, num_preamble_bytes=20, sps=20):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fsk_g3ruh")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.num_postamble_bytes = num_postamble_bytes
        self.num_preamble_bytes = num_preamble_bytes
        self.sps = sps

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 192000

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_0 = filter.interp_fir_filter_fff(
            sps,
            firdes.root_raised_cosine(
                sps,
                sps,
                1.0,
                0.35,
                sps*7))
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "FSK modulation of ax25 frame", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_gr_complex, 1, '127.0.0.1', 1234, 0, 1472, False)
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x00, 16)
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb('packet_len')
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf([-1.0, 1.0], 1)
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_float*1, "packet_len", sps)
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, num_postamble_bytes*8, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, num_preamble_bytes*8, "packet_len")
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu('UDP_SERVER', '127.0.0.1', '50248', 10000, False)
        self.blocks_packed_to_unpacked_xx_0_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
        self.blocks_not_xx_0 = blocks.not_bb()
        self.blocks_and_const_xx_0 = blocks.and_const_bb(0x01)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2.0*3.14159*3500.0/float(samp_rate))
        self.analog_const_source_x_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 126)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 126)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.digital_hdlc_framer_pb_0, 'in'))
        self.connect((self.analog_const_source_x_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.analog_const_source_x_0_0, 0), (self.digital_binary_slicer_fb_0_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_and_const_xx_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_not_xx_0, 0), (self.blocks_and_const_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.blocks_tagged_stream_mux_0, 2))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_not_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.blocks_packed_to_unpacked_xx_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_scrambler_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fsk_g3ruh")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_num_postamble_bytes(self):
        return self.num_postamble_bytes

    def set_num_postamble_bytes(self, num_postamble_bytes):
        self.num_postamble_bytes = num_postamble_bytes
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(self.num_postamble_bytes*8)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(self.num_postamble_bytes*8)

    def get_num_preamble_bytes(self):
        return self.num_preamble_bytes

    def set_num_preamble_bytes(self, num_preamble_bytes):
        self.num_preamble_bytes = num_preamble_bytes
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.num_preamble_bytes*8)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.num_preamble_bytes*8)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.blocks_tagged_stream_multiply_length_0.set_scalar(self.sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.sps, self.sps, 1.0, 0.35, self.sps*7))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity(2.0*3.14159*3500.0/float(self.samp_rate))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--num-postamble-bytes", dest="num_postamble_bytes", type=intx, default=10,
        help="Set Number of Postamble Bytes [default=%(default)r]")
    parser.add_argument(
        "--num-preamble-bytes", dest="num_preamble_bytes", type=intx, default=20,
        help="Set Number of Preamble Bytes [default=%(default)r]")
    parser.add_argument(
        "--sps", dest="sps", type=intx, default=20,
        help="Set sps [default=%(default)r]")
    return parser


def main(top_block_cls=fsk_g3ruh, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(num_postamble_bytes=options.num_postamble_bytes, num_preamble_bytes=options.num_preamble_bytes, sps=options.sps)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
