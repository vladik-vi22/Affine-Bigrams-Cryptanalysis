import sys


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def inverse_modulo(a, n):
    a = a % n
    if n == 0:
        return 1
    x1, x2 = 1, 0
    while a > 0:
        q = int(n / a)
        r, x = n - (q * a), x2 - (q * x1)
        n, a = a, r
        x2, x1 = x1, x
    return x2


def linear_comparisons(a, b, n):
    X = []
    d = gcd(a, n)
    a1, b1, n1 = a / d, b / d, n / d
    x0 = (b1 * inverse_modulo(a1, n1)) % n1
    if d == 1:
        X.append((inverse_modulo(a, n) * b) % n)
        return X
    else:
        if (b % d) != 0:
            return None
        else:
            for i in range(0, d):
                X.append(x0 + (i * n1))
            return X


def most_frequent_bigrams(text):
    bif = {}
    most_freq = []
    for ch1 in alphabet:
        for ch2 in alphabet:
            bif[ch1 + ch2] = sys.float_info.min
    for i in range(0, len(text) - 1, 2):
        bif[text[i] + text[i + 1]] += 1
    bif = sorted(bif.items(), key=lambda bf: bf[1], reverse=True)
    for i in range(0, 5):
        most_freq.append(bif[i][0])
    return most_freq


def encrypt_by_afin(text, key):
    m = len(alphabet)
    a, b = key[0], key[1]
    encrypt = ""
    binumx, binumy = [], []
    for i in range(0, len(text) - 1, 2):
        binumx.append((alphabet.index(text[i]) * m) + alphabet.index(text[i + 1]))
    for i in range(0, len(binumx)):
        binumy.append(((a * binumx[i]) + b) % (m ** 2))
        encrypt += alphabet[binumy[i] // m] + alphabet[binumy[i] - ((binumy[i] // m) * m)]
    return encrypt


def decrypt_by_afin(text, key):
    m = len(alphabet)
    a, b = key[0], key[1]
    if inverse_modulo(a, m ** 2) is None:
        # print('Cant Decrypt')
        return None
    else:
        decrypt = ""
        binumy, binumx = [], []
        for i in range(0, len(text) - 1, 2):
            binumy.append((alphabet.index(text[i]) * m) + alphabet.index(text[i + 1]))
        for i in range(0, len(binumy)):
            binumx.append((inverse_modulo(a, m ** 2) * (binumy[i] - b)) % (m ** 2))
            decrypt += alphabet[binumx[i] // m] + alphabet[binumx[i] - ((binumx[i] // m) * m)]
        return decrypt


def find_keys(text):
    m = len(alphabet)
    most_freq_bigrams2 = most_frequent_bigrams(text);
    keys = []
    binumx, binumy = [], []
    for i in range(0, len(most_freq_bigrams1)):
        binumx.append((alphabet.index(most_freq_bigrams1[i][0]) * m) + alphabet.index(most_freq_bigrams1[i][1]))
        binumy.append((alphabet.index(most_freq_bigrams2[i][0]) * m) + alphabet.index(most_freq_bigrams2[i][1]))
    for i in range(0, len(binumx)):
        for j in range(0, len(binumy)):
            for k in range(0, len(binumx)):
                for l in range(0, len(binumy)):
                    if (i != k) and (j != l):
                        a = linear_comparisons((binumx[i] - binumx[k]), (binumy[j] - binumy[l]), (m ** 2))
                        if (a is not None) and (a != 0):
                            for q in range(0, len(a)):
                                keys.append((int(a[q]), (binumy[i] - (int(a[q]) * binumx[i])) % (m ** 2)))
    keys = list(set(keys))
    # if (654, 777) in keys:
    #     print('chetko')
    return keys


def decrypt_text(text):
    keys = find_keys(text)
    for i in range(0, len(keys)):
        decrypt = decrypt_by_afin(text, keys[i])
        if decrypt is not None:
            accepted = True
            for bi in never_freq_bigrams:
                if decrypt.count(bi) != 0:
                    accepted = False
            if accepted:
                print(keys[i])
                print(decrypt)


alphabet = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з',
            'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
            'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч',
            'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я')
most_freq_bigrams1 = ('ст', 'но', 'ен', 'то', 'на')
never_freq_bigrams = ('оь', 'оы', 'ыы', 'ьь')
key1 = (654, 777)

with open("var05") as file:
    data = file.read().replace('ё', 'е').replace('ъ', 'ь').lower()
    for c in data:
        if c not in alphabet:
            data = data.replace(c, '')

# print(encrypt_by_afin(data, key1))
# print(decrypt_by_afin(data, key1))
# print(decrypt_by_afin(data, key1).count('оь'))
# print(decrypt_by_afin(encrypt_by_afin(data, key1), key1))
# print(find_keys(data))
decrypt_text(data)
# print(mSost_frequent_bigrams(data))
# print(never_frequent_bigrams(data))
# print(gcd(0, 961))
# print(inverse_modulo(0, 961))
# print(linear_comparisons(-100, 31, 961))
