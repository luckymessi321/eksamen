// koden for funksjonen 'sendScore(score)' er tatt fra en venn sitt prosjekt
const grid = document.getElementsByClassName("grid")[0] 
const startDisplayButton = document.getElementById("start")
const score = document.getElementById("score")
const music = new Audio('static/audio/invisible.mp3')
const gasp = new Audio('static/audio/gasp.mp3')
const voiceline = new Audio('static/audio/voiceline.mp3')
const ammo = new Audio('static/audio/ammo.mp3')
const snake = new Audio('static/audio/snake.mp3')
let buttonPressed = false
let gameStopped = false
let squares = []
let currentSnake = [2,1,0]
let direction = 1
let gridWidth = 10
let appleIndex = 0
let count = 0
let currentInterval = 1000
let moveTimeout;
music.volume = 0.5
snake.volume = 0.5

// funksjon som sender score til app.py
function sendScore(score) {
    // henter ruten '/save_score' fra app.py og sender data til ruten som en JSON fil. denne dataen blir lagret som en ordbok
    fetch('/save_score', {
        // forteller funksjonen at den skal bruke POST-metoden etter å ha hentet ruten
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // spesifiserer at innholdet som blir sendt er en JSON fil
        },
        // konverterer dataen til en JSON streng. dette gjøres fordi JSON kun kan motta strenger
        body: JSON.stringify({ score: score })    
    })
    // leser JSON-dataen (response) KUN når dataen er mottatt fra app.py i 'fetch()' funksjonen og konverterer det til et javascript objekt slik at script.js kan lese det
    .then(response => response.json())
    // dette utføres KUN når mer data er mottatt etter det første 'then' statementet. denne dataen sendes fra app.py
    .then(data => {
        // logger at score ble lagret og dataen mottatt i webkonsollen. denne koden kjører KUN om nøkkelen 'status' i ordboken data har verdien 'success'
        if(data.status === 'success'){
            console.log('score lagret', data)
        // logger at det var en feil og dataen mottatt i webkonsollen. denne koden kjører KUN når nøkkelen 'status' i data ikke har verdien 'success'
        } else if (data.status === 'score too low') {
            console.log('score too low', data)
        } else {
            console.log('feil ved lagring av score', data);
        }
    })
    // fanger og håndterer eventuelle feilmeldinger som oppstår og logger dem som errors. denne koden er bra for å teste nettsider siden nettsiden ikke krasjer, og feilmeldinger blir logget. denne koden kjører KUN om en feilmelding oppstår i sendScore funksjonen
    .catch(error => console.error('Error:', error));
}

function startButton () {
    if (!buttonPressed) {
        startGame()
        buttonPressed = true
    } else {
        restartGame()
    }
}

function startGame () {
    createGrid()
    currentSnake.forEach(index => squares[index].classList.add('snake'))
    generateApple()
    move()
    console.log('game started')
}

function restartGame () {
    sendScore(count)
    squares.forEach(square => square.classList.remove('apple'))
    currentSnake.forEach(index => squares[index].classList.remove('snake'))
    currentSnake = [2,1,0]
    direction = 1
    gridWidth = 10
    appleIndex = 0
    count = 0
    currentInterval = 1000
    updateScore()
    currentSnake.forEach(index => squares[index].classList.add('snake'))
    generateApple()
    clearTimeout(moveTimeout)
    gameStopped = false
    move()
    console.log('game restarted')
}

function playSoundEffect() {
    let number = Math.floor(Math.random() * 100)
    if (number >= 0 && number <= 25) {
        ammo.play()
    }else if (number >= 26 && number <= 50) {
        gasp.play()
    } else if (number >= 51 && number <= 75) {
        voiceline.play()
    } else if (number >= 76 && number <= 100) {
        snake.play()
    }
}

function updateScore() {
    if (score) score.textContent = `${count}`;
}

function createGrid() {
    //lager 100 av firkantene med en for-løkke
    for (let i = 0; i < 100; i++) {
        //lager element 'square'
        const square = document.createElement('div')
        //legger til styling for firkantene
        square.classList.add('square')
        //legger til firkant i grid-en
        grid.appendChild(square)
        //lagrer firkantene til en ny tabell
        squares.push(square)
    }
}


function move() {
    if (
        (currentSnake[0] >= 90 && currentSnake[0] <= 100 && direction === 10) || // om snake head er på bunnen av grid
        (currentSnake[0] >= 0 && currentSnake[0] <= 9 && direction === -10) || // om snake head er på toppen av grid
        (currentSnake[0] % 10 === 0 && direction === -1) || // om snake head er ved venstre vegg av grid
        (currentSnake[0] % 10 === 9 && direction === 1) || // om snake head er ved høyre vegg av grid
        squares[currentSnake[0] + direction].classList.contains('snake') // om snake crasher i seg selv
    ) {
        music.pause()
        console.log('game stopped')
        gameStopped = true
        alert('Game over!')
        restartGame()
        return
    } else {
        //fjerner siste element/firkant i currentSnake tabellen
        const tail = currentSnake.pop()
        //fjerner styling fra siste element/firkant
        squares[tail].classList.remove('snake')
        //legger til firkanter i retningen slangen flytter seg
        currentSnake.unshift(currentSnake[0] + direction)   
        //legger til styling til de nye firkantene
        squares[currentSnake[0]].classList.add('snake')
        // bestemmer hva som skjer om snake spiser et eple
        if (squares[currentSnake[0]].classList.contains('apple')) {
            //fjerner klassen til eplet slik at det ser ut som om det ble spist
            squares[currentSnake[0]].classList.remove('apple')
            //øker snake lengde
            squares[tail].classList.add('snake')
            //legger til en ny firkant i currentSnake slik at halen (tail) følger resten av snake
            currentSnake.push(tail)
            //lager et nytt eple
            generateApple()
            //legger til 1 til scoren
            count++
            updateScore()
            playSoundEffect()
            //endrer farten på snake
            if (currentInterval > 500) {
                currentInterval -= 50
            }
        }
    }
    if (!gameStopped) {
        moveTimeout = setTimeout(move, currentInterval)
    }
}

function generateApple () {
    do {
        // generer tilfeldig tall
        appleIndex = Math.floor(Math.random() * squares.length)
    } while (squares[appleIndex].classList.contains('snake'))
    squares[appleIndex].classList.add('apple') 
}

function controlMusic (event) {
    if (event.key === 'p' || event.key === 'P') {
        music.play()
    }
    if (event.key === 'm' || event.key === 'M') {
        music.pause()
    }
}


function control(e) {
  if (e.key === 'ArrowRight' && direction != -1) {
    direction = 1
  } else if (e.key === 'ArrowUp' && direction != gridWidth) {
    direction = -gridWidth
  } else if (e.key === 'ArrowLeft' && direction != 1) {
    direction = -1
  } else if (e.key === 'ArrowDown' && direction != -gridWidth) {;
    direction = +gridWidth
  }
}


document.addEventListener('keydown', control);
document.addEventListener('keydown', controlMusic);
startDisplayButton.addEventListener('click', startButton)