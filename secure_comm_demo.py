import textwrap as tw

def print_intro():
    title = ('\nSecure Communication on Unsecured Lines Between Strangers\n'
           + '-----------------------------------------------------------------\n')
    intro_pt1 = ('Story Time! Alice and Bob are great friends! So much so that '
                 'Alice wants to send Bob a present! But Alice knows that the '
                 'post office that handles her mail is totally corrupt. They '
                 'will open her package if it\'s not locked and steal Bob\'s '
                 'present! But if Alice locks the box she sends Bob, Bob won\'t '
                 'be able to open it either! How to solve this mystery...')
    intro_pt2 = ('Alice is a smart lady. She came up with this solution. Alice '
                 'locked Bob\'s gift inside a box and mailed it to Bob. Then, '
                 'Bob put his own, Second lock on the box and mailed it back '
                 'to Alice. Now the box is locked with two locks. Alice takes '
                 'her lock off the box, but leaves Bob\'s lock alone, and '
                 'mails it back to Bob, who takes his lock off! Now (aside '
                 'from a fortune spent on shipping), we have a success! Bob '
                 'got his gift from Alice without ever having it stolen by the '
                 'post office!\n\nNow, although this is an interesting story, '
                 'it is also a good way to understand one way that strangers '
                 'can communicate securely over insecure communication '
                 'channels in the digital world. Let\'s say instead, Alice and '
                 'Bob are two computers who have never talked before. Now they want '
                 'to talk, but they want to talk secretly. The problem is that if '
                 'Alice encrypts her message, Bob won\'t know the key to decrypt '
                 'it. But if Alice sends Bob the key in advance, an enemy '
                 'could steal the key and use it to spy on later messages. So how '
                 'does Alice send a secure message without Bob knowing the key? '
                 'The answer is the story above. But in this case, the locks '
                 'are different ciphers and the gift is a secret message.\n\n'
                 'Let\'s see a demonstration!\n')

    print(title)
    intro_pt1_lines = tw.wrap(intro_pt1, width=80)
    for l in intro_pt1_lines:
        print(l)
    input('\nTry to solve Alice\'s problem!\n\n'
        + 'When you\'re done, press Enter to continue...\n')
    print('\u008d\u008d\u008d')
    intro_pt2_lines = tw.wrap(intro_pt2, width=80)
    for l in intro_pt2_lines:
        print(l)

def print_err(err_msg):
    lines = err_msg.splitlines()
    print('ERROR: {}'.format(lines[0]))
    if len(lines) > 1:
        for i in range(1, len(lines)):
            print('       {}'.format(lines[i]))
    print()

def msg_to_bin(msg):
    # NOTE: because of custom use, there is no input validation and the
    # argument, msg, is assumed to be a 5 character string with values
    # in [A-Za-z].

    bins = [0 for i in range(5)]
    for i in range(len(msg)):
        bins[i] = int('{0:b}'.format(ord(msg[i])))
    return bins

def crypt(bins, key):
    output = [0 for i in range(len(bins))]
    k = list('{:08}'.format(key))
    for i in range(len(bins)):
        a = list('{:08}'.format(bins[i]))
        temp = ['x' for i in range(8)]
        cnt = 0
        for z in zip(a, k):
            temp[cnt] = str(int(z[0] != z[1]))
            cnt += 1
        output[i] = int(''.join(temp))
    return output


############################################################################# 
#     Main Program
############################################################################# 


# Print intro and prompt for 5 letter string, 'msg'

print_intro()
while True:
    msg = input('\nPlease enter a 5 letter message: ')
    if len(msg) != 5:
        print_err('Your message was not 5 characters!\nPlease try again')
        continue
    if not msg.isalpha():
        print_err('Your message must contain only '
                + 'English letters!\nPlease try again.')
        continue
    break
print()

# Show Alice encrypting msg and sending to Bob

print('='*90)
print()
print('Great! Alice will send "{}" to Bob!\n'.format(msg))
print('Encrypting and decrypting has 2 steps:')
print('     1) Convert the letters into binary numbers using Unicode[1].')
print('     2) Encrypt/Decrypt the numbers with a key and XOR[2].\n')
print('[1]: Unicode is just a universally agreed upon dictionary that')
print('     allows everyone to convert symbols into numbers.')
print('[2]: XOR is an operation for 1\'s and 0\'s.')
print('     If you have 2 digits (either 1 or 0), x and y,')
print('     x XOR y = 0 if they are the same (both 1 or 0) or')
print('     x XOR y = 1 if they are not the same (1 and 0 or 0 and 1\n')
print('So first Alice converts "{}" to binary!\n'.format(msg))
print('     {:>8} {:>8} {:>8} {:>8} {:>8}'.format(msg[0], msg[1], msg[2],
                                             msg[3], msg[4]))
bins = msg_to_bin(msg)
print('     {:08} {:08} {:08} {:08} {:08}\n'.format(bins[0], bins[1], bins[2],
                                                  bins[3], bins[4]))

print('Then, Alice uses XOR to encrypt the binary numbers with a key.\n')
a_key = 1110100
print('     Alice\'s Key: {:08}\n'.format(a_key))
print('     {:08} {:08} {:08} {:08} {:08}'.format(bins[0], bins[1], bins[2],
                                                  bins[3], bins[4]))
