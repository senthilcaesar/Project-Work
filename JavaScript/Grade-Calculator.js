let gradeCalculator = function (studentScore, totalScore) {

    let percent = (studentScore/totalScore)*100
    if (percent >= 90) {
        console.log(`You got a A (${percent}%)!`)
    } else if (percent >= 80) {
        console.log(`You got a B (${percent}%)!`)
    } else if (percent >= 70) {
        console.log(`You got a C (${percent}%)!`)
    } else if (percent >= 60) {
        console.log(`You got a D (${percent}%)!`)
    } else {
        console.log(`You got a F (${percent}%)!`)
    }
}

gradeCalculator(19,20)
gradeCalculator(16, 20)
gradeCalculator(15, 20)
gradeCalculator(12, 20)
gradeCalculator(5, 20)
