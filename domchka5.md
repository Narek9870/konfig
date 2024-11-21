##Задача 1 
Байткод:
```
11    0 LOAD_FAST          0 (x)
      2 LOAD_CONST         1 (10)
      4 BINARY_MULTIPLY
      6 LOAD_CONST         2 (42)
      8 BINARY_ADD
     10 RETURN_VALUE
```
Что делает каждая строка байткода?
LOAD_FAST 0 (x)

Команда загружает локальную переменную x на стек.
Эквивалент на Python: получить значение переменной x.
LOAD_CONST 1 (10)

Загружает на стек константу 10.
Эквивалент на Python: число 10.
BINARY_MULTIPLY

Выполняет умножение двух верхних элементов на стеке.
После выполнения: результат (x * 10) помещается обратно на стек.
Эквивалент на Python: x * 10.
LOAD_CONST 2 (42)

Загружает на стек константу 42.
Эквивалент на Python: число 42.
BINARY_ADD

Выполняет сложение двух верхних элементов на стеке.
После выполнения: результат ((x * 10) + 42) помещается обратно на стек.
Эквивалент на Python: (x * 10) + 42.
RETURN_VALUE

Возвращает верхний элемент стека как результат функции.
Эквивалент на Python: return (x * 10) + 42.
Эквивалентный Python-код:
На языке Python этот набор байткода соответствует следующей функции:
```
def foo(x):
    return (x * 10) + 42
```
#Задача 2
Байткод
Шаг 1: Инициализация переменной r
```
5    0 LOAD_CONST          1 (1)
     2 STORE_FAST          1 (r)
```
LOAD_CONST 1 (1): Загружается константа 1 (целое число) на стек.
STORE_FAST 1 (r): Сохраняет значение 1 в локальную переменную r.
Результат на данном этапе: r = 1.

Шаг 2: Начало цикла while n > 1
```
6    4 LOAD_FAST           0 (n)
     6 LOAD_CONST          1 (1)
     8 COMPARE_OP          4 (>)
    10 POP_JUMP_IF_FALSE   30
```
LOAD_FAST 0 (n): Загружает значение переменной n на стек.
LOAD_CONST 1 (1): Загружает значение 1 на стек.
COMPARE_OP 4 (>): Сравнивает n > 1.
POP_JUMP_IF_FALSE 30: Если результат сравнения False (т.е. n <= 1), выполнение переходит к строке 30 (выход из цикла).
Результат на данном этапе: Проверяется условие цикла while n > 1.

Шаг 3: Умножение r на n
```
7    12 LOAD_FAST          1 (r)
     14 LOAD_FAST          0 (n)
     16 INPLACE_MULTIPLY
     18 STORE_FAST         1 (r)
```
LOAD_FAST 1 (r): Загружает текущее значение переменной r на стек.
LOAD_FAST 0 (n): Загружает текущее значение переменной n на стек.
INPLACE_MULTIPLY: Умножает верхние два значения стека (т.е. r * n) и сохраняет результат на стеке.
STORE_FAST 1 (r): Сохраняет результат умножения обратно в переменную r.
Результат на данном этапе: r *= n.

Шаг 4: Уменьшение n
```
8    20 LOAD_FAST          0 (n)
     22 LOAD_CONST         1 (1)
     24 INPLACE_SUBTRACT
     26 STORE_FAST         0 (n)
     28 JUMP_ABSOLUTE
```
LOAD_FAST 0 (n): Загружает текущее значение переменной n на стек.
LOAD_CONST 1 (1): Загружает значение 1 на стек.
INPLACE_SUBTRACT: Вычитает 1 из n (т.е. n = n - 1) и сохраняет результат на стеке.
STORE_FAST 0 (n): Сохраняет результат в переменную n.
JUMP_ABSOLUTE 4: Возвращается к строке 4, чтобы повторить цикл.
Результат на данном этапе: n -= 1.

Шаг 5: Возврат результата
```
9    30 LOAD_FAST          1 (r)
     32 RETURN_VALUE
```
LOAD_FAST 1 (r): Загружает значение переменной r на стек.
RETURN_VALUE: Возвращает значение r как результат функции.
Результат: возвращается значение переменной r.

Название функции  факториал числа.


##Задача 3
Приведите результаты из задач 1 и 2 для виртуальной машины JVM (Java) или .Net (C#).
Java
```
public class Main {
    public static int foo(int x) {
        return (x * 10) + 42;
    }

    public static void main(String[] args) {
        int result = foo(5);
        System.out.println(result);
    }
}
```
Байткод
```
// class version 66.0 (66)
// access flags 0x21
public class Main {

  // compiled from: Main.java

  // access flags 0x1
  public <init>()V
   L0
    LINENUMBER 1 L0
    ALOAD 0
    INVOKESPECIAL java/lang/Object.<init> ()V
    RETURN
   L1
    LOCALVARIABLE this LMain; L0 L1 0
    MAXSTACK = 1
    MAXLOCALS = 1

  // access flags 0x9
  public static foo(I)I
   L0
    LINENUMBER 3 L0
    ILOAD 0
    BIPUSH 10
    IMUL
    BIPUSH 42
    IADD
    IRETURN
   L1
    LOCALVARIABLE x I L0 L1 0
    MAXSTACK = 2
    MAXLOCALS = 1

  // access flags 0x9
  public static main([Ljava/lang/String;)V
   L0
    LINENUMBER 7 L0
    ICONST_5
    INVOKESTATIC Main.foo (I)I
    ISTORE 1
   L1
    LINENUMBER 8 L1
    GETSTATIC java/lang/System.out : Ljava/io/PrintStream;
    ILOAD 1
    INVOKEVIRTUAL java/io/PrintStream.println (I)V
   L2
    LINENUMBER 9 L2
    RETURN
   L3
    LOCALVARIABLE args [Ljava/lang/String; L0 L3 0
    LOCALVARIABLE result I L1 L3 1
    MAXSTACK = 2
    MAXLOCALS = 2
}
```
![image](https://github.com/user-attachments/assets/9b2d350b-1af4-4bf4-b2d1-43927494d5c7)

