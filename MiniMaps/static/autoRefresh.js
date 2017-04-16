// Refresh the page every 'refreshRate' seconds
var refreshRate = 30; // In seconds please
var seconds = 0; // For countdown
var status = document.getElementById('status');

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function convertSeconds(s) {
    // Convert milliseconds to seconds
    return s * 1000;
}

function updateTimer() {
    seconds++;
    status.innerHTML = 'Client Statuses - Refresh in ' + (refreshRate - seconds);
}
async function refresh() {
    await sleep(convertSeconds(refreshRate));
    location.reload(false);
}

refresh();