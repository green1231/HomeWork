import io
import unittest
from unittest.mock import patch

import main


class NormalizeTests(unittest.TestCase):
    def test_normalizes_text_as_required(self):
        self.assertEqual(main.normalize("Отличный, товар."), "отличный  товар ")
        self.assertEqual(main.normalize("  БЫСТРАЯ доставка  "), "быстрая доставка")
        self.assertEqual(
            main.normalize("Товар, хороший. Очень!"),
            "товар  хороший  очень!",
        )

    def test_non_string_returns_empty_string(self):
        self.assertEqual(main.normalize(None), "")
        self.assertEqual(main.normalize(42), "")


class WordAnalysisTests(unittest.TestCase):
    def test_counts_word_frequency(self):
        reviews = [("Товар хороший", 5), ("Товар плохой", 1)]
        self.assertEqual(
            main.word_frequency(reviews),
            {"товар": 2, "хороший": 1, "плохой": 1},
        )

    def test_collects_unique_words(self):
        reviews = [("товар хороший товар", 5), ("товар плохой", 1)]
        self.assertEqual(
            main.unique_words(reviews),
            {"товар", "хороший", "плохой"},
        )

    def test_returns_most_frequent_words(self):
        reviews = [
            ("товар товар товар", 5),
            ("доставка доставка", 4),
            ("сервис", 5),
        ]
        self.assertEqual(
            main.top_words(reviews, 2),
            [("товар", 3), ("доставка", 2)],
        )

    def test_top_words_handles_limits(self):
        reviews = [("один два", 5)]
        self.assertEqual(len(main.top_words(reviews, 10)), 2)
        self.assertEqual(main.top_words(reviews, 0), [])
        self.assertEqual(main.top_words(reviews, -1), [])


class RatingStatsTests(unittest.TestCase):
    def test_calculates_rating_statistics(self):
        reviews = [("текст", 5), ("текст", 4), ("текст", 1), ("текст", 3)]
        self.assertEqual(
            main.rating_stats(reviews),
            {
                "average": 3.25,
                "max": 5,
                "min": 1,
                "positive": 2,
                "negative": 1,
                "neutral": 1,
            },
        )

    def test_empty_reviews_return_zero_statistics(self):
        self.assertEqual(
            main.rating_stats([]),
            {
                "average": 0,
                "max": 0,
                "min": 0,
                "positive": 0,
                "negative": 0,
                "neutral": 0,
            },
        )


class ReportTests(unittest.TestCase):
    def test_report_uses_calculated_values(self):
        report = main.make_report(main.reviews)
        expected_lines = [
            "ОТЧЕТ ПО ОТЗЫВАМ",
            "Всего отзывов: 6",
            "Уникальных слов: 17",
            "Средняя оценка: 3.50",
            "Положительных: 4",
            "Нейтральных: 0",
            "Отрицательных: 2",
            "Топ-3 слова:",
            "  товар — 5",
            "  отличный — 3",
            "  доставка — 3",
        ]
        for line in expected_lines:
            with self.subTest(line=line):
                self.assertIn(line, report)

    def test_empty_report_does_not_crash(self):
        report = main.make_report([])
        self.assertIn("Всего отзывов: 0", report)
        self.assertIn("Средняя оценка: 0.00", report)


class MenuTests(unittest.TestCase):
    @patch("builtins.input", side_effect=["incorrect", "2", "3", "1", "0"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_menu_handles_every_action_and_invalid_input(self, stdout, _input):
        main.run()
        output = stdout.getvalue()
        self.assertIn("Неверный выбор", output)
        self.assertIn("товар — 5", output)
        self.assertIn("Максимальная оценка: 5", output)
        self.assertIn("ОТЧЕТ ПО ОТЗЫВАМ", output)
        self.assertIn("До свидания!", output)


if __name__ == "__main__":
    unittest.main()
