var num = 0; // Number of (whatever unit we're using) that the player has obtained

// all in seconds
var timerSec = 60;
var timeToEnableTimer = 5;
var timeToAutoStop = timerSec - timeToEnableTimer;

var isTimerEnabled = false;
setInterval(updateTimer, 1);
document.getElementById('timer').innerHTML = secondsToTime(timerSec);

function onCoffeeButtonPress() {
    if (timerSec > 0) {
        num++;
        document.getElementById('num').innerHTML = num;
        isTimerEnabled = true;
        timeToAutoStop = timerSec - timeToEnableTimer;
    }
}

// Should be called 100 times every second
function updateTimer() {
    if (isTimerEnabled) {
        timerSec-=0.01;
        document.getElementById('timer').innerHTML = secondsToTime(timerSec);
        if (timerSec <= 0) {
            isTimerEnabled = false;
            timerSec = 0;
            timeToAutoStop = 0;
        } else if (timeToAutoStop >= timerSec) {
            isTimerEnabled = false;
            timerSec = timeToAutoStop;
        }
    }
}

function secondsToTime(seconds) {
    if (seconds <= 0) return "00:00"
    M = Math.floor(seconds/60)
    S = Math.ceil(seconds % 60 * 100)/100
    if (S < 10) S = "0" + S
    if (M < 10) M = "0" + M
    return M + ":" + S
}