print(' XOR {:08} {:08} {:08} {:08} {:08}'.format(a_key, a_key, a_key,
                                                  a_key, a_key))
print('-'*49)
a_encrypt = crypt(bins, a_key)
print('     {:08} {:08} {:08} {:08} {:08}\n'.format(a_encrypt[0], a_encrypt[1],
                                                    a_encrypt[2], a_encrypt[3],
                                                    a_encrypt[4]))
print('Alice sends Bob that binary string. Totally scrambled!\n')
input('Press Enter to continue...')

# Show Bob encrypting A-encrypted msg and sending
# AB-encrypted msg back to Alice

print('\u008d\u008d')
print('='*90)
print()
print('So Bob gets that message and thinks "Well, I have not a clue what this is.')
print('But I\'m going to put my own encryption on and send it back!"')
print('So Bob does another XOR encryption with his own key!\n')
b_key = 10101110
print('     Bob\'s Key: {:08}\n'.format(b_key))
print('     {:08} {:08} {:08} {:08} {:08}'.format(a_encrypt[0], a_encrypt[1],
                                                  a_encrypt[2], a_encrypt[3],
                                                  a_encrypt[4]))
print(' XOR {:08} {:08} {:08} {:08} {:08}'.format(b_key, b_key, b_key,
                                                  b_key, b_key))
print('-'*49)
ab_encrypt = crypt(a_encrypt, b_key)
print('     {:08} {:08} {:08} {:08} {:08}\n'.format(ab_encrypt[0], ab_encrypt[1],
                                                    ab_encrypt[2], ab_encrypt[3],
                                                    ab_encrypt[4]))
print('Bob sends that binary string back to Alice. Still totally scrambled!\n')
input('Press Enter to continue...')
print('\u008d\u008d')
print('='*90)
print()

# Show Alice decrypting AB-encrypted msg and sending
# B-encrypted msg back to Bob

print('Now, the rest is trivial. First, Alice decrypts the double-encrypted')
print('message that Bob sent her[3].\n')
print('[3]: XOR is a symmetric cipher, meaning that decryption uses the')
print('     same key that encryption does, so here it is the same, exact process.\n')
print('     Alice\'s Key: {:08}\n'.format(a_key))
print('     {:08} {:08} {:08} {:08} {:08}'.format(ab_encrypt[0], ab_encrypt[1],
                                                  ab_encrypt[2], ab_encrypt[3],
                                                  ab_encrypt[4]))
print(' XOR {:08} {:08} {:08} {:08} {:08}'.format(a_key, a_key, a_key,
                                                  a_key, a_key))
print('-'*49)
b_encrypt = crypt(ab_encrypt, a_key)
print('     {:08} {:08} {:08} {:08} {:08}\n'.format(b_encrypt[0], b_encrypt[1],
                                                    b_encrypt[2], b_encrypt[3],
                                                    b_encrypt[4]))
input('Press Enter to continue...')
print('\u008d\u008d')
print('='*90)
print()

# Show Bob decrypting B-encrypted msg and getting original msg!

print('Now, Alice\'s encryption is broken, but Bob\'s encryption')
print('is still active. Alice sends the resulting message')
print('back to Bob, who decrypts his own encryption.\n')
print('     Bob\'s Key: {:08}\n'.format(b_key))
print('     {:08} {:08} {:08} {:08} {:08}'.format(b_encrypt[0], b_encrypt[1],
                                                  b_encrypt[2], b_encrypt[3],
                                                  b_encrypt[4]))
print(' XOR {:08} {:08} {:08} {:08} {:08}'.format(b_key, b_key, b_key,
                                                  b_key, b_key))
print('-'*49)
msg_decrypted = crypt(b_encrypt, b_key)
print('     {:08} {:08} {:08} {:08} {:08}\n'.format(msg_decrypted[0], msg_decrypted[1],
                                                    msg_decrypted[2], msg_decrypted[3],
                                                    msg_decrypted[4]))
print('When we use Unicode to convert the last binary result back to text,')
print('we get...\n')
ltrs_decrypted = [chr(int(str(a), 2)) for a in msg_decrypted]
print('     {:>8} {:>8} {:>8} {:>8} {:>8}'.format(ltrs_decrypted[0], ltrs_decrypted[1],
                                                  ltrs_decrypted[2], ltrs_decrypted[3],
                                                  ltrs_decrypted[4]))
print('     {:08} {:08} {:08} {:08} {:08}\n'.format(msg_decrypted[0], msg_decrypted[1],
                                                    msg_decrypted[2], msg_decrypted[3],
                                                    msg_decrypted[4]))
input('Press Enter to continue...')
print('\u008d\u008d')
print('='*90)
print()

# Closing message

print('Now Bob has Alice\'s message! He can read it clearly and no one')
print('could have stolen the message during travel. More importantly,')
print('Alice and Bob never met, knew each other, or exchanged secrets over')
print('an unsecured line of communication. Despite being total strangers,')
print('Alice and Bob can communicate securely without knowing each other\'s')
print('keys at all! Amazing! Obviously digital encryption in the real world')
print('is enormously more sophisticated than a simple XOR cipher, but this')
print('is still an interesting and easy to grasp beginning to the security')
print('mentality. Thanks for reading!\n')
