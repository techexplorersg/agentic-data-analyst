from app.security.sql_validator import SQLValidator


validator = SQLValidator()


def test_select_is_allowed():
    result = validator.validate(
        "SELECT customer_id, revenue FROM sales LIMIT 10"
    )

    assert result.allowed


def test_delete_is_blocked():
    result = validator.validate(
        "DELETE FROM customers"
    )

    assert not result.allowed


def test_drop_is_blocked():
    result = validator.validate(
        "DROP TABLE customers"
    )

    assert not result.allowed


def test_multiple_statements_are_blocked():
    result = validator.validate(
        "SELECT * FROM sales; DROP TABLE sales;"
    )

    assert not result.allowed


def test_cte_is_allowed():
    result = validator.validate(
        """
        WITH revenue AS (
            SELECT customer_id, SUM(amount) AS total
            FROM sales
            GROUP BY customer_id
        )
        SELECT *
        FROM revenue
        ORDER BY total DESC
        """
    )

    assert result.allowed
