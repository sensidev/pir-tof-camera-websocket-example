(function ($) {

    const Client = {

        init: function () {
            const canvas = document.getElementById('video-canvas');
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
                    const payload = JSON.parse(event.data);

                    if (payload['sensor_type'] === 'ToF') {
                        Client.displayToFSensors(payload['data']);
                    } else if (payload['sensor_type'] === 'PIR') {
                        Client.displayPIRSensors(payload['data']);
                    }

                    console.log(payload);
                }
            };
        },

        displayToFSensors(data) {

        },

        displayPIRSensors(data) {
            const children = $('#pir-sensors').children();

            if (!children.length) {
                for (let i = 0; i <= data.length; i++) {
                    children.add($('<div>'));
                }
            }
        }

    };


    Client.init();

})($);