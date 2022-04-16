"""
Module for ax25 utilities
"""
import textwrap


class AX25Framer:
    """
    ax25 packet framer with information passed during init.

    Adapted from trxvu_driver c++ code

    Visit https://notblackmagic.com/bitsnpieces/ax.25/ for frame information
    """

    def __init__(self, to_call: str, from_call: str, to_ssid: int, from_ssid: int, payload: bytes):
        self._pdu: bytearray = bytearray()
        self._validate_callsigns(to_call, from_call)
        self._validate_ssid(to_ssid, from_ssid)
        self._validate_payload(payload)

        self._to_call = to_call.upper().ljust(6)
        self._from_call = from_call.upper().ljust(6)
        self._to_ssid = to_ssid
        self._from_ssid = from_ssid
        self._payload = payload

        self._assemble_pdu()

    def __str__(self):
        return textwrap.wrap(" ".join(["{:02x}".format(x) for x in self._pdu]), 80)[0]

    def get_pdu(self):
        """
        Returns the bytearray value of this data frame
        """
        return self._pdu

    @staticmethod
    def _validate_payload(payload: bytes):
        if payload is None:
            raise AttributeError("payload must have a value")

        if type(payload) is not bytes:
            raise AttributeError("payload must be bytes")

    @staticmethod
    def _validate_callsigns(to_call: str, from_call: str):
        if (len(to_call) > 6) or (len(from_call) > 6):
            raise AttributeError("callsigns may be no longer than six characters")

        if not (to_call.isalnum()) or not from_call.isalnum():
            raise AttributeError("callsigns may only contain alphanumeric characters")

    @staticmethod
    def _validate_ssid(to_ssid: int, from_ssid: int):
        if not (0 <= to_ssid <= 15) or not (0 <= from_ssid <= 15):
            raise AttributeError("SSIDs must be in the range of 0..15")

    def _assemble_pdu(self):
        self._assemble_address()
        self._assemble_control()
        self._assemble_protocol()
        self._assemble_payload()

    def _assemble_address(self):
        # to_call sign
        for character in self._to_call:
            self._pdu.append(ord(character) << 1)

        # to_ssid
        self._pdu.append((self._to_ssid << 1) | 0xE0)

        # from_call
        for character in self._from_call:
            self._pdu.append(ord(character) << 1)

        self._pdu.append((self._from_ssid << 1) | 0x61)

    def _assemble_control(self):
        # UI frame
        self._pdu.append(0x03)

    def _assemble_protocol(self):
        self._pdu.append(0xF0)

    def _assemble_payload(self):
        self._pdu.extend(self._payload)
