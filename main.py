import random
import time
from collections import Counter
import matplotlib.pyplot as plt

def compute_lps(pattern):
    length = len(pattern)
    # inicjalizacja tablicy
    lps = [0] * length

    # długość poprzedniego najdłuższego prefiksu-sufiksu
    len_prev = 0

    # LPS[0] zawsze wynosi 0
    i = 1

    while i < length:
        if pattern[i] == pattern[len_prev]:
            # Jeśli znaki się zgadzają, zwiększamy długość LPS
            len_prev += 1
            lps[i] = len_prev
            i += 1
        else:
            if len_prev != 0:
                # Cofamy się do poprzedniego potencjalnego dopasowania
                len_prev = lps[len_prev - 1]
            else:
                # Nie znaleziono dopasowania, przechodzimy dalej
                lps[i] = 0
                i += 1

    print(f"Utworzona tablica LPS: {lps}")
    return lps


def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


def kmp_search(text, pattern):
    if not pattern or not text:
        return []

    matches = []

    n = len(text)
    m = len(pattern)

    print(f"\nWzorzec '{pattern}' w tekście '{text}'")

    # tablica LPS
    lps = compute_lps(pattern)

    # indeksy dla tekstu i wzorca
    i = 0
    j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == m:
                # Znaleziono pełne dopasowanie
                match_index = i - j
                matches.append(match_index)
                # Przesuwamy się do następnego potencjalnego dopasowania
                j = lps[j - 1]
        else:
            if j != 0:
                # Niedopasowanie, przesunięcie wzorca używając LPS
                j = lps[j - 1]
            else:
                # Brak dopasowania na początku wzorca
                i += 1

    if not matches:
        print("Nie znaleziono żadnych dopasowań.")

    return matches


def plot_matches(text, pattern, matches):

    x_values = range(len(text))
    y_values = [1] * len(text)

    plt.figure(figsize=(14, 3))

    plt.plot(x_values, y_values, color='red', label='Tekst')

    for match in matches:

        match_range = range(match, match + len(pattern))
        match_y_values = [1] * len(pattern)
        plt.plot(match_range, match_y_values, color='green', linewidth=5, alpha=0.8, label='Dopasowanie wzorca')

    plt.title(f"Dopasowania wzorca '{pattern}' w tekście")
    plt.xlabel("Indeks w tekście")
    plt.ylabel("Poziom")

    plt.ylim(0, 2)
    plt.yticks([1])

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = list(dict(zip(labels, handles)).items())
    plt.legend([x[1] for x in unique], [x[0] for x in unique])
    plt.show()


def plot_char_distribution(text, pattern):
    char_count_text = Counter(text)
    char_count_pattern = Counter(pattern)

    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    ax[0].bar(char_count_text.keys(), char_count_text.values(), color='b', alpha=0.7)
    ax[0].set_title("Rozkład liczności znaków w tekście")
    ax[0].set_xlabel("Znaki")
    ax[0].set_ylabel("Liczność")

    ax[1].bar(char_count_pattern.keys(), char_count_pattern.values(), color='r', alpha=0.7)
    ax[1].set_title("Rozkład liczności znaków we wzorcu")
    ax[1].set_xlabel("Znaki")
    ax[1].set_ylabel("Liczność")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    text_chars = input("Podaj znaki używane do generowania tekstu (np. A,B,C,D): ")
    pattern = input("Podaj wzorzec do wyszukania: ")
    factorial_param = int(input("Podaj wartość do obliczenia silni: "))

    text = ''.join(random.choice(text_chars.split(',')) for _ in range(5000))

    start_kmp = time.perf_counter()
    matches = kmp_search(text, pattern)
    end_kmp = time.perf_counter()
    kmp_duration = end_kmp - start_kmp

    start_factorial = time.perf_counter()
    factorial_value = factorial(factorial_param)
    end_factorial = time.perf_counter()
    factorial_duration = end_factorial - start_factorial
    if matches:
        print(f"Wzorzec '{pattern}' został znaleziony na pozycjach: {matches}")
        char_count_text = Counter(text)
        char_count_pattern = Counter(pattern)

        print("\nRozkład liczności zbioru (tekst):")
        for char, count in char_count_text.items():
            print(f"{char}: {count}")

        print("\nRozkład liczności zbioru (wzorzec):")
        for char, count in char_count_pattern.items():
            print(f"{char}: {count}")

        # generowanie wykresów
        plot_matches(text, pattern, matches)
        plot_char_distribution(text, pattern)

        # współczynnik
        ratio = kmp_duration / factorial_duration
        print(
            f"Czas KMP: {kmp_duration:.6f} s, Czas silni({factorial_param}): {factorial_duration:.6f} s, Współczynnik: {ratio:.2f}x")
        input("Naciśnij Enter, aby zakończyć...")

