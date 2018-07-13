let myAccount = {
    name: 'Andrew Mead',
    expenses: 0,
    income: 0
}

let addExpense = function (account, amount) {
    account.expenses = account.expenses + amount
}

let addIncome = function (account, amount) {
    account.income = account.income + amount
}

let resetAccount = function (account) {
    account.income = 0
    account.expenses = 0
}

let getAccountSummary = function (account) {
    let balance = account.income - account.expenses
    return `Account for ${account.name} has $${balance}.
            $${account.income} in income.
            $${account.expenses} in expenses.`
}

addExpense(myAccount, 100)
console.log(myAccount)
addIncome(myAccount, 1000)
console.log(myAccount)
resetAccount(myAccount)
console.log(myAccount)
summary = getAccountSummary(myAccount)
console.log(summary)