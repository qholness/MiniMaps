function within(x,y,z=10) {
    // Check if x is within z of y
    if (Math.abs(x - y) < z) {
        return true;
    }
    return false;
}
function pause() {
    // Handle pausing
    // Paused state is global
    if (paused) {
        paused = false;
    }
    else {
        paused = true;
    }
}