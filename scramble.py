import random as r

def scramble_internal(sentence):
    words = sentence.lower().split(' ')
    new_words = []
    for w in words:
        if len(w) in (1, 2):
            new_words.append(w)
            continue
        w = list(w)
        i = 0
        while not w[i].isalnum():
            i += 1
        if i == 0:
            prefix = w[i]
            w = w[1:]
        else:
            prefix = w[:i + 1]
            w = w[i + 1:]
        i = len(w) - 1
        while not w[i].isalnum():
            i -= 1
        if i == (len(w) - 1):
            suffix = w[len(w) - 1]
            w = w[:-1]
        else:
            suffix = w[i:]
            w = w[:i]
        prefix = ''.join(prefix)
        suffix = ''.join(suffix)
        r.shuffle(w)
        w = ''.join(w)
        new_words.append(prefix + w + suffix)
    new_sentence = ' '.join(new_words)
    return(new_sentence)


def main():
    print()
    print('Internal Scrambler')
    print('------------------')
    print()
    sentence = input('Type a sentence to be scrambled.\n> ')
    sentence = scramble_internal(sentence)
    print()
    print(f'Here is your scrambled sentence.\n> {sentence}')
    print()


if __name__ == '__main__':
    main()
