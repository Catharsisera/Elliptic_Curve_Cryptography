# Программная реализация алгоритма шифрования и дешифрования на эллиптических кривых

  В программе используется библиотека random для генерация случайных целых и вещественных чисел, в том числе и из некоторых вероятностных распределений, создание объектов-генераторов и работа с их внутренним состоянием.
  Программа состоит из одного исполняемого модуля ECC.py – модуль, реализующий консольный интерфейс, с реализацией функций, выполняющих процессы шифрования и расшифрования данных на эллиптических кривых.
  Модуль ECC содержит в себе следующие методы:
===
-	is_prime – проверяет число на простоту;
-	inv_element – находит обратный элемент;
-	nod – находит наибольший общий делитель;
-	summ_dots – выполнение суммирования двух точек;
-	mult_dot – выполняет умножения точки на число;
-	count_dots_EC – находит количество точек на эллиптической кривой; 
-	encrypt_and_decrypt – выполняет шифрование и дешифрование данных.
