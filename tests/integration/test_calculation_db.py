from app.models.calculation import Calculation
from app.models.user import User


def make_user():
    return User(
        username="alice",
        email="alice@example.com",
        password_hash=User.hash_password("longenough1"),
    )


def test_calculation_stored_with_computed_result(db_session):
    calc = Calculation(a=2, b=3, type="Add")
    calc.compute()
    db_session.add(calc)
    db_session.commit()
    stored = db_session.query(Calculation).one()
    assert stored.result == 5
    assert stored.created_at is not None


def test_calculation_links_to_user(db_session):
    user = make_user()
    db_session.add(user)
    db_session.commit()
    calc = Calculation(a=10, b=2, type="Divide", user_id=user.id)
    calc.compute()
    db_session.add(calc)
    db_session.commit()
    stored = db_session.query(Calculation).filter_by(user_id=user.id).one()
    assert stored.result == 5


def test_deleting_user_cascades_to_calculations(db_session):
    user = make_user()
    db_session.add(user)
    db_session.commit()
    calc = Calculation(a=4, b=5, type="Multiply", user_id=user.id)
    calc.compute()
    db_session.add(calc)
    db_session.commit()
    db_session.delete(user)
    db_session.commit()
    assert db_session.query(Calculation).count() == 0
