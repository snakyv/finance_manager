from datetime import timedelta
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from expenses.models import Expense, Income, CategoryBudget
from expenses.ml.expense_classifier import predict_category
from expenses.emotion_rules import analyze_emotional_expense


class Command(BaseCommand):
    help = "Создаёт тестовые данные: користувача, доходи, витрати, бюджети."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="bob",
            defaults={"email": "bob@example.com"}
        )
        if created:
            user.set_password("bob12345")
            user.save()
            self.stdout.write(self.style.SUCCESS(
                "Створено тестового користувача: логін=bob, пароль=bob12345"
            ))
        else:
            self.stdout.write("Користувач 'bob' вже існує.")

        if Expense.objects.filter(user=user).exists() or Income.objects.filter(user=user).exists():
            self.stdout.write(self.style.WARNING(
                "У користувача вже є витрати/доходи. Нові дані будуть додані поверх існуючих."
            ))

        now = timezone.now()

        income_templates = [
            ("Зарплата основна", 25000, "salary"),
            ("Фріланс проект", 8000, "freelance"),
            ("Подарунок на День народження", 3000, "gift"),
            ("Повернення боргу", 2000, "other"),
        ]

        for weeks_ago in range(0, 8, 2):
            for desc, amount, cat in income_templates:
                created_at = now - timedelta(weeks=weeks_ago, days=random.randint(0, 3))
                Income.objects.create(
                    user=user,
                    amount=amount,
                    category=cat,
                    description=desc,
                    created_at=created_at,
                )

        self.stdout.write(self.style.SUCCESS("Створено тестові доходи."))

        expense_templates = [
            ("McDonalds lunch", 220, 12),
            ("KFC late dinner", 260, 10),
            ("Supermarket groceries", 850, 5),
            ("Pizza Hut delivery", 300, 7),
            ("Кава Starbucks", 120, 3),

            ("Uber to university", 95, 15),
            ("Metro ticket", 40, 20),
            ("Taxi at night", 180, 8),

            ("Rozetka electronics order", 3200, 18),
            ("AliExpress gadgets", 900, 25),
            ("New sneakers Nike", 2700, 30),

            ("Cinema tickets", 280, 6),
            ("Netflix monthly subscription", 250, 28),
            ("Steam games sale", 600, 14),
            ("Bar with friends", 450, 4),

            ("Electricity bill", 1100, 22),
            ("Gas bill", 900, 24),
            ("Water bill", 300, 26),
            ("Pharmacy vitamins", 350, 9),
            ("Doctor visit", 800, 16),
            ("Random purchase", 150, 2),
        ]

        for desc, base_amount, days_ago in expense_templates:
            amount = base_amount + random.randint(-50, 50)
            created_at = now - timedelta(days=days_ago)
            hour = random.choice([11, 13, 17, 20, 22])
            created_at = created_at.replace(
                hour=hour, minute=random.randint(0, 59), second=0, microsecond=0
            )

            cat, conf = predict_category(desc)
            from expenses.models import Expense as ExpenseModel
            valid_categories = {c[0] for c in ExpenseModel.CATEGORY_CHOICES}
            if cat not in valid_categories:
                cat = "other"

            is_emotional, tag = analyze_emotional_expense(desc, cat, created_at)

            Expense.objects.create(
                user=user,
                amount=amount,
                description=desc,
                created_at=created_at,
                category=cat,
                ml_confidence=conf,
                is_emotional=is_emotional,
                emotional_tag=tag,
                notes="test data",
            )

        self.stdout.write(self.style.SUCCESS("Створено тестові витрати."))

        # 5. Бюджети по категоріях
        CategoryBudget.objects.get_or_create(
            user=user, category="food",
            defaults={"monthly_limit": 4000}
        )
        CategoryBudget.objects.get_or_create(
            user=user, category="transport",
            defaults={"monthly_limit": 1500}
        )
        CategoryBudget.objects.get_or_create(
            user=user, category="shopping",
            defaults={"monthly_limit": 5000}
        )
        CategoryBudget.objects.get_or_create(
            user=user, category="entertainment",
            defaults={"monthly_limit": 3000}
        )
        CategoryBudget.objects.get_or_create(
            user=user, category="bills",
            defaults={"monthly_limit": 4500}
        )
        CategoryBudget.objects.get_or_create(
            user=user, category="health",
            defaults={"monthly_limit": 2000}
        )

        self.stdout.write(self.style.SUCCESS("Створено тестові бюджети."))
        self.stdout.write(self.style.SUCCESS("Готово! Перевірте дашборд та інші сторінки."))
