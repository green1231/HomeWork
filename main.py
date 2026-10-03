"""Консольная программа для анализа отзывов покупателей."""


reviews = [
    ("Отличный товар быстрая доставка", 5),
    ("Товар хороший но доставка медленная", 4),
    ("Ужасный товар не советую никому", 1),
    ("Доставка быстрая товар нормальный", 4),
    ("Отличный магазин отличный сервис", 5),
    ("Плохой товар сломался сразу", 2),
]


def normalize(text):
    """Привести текст к единому виду для дальнейшего анализа."""
    if not isinstance(text, str):
        return ""
    return text.lower().strip().replace(",", " ").replace(".", " ")


def word_frequency(reviews):
    """Вернуть словарь частот слов во всех отзывах."""
    counter = {}
    for text, rating in reviews:
        for word in normalize(text).split():
            counter[word] = counter.get(word, 0) + 1
    return counter


def unique_words(reviews):
    """Вернуть множество уникальных слов из всех отзывов."""
    words = set()
    for text, rating in reviews:
        for word in normalize(text).split():
            words.add(word)
    return words


def top_words(reviews, n):
    """Вернуть не более n самых частых слов и число их употреблений."""
    if n <= 0:
        return []

    frequencies = word_frequency(reviews)
    sorted_words = sorted(
        frequencies.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    return sorted_words[:n]


def rating_stats(reviews):
    """Рассчитать среднюю, крайние оценки и число отзывов по настроению."""
    ratings = [rating for text, rating in reviews]
    stats = {
        "average": 0,
        "max": 0,
        "min": 0,
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }

    if not ratings:
        return stats

    stats["average"] = sum(ratings) / len(ratings)
    stats["max"] = max(ratings)
    stats["min"] = min(ratings)

    for rating in ratings:
        if rating >= 4:
            stats["positive"] += 1
        elif rating <= 2:
            stats["negative"] += 1
        else:
            stats["neutral"] += 1

    return stats


def make_report(reviews):
    """Собрать и вернуть многострочный отчёт по отзывам."""
    words = unique_words(reviews)
    stats = rating_stats(reviews)
    lines = [
        "ОТЧЕТ ПО ОТЗЫВАМ",
        f"Всего отзывов: {len(reviews)}",
        f"Уникальных слов: {len(words)}",
        f"Средняя оценка: {stats['average']:.2f}",
        "",
        f"Положительных: {stats['positive']}",
        f"Нейтральных: {stats['neutral']}",
        f"Отрицательных: {stats['negative']}",
        "",
        "Топ-3 слова:",
    ]

    for word, count in top_words(reviews, 3):
        lines.append(f"  {word} — {count}")

    return "\n".join(lines)


def run():
    """Показывать меню и выполнять команды до выбора выхода."""
    while True:
        print("\n1 — Полный отчет")
        print("2 — Топ слов")
        print("3 — Статистика оценок")
        print("0 — Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print(make_report(reviews))
        elif choice == "2":
            for word, count in top_words(reviews, 3):
                print(f"  {word} — {count}")
        elif choice == "3":
            stats = rating_stats(reviews)
            print(f"Средняя оценка: {stats['average']:.2f}")
            print(f"Максимальная оценка: {stats['max']}")
            print(f"Минимальная оценка: {stats['min']}")
            print(f"Положительных: {stats['positive']}")
            print(f"Нейтральных: {stats['neutral']}")
            print(f"Отрицательных: {stats['negative']}")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Введите 1, 2, 3 или 0.")


if __name__ == "__main__":
    run()
