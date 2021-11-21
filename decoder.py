def get_str(name):
    file = open(name, 'rb')
    to_encode = bytes()
    line = True
    while line:
        line = file.readline()
        to_encode += line
    file.close()
    return to_encode


def get_encoding(byte_expression):
    byte_expression = byte_expression[5:]
    end = byte_expression.index(b'|')
    if byte_expression[end:(end + 5)] == b'|&|&|':
        byte_expression = byte_expression[:end]
    byte_expression = byte_expression[1:-1]
    encodes = byte_expression.split(b'}{')
    keys = list()
    values = list()
    for elem in encodes:
        keys.append(chr(int.from_bytes(elem[0:2], 'big')))
        values.append(elem[2:].decode())
    decoding = dict()
    for elem_id in range(len(keys)):
        decoding[values[elem_id]] = keys[elem_id]
    return decoding


def get_bit_link(byte_expression):
    byte_expression = byte_expression[5:]
    end = byte_expression.index(b'|')
    if byte_expression[end:(end + 5)] == b'|&|&|':
        byte_expression = byte_expression[end + 5:]
    bytes_list = list(byte_expression)
    for num_id in range(len(bytes_list)):
        bits = bin(bytes_list[num_id])[2:]
        if len(bits) != 8:
            correction = '0' * (8 - len(bits)) + bits
            bits = correction
        bytes_list[num_id] = bits
    bit_link = str()
    for bits in bytes_list:
        bit_link += bits
    return bit_link


def get_text(bit_link, decodes):
    text = ''
    bits = ''
    for bit in bit_link:
        bits += bit
        if bits in decodes:
            symbol = decodes[bits]
            text += symbol
            bits = ''
            if symbol == '$':
                break
    return text[:-1]


def init(file):
    expression = get_str(file)
    return get_text(get_bit_link(expression), get_encoding(expression))
