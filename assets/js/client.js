// Show loading notice
const canvas = document.getElementById('videoCanvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = color;
ctx.fillText('Loading...', canvas.width / 2 - 30, canvas.height / 3);

// Setup the WebSocket connection and start the player
const cameraClient = new WebSocket(`ws://${window.location.hostname}:${cameraPort}/`);
const player = new jsmpeg(cameraClient, {canvas: canvas});

const sensorsClient = new WebSocket(`ws://${window.location.hostname}:${sensorsPort}/`);
sensorsClient.onmessage = function (event) {
    const isCameraFrame = event.data instanceof Blob;

    if (!isCameraFrame) {
        const data = JSON.parse(event.data);

        console.log(data);
    }
};