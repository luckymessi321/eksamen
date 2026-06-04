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
  // Use string values for the 'e.key' property for modern compatibility
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