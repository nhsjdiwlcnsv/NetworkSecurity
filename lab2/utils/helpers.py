import os
import time


def hex2bin(s):
    s = s.upper()
    mp = {'0': "0000",
          '1': "0001",
          '2': "0010",
          '3': "0011",
          '4': "0100",
          '5': "0101",
          '6': "0110",
          '7': "0111",
          '8': "1000",
          '9': "1001",
          'A': "1010",
          'B': "1011",
          'C': "1100",
          'D': "1101",
          'E': "1110",
          'F': "1111"}
    bin = ""

    for i in range(len(s)):
        bin = bin + mp[s[i]]
    return bin


def bin2hex(s):
    mp = {"0000": '0',
          "0001": '1',
          "0010": '2',
          "0011": '3',
          "0100": '4',
          "0101": '5',
          "0110": '6',
          "0111": '7',
          "1000": '8',
          "1001": '9',
          "1010": 'A',
          "1011": 'B',
          "1100": 'C',
          "1101": 'D',
          "1110": 'E',
          "1111": 'F'}
    hex = ""
    for i in range(0, len(s), 4):
        ch = ""
        ch = ch + s[i]
        ch = ch + s[i + 1]
        ch = ch + s[i + 2]
        ch = ch + s[i + 3]
        hex = hex + mp[ch]

    return hex


def decimal2hex(decimal_number):
    hex_string = hex(decimal_number)[2:].zfill(16)
    return hex_string


def hex2decimal(hex_string):
    decimal_number = int(hex_string, 16)
    return decimal_number


def decimal2binary(decimal_number):
    binary_string = bin(decimal_number)[2:].zfill(64)
    return binary_string


def binary2decimal(binary_string):
    decimal_number = int(binary_string, 2)
    return decimal_number


def get_random_key():
    return os.urandom(8).hex().upper()


def get_timestamp():
    return int(time.time())


def print_line():
    print('_' * 60)
