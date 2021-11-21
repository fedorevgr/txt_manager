import encoder
import decoder
import sys

if len(sys.argv) == 3:
    file_name = sys.argv[2]
    mode = sys.argv[1]
    if mode == '-e':
        encoder.init(file_name)
        print('Encoded ' + str(file_name))
    else:
        text = decoder.init(file_name)
        new_file = 'decoded_' + file_name + '.txt'
        file = open(new_file, 'x', encoding='UTF8')
        file.write(text)
        file.close()
        print('Decoded ' + str(file_name) + '.dec')