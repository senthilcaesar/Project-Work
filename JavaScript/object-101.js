let myBook = {
    title: 'Gift of Imperfection', 
    author: 'Senthil Caesar',
    pageCount: 456
}

console.log(`${myBook.title} by ${myBook.author}`)
myBook.title = 'Animal Farm'
console.log(`${myBook.title} by ${myBook.author}`)

// Challenge area
let person = {
    firstName: 'Senthil',
    age: 23,
    location: 'Boston'
}

console.log(`${person.firstName} is ${person.age} lives in ${person.location}`)
person.age++
console.log(`${person.firstName} is ${person.age} lives in ${person.location}`)
