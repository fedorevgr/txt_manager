from collections import Counter
from math import log2, ceil
from random import randint


def reader(name):
    file = open(name, 'r', encoding='UTF8')
    to_encode = ''
    while True:
        line = file.readline()
        if not line:
            break
        to_encode += line
    file.close()
    return to_encode


def probabilities_of_elements(values):
    divider = sum(list(values.values()))
    not_sorted_prob = dict()
    for elem in values:
        not_sorted_prob[elem] = (values[elem]) / divider
    output = dict(sorted(not_sorted_prob.items(), key=lambda item: item[1], reverse=True))
    return output


def shannon_in_business(probs):
    output = dict()
    probs_keys = list(probs.keys())
    probs_values = list(probs.values())
    for elem_id in range(len(probs_keys)):
        if elem_id == 0:
            output[probs_keys[0]] = 0
        else:
            output[probs_keys[elem_id]] = sum(probs_values[0:elem_id])
    return output


def make_bin(number):
    binary_number = '0.'
    for coefficient in range(1, 30):
        check = 1 / (2 ** coefficient)
        if number >= check:
            binary_number += '1'
            number -= check
        else:
            binary_number += '0'
    return binary_number


def shannon_in_binary(values):
    output = dict()
    keys = []
    for elem in values:
        keys.append(elem)
    for elem_id in range(len(keys)):
        output[keys[elem_id]] = make_bin(values[keys[elem_id]])
    return output


def make_log(brand_new_values):
    output = []
    values = list(brand_new_values.values())
    for value in values:
        default = ceil(abs(log2(value)))
        output.append(default)
    return output


def encoding_for_elements(values, mask):
    output = dict()
    keys = []
    for key in values:
        keys.append(key)
    for elem_id in range(len(keys)):
        output[keys[elem_id]] = values[keys[elem_id]][2:(2 + mask[elem_id])]
    return output


def alphabet_to_encrypt(alphabet):
    keys = []
    values = []
    for item in alphabet:
        keys.append(item)
        values.append(str(alphabet[item]))
    return keys, values


def slice_by_bytes(data_in):
    data_out = list()
    for byte in range(0, len(data_in), 8):
        data_out.append(data_in[byte:(byte + 8)])
    return data_out


def encoder(text, encryption):
    code = ''
    for item in text:
        code += encryption[item]
    output = slice_by_bytes(code)
    if len(output[-1]) < 8:
        code += encryption['$']
        output = slice_by_bytes(code)
    if len(output[-1]) < 8:
        last_byte = output[-1] + ('0' * (8 - len(output[-1])))
        output[-1] = last_byte
    for byte_id in range(len(output)):
        output[byte_id] = int(output[byte_id], 2)
    #print(output)
    output = bytes(output)

    return output

def write_code(file, mode):
    file_name = file
    imported = Counter(reader(file_name))
    imported['$'] = 1
    probabilities = probabilities_of_elements(imported)
    frequency_of_elements = shannon_in_business(probabilities)
    encoding = encoding_for_elements(shannon_in_binary(frequency_of_elements), make_log(probabilities))
    encoded_text = encoder(reader(file), encoding)
    z = open(file_name[:-4] + '.dec', mode)
    # ___________________________________________________________________________________________________________________
    # ceasar_shift = randint(1, 256)
    z.write('|&|&|'.encode())
    encrypt_alphabet = alphabet_to_encrypt(encoding)
    for item_id in range(len(encrypt_alphabet[0])):
        z.write('{'.encode() + ord(encrypt_alphabet[0][item_id]).to_bytes(2, 'big') + encrypt_alphabet[1][item_id].encode() + '}'.encode())
    z.write('|&|&|'.encode())
    # ___________________________________________________________________________________________________________________
    z.write(encoded_text)
    z.close()


def init(file):
    try:
        write_code(file, 'xb')
    except FileExistsError:
        write_code(file, 'wb')
