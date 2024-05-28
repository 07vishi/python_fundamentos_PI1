document.getElementById('expense-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const description = document.getElementById('description').value;
    const amount = document.getElementById('amount').value;

    if (description && amount) {
        addExpense(description, amount);
        document.getElementById('description').value = '';
        document.getElementById('amount').value = '';
    }
});

async function addExpense(description, amount) {
    const response = await fetch('/api/expenses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ description, amount })
    });

    const expense = await response.json();
    displayExpense(expense);
}

function displayExpense(expense) {
    const expenseList = document.getElementById('expense-list');
    const li = document.createElement('li');
    li.textContent = `${expense.description}: $${expense.amount}`;
    expenseList.appendChild(li);
}
