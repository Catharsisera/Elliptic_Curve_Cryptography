import random

alphabet = [chr(i) for i in range(ord('А'), ord('А') + 6)] + [chr(ord('Ё'))] + \
           [chr(i) for i in range(ord('А') + 6, ord('А') + 32)] + \
           [chr(i) for i in range(ord('а'), ord('а') + 6)] + [chr(ord('а') + 33)] + \
           [chr(i) for i in range(ord('а') + 6, ord('а') + 32)] + \
           [chr(i) for i in range(ord('A'), ord('A') + 26)] + [chr(i) for i in range(ord('a'), ord('a') + 26)] + \
           [chr(ord('.'))] + [chr(ord(','))] + [chr(ord(' '))] + [chr(ord('?'))]

def is_prime(number):
    if number == 2:
        return True
    if number < 2 or number % 2 == 0:
        return False
    for n in range(3, int(number ** 0.5) + 2, 2):
        if number % n == 0:
            return False
    return True

def inv_element(number, p):
    for i in range(1, p):
        if (i * number) % p == 1:
            return i
    return -1

def nod(x, y):
    if y == 0:
        return x
    else:
        return nod(y, x % y)

def summ_dots(x1, y1, x2, y2, a, p):
    symb = 1  #бит знака (+/-)

    if x1 == x2 and y1 == y2:
        numerator = 3 * (x1 ** 2) + a
        denominator = 2 * y1
    else:
        numerator = y2 - y1
        denominator = x2 - x1
        if numerator * denominator < 0:
            symb = 0
            numerator = abs(numerator)
            denominator = abs(denominator)

    nod_value = nod(numerator, denominator)
    numerator = int(numerator / nod_value)
    denominator = int(denominator / nod_value)
    inv_denominator = inv_element(denominator, p)
    K = (numerator * inv_denominator)
    print("K", K)
    if symb == 0:
        K = -K
    K %= p

    x3 = (K ** 2 - x1 - x2) % p
    y3 = (K * (x1 - x3) - y1) % p
    return [x3, y3]

def mult_dot(G_x, G_y, d, a, p):
    temp_x = G_x
    temp_y = G_y
    while d != 1:
        value_dot = summ_dots(temp_x, temp_y, G_x, G_y, a, p)
        temp_x = value_dot[0]
        temp_y = value_dot[1]
        d -= 1
    return value_dot

def count_dots_EC(a, b, p):
    arrY = []
    for y in range(0, p):
        y1 = pow(y, 2) % p
        arrY.append(y1)

    arrX = []
    for x in range(0, p):
        x1 = (pow(x, 3) + a * x + b) % p
        arrX.append(x1)

    result = []
    for indX, x in enumerate(arrX):
        for indY, y in enumerate(arrY):
            while (x == y):
                result.append([indX, indY])
                break
    return result

def encrypt_and_decrypt():
    while True:
        a = int(input("Введите параметр a эллиптической кривой: "))
        b = int(input("Введите параметр b эллиптической кривой: "))
        p = int(input("Введите параметр p эллиптической кривой (p - простое число): "))
        if not is_prime(p):
            while not is_prime(p):
                print('Число p, должно быть простым!')
                p = int(input("Введите параметр p эллиптической кривой (p - простое число): "))
        if (4 * (a ** 3) + 27 * (b ** 2)) % p == 0:
            print("Выбранная эллиптическая кривая не может быть использована для шифрования, пожалуйста, выберите заново. \n")
            continue
        else:
            break

    count_points = count_dots_EC(a, b, p)
    print('\n Точки ЭК:\n ', count_points)
    arr_x = []
    for i in range(len(count_points)):
        arr_x.append(count_points[i][0])
    arr_x = list(set(arr_x))
    n = len(count_points)
    print('Порядок эллиптической кривой = ', n)
    print("_____________", len(alphabet))
    while len(alphabet) != n:
        alphabet.insert(0, '*')
    alpha = list(zip(alphabet, count_points))
    print('\nАлфавит:')
    for i in range(len(alpha)):
        print(alpha[i][0], '-', alpha[i][1])
    print("\nВыберите генерирующую точку G из точек ЭК, незанятых алфавитом:")
    print("В противном случае, программа может работать некорректно!")
    G_x = int(input("X координата: "))
    G_y = int(input("Y кордината: "))
    count = 0
    while count == 0:
        for i in range(len(count_points)):
            if count_points[i][0] == G_x and count_points[i][1] == G_y:
                count += 1
        if count == 0:
            print('Генерирующая точка выбрана неверно, такой точки на ЭК не существует, попробуйте ещё раз:')
            G_x = int(input("X координата: "))
            G_y = int(input("Y кордината: "))

    d = 0
    while d >= n or d == 0 or d >= abs(p - n):
        d = int(input(f"\nВведите закрытый ключ < {abs(p - n)}: "))
        if d >= abs(p - n) or d == 0:
            print('Закрытый ключ должен быть меньше порядка ЭК и не равен нулю, попробуйте ещё раз:')

    Q = mult_dot(G_x, G_y, d, a, p)
    # print("Создать открытый ключ {a =% d, b =% d, p =% d, n =% d, G = (% d,% d) , Q = (% d,% d)}" % (a, b, p, n, G_x, G_y, Q[0], Q[1]))
    print('Открытый ключ: ', Q)

    OpenText = []
    OpenTextW = list(input("\nВведите открытый текст для шифрования: "))
    for i in range(len(OpenTextW)):
        if OpenTextW[i] not in alphabet:
            print(f'Символа "{OpenTextW[i]}" нет в алфавите, он будет заменен на " "')
            OpenTextW[i] = ' '
    print('Открытый текст:', ''.join(OpenTextW))
    for i in range(len(OpenTextW)):
        for j in range(len(alpha)):
            if OpenTextW[i] == alpha[j][0]:
                OpenText.append(alpha[j][1])
    print('Координаты открытого текста: ', OpenText)

    CipherText = []
    kG_list = []
    for i in range(len(OpenText)):
        k = arr_x[i]
        if k == 0:
            k += 2
        elif k == 1:
            k += 1
        k_G = mult_dot(G_x, G_y, k, a, p)
        k_Q = mult_dot(Q[0], Q[1], k, a, p)
        CipherText.append(summ_dots(OpenText[i][0], OpenText[i][1], k_Q[0], k_Q[1], a, p))
        kG_list.append(k_G)
    print("\nЗашифрованный текст:", list(zip(kG_list, CipherText)))

    def Sub(C_y, C_x, a, p):
        C_x[1] *= -1
        return summ_dots(C_y[0], C_y[1], C_x[0], C_x[1], a, p)
    message = []
    for i in range(len(CipherText)):
        decrypt = mult_dot(kG_list[i][0], kG_list[i][1], d, a, p)
        inv_el = Sub(CipherText[i], decrypt, a, p)
        message.append(inv_el)
    print("\nКоординаты расшифрованного текста: ", message)
    decrypt_text = []
    for i in range(len(message)):
        for j in range(len(alpha)):
            if message[i] == alpha[j][1]:
                decrypt_text.append(alpha[j][0])
    print("Расшифрованный открытый текст: ", ''.join(decrypt_text))

encrypt_and_decrypt()