#!/usr/bin/python

test_string = "Hello, what? How;never! egads you are here"

separators = [',', ' ', '.', '?', '!', ';', '\n']
start = "<START_OF_SENT>"

def divideBySeps(inp_string = test_string, sep_list = separators, include_seps = False):
    piece_list = []
    cur_piece = ""
    for character in inp_string:
        if character in sep_list:
            if len(cur_piece) > 0:
                piece_list.append(cur_piece)
            if include_seps:
                piece_list.append(character)
            cur_piece = ""
        else:
            cur_piece += character
    piece_list.append(cur_piece)
    return piece_list

def combineSeps(inp_list, sep_list = separators):
    pos = 0
    final_list = []
    cur_seps = ""
    while pos < len(inp_list):
        if inp_list[pos] in sep_list:
            while pos < len(inp_list) and inp_list[pos] in sep_list:
                cur_seps += inp_list[pos]
                pos += 1
            final_list.append(cur_seps)
            cur_seps = ""
        else:
            final_list.append(inp_list[pos])
            pos += 1
    return final_list

if __name__=="__main__":
    print divideBySeps()
    print combineSeps(divideBySeps())
    print "".join(combineSeps(divideBySeps())[0:(2*3 -1)])
