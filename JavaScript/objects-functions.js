let myBook = {
    title: 'Gift of Imperfection',
    author: 'Senthil Caesar',
    pageCount: 456
}

let financeBook = {
    title: 'Rich Dad Poor Dad',
    author: 'Miko',
    pageCount: 213
}

// Functions that accepts the Object
let printBook = function (book) {
    return {
        summary:`${book.title} by ${book.author}`,
        pageCountsummary: `${book.title} is ${book.pageCount} pages long`
    }
}

let bookSummary = printBook(myBook)
let financeSummary = printBook(financeBook)
console.log(bookSummary.pageCountsummary)

// Challenge - Functions returns object
let tempConversion = function (farenhiet) {
    return {
        farenhiet: farenhiet,
        celcius: (farenhiet - 32) * (5 / 9),
        kelvin: (farenhiet + 459.67) * (5 / 9)
    }   
}

let tmp = tempConversion(32)
console.log(tmp)

















