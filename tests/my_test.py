
import py
import pytest
from app.calculation import add, divide, multiply, subtract,BankAccount,Insufficient

@pytest.fixture
def zero_bal_acc():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (7,5,12)
])



def test_add(num1,num2,expected):
    print("lets do it")
    assert add(num1,num2) == expected

def test_subtract():
    assert subtract(5,3) == 2

def test_multiply():
    assert multiply(5,3) == 15

def test_divide():
    assert divide(20,5) == 4

#test_add()


def test_bank_set_initial_amount(bank_account):
 #   bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_deposit(bank_account):
 #   bank_account = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_interest():
    bank_account = BankAccount(100)
    bank_account.col_int()
    assert round(bank_account.balance,3) == 110


@pytest.mark.parametrize("depamt,withamt,bal",[(100,75,25)])

def test_transaction(zero_bal_acc,depamt,withamt,bal):
    zero_bal_acc.deposit(depamt)
    zero_bal_acc.withdraw(withamt) 
    assert zero_bal_acc.balance == bal

def test_suff_bal(bank_account):
    with pytest.raises(Insufficient):
        bank_account.withdraw(100)