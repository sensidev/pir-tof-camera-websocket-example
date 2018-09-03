(function ($) {

    const Dashboard = {

        motionChart: null,

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

                    if (payload['type'] === 'distance') {
                        Dashboard.displayDistanceSensors(payload['samples']);
                    } else if (payload['type'] === 'motion') {
                        Dashboard.displayMotionSensors(payload['samples']);
                    }

                    console.log(payload);
                }
            };
        },

        displayDistanceSensors(data) {

        },

        updateMotionCharts: function (samples) {
            for (let i = 0; i < samples.length; i++) {
                const s = samples[i];

                let data = Dashboard.motionChart.data.datasets[i].data;

                data.push(Dashboard.getMotionDataFor(s));
            }


            Dashboard.motionChart.update();
        },

        displayMotionSensors(samples) {
            this.createMotionCharts(samples);
            this.updateMotionCharts(samples);
        },

        getMotionDataFor: function (sample) {
            return {
                x: new Date(sample['sample']['timestamp'] * 1000),
                y: sample['sample']['value']
            };
        },

        createMotionCharts: function (samples) {
            const motionSensorsWrapper = $('#motion-sensors');

            if (motionSensorsWrapper.is(':empty')) {
                const canvasId = 'motion-canvas';
                motionSensorsWrapper.append(Dashboard.getMotionCanvasFor(canvasId));
                Dashboard.motionChart = new Chart(document.getElementById(canvasId).getContext('2d'), {
                    type: 'bar',
                    data: {
                        datasets: Dashboard.getMotionChartDatasets(samples)
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Chart.js Time Point Data'
                        },
                        scales: {
                            xAxes: [{
                                type: 'time',
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Date'
                                },
                                ticks: {
                                    major: {
                                        fontStyle: 'bold',
                                        fontColor: '#FF0000'
                                    }
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'value'
                                }
                            }]
                        }
                    }
                })
            }
        },

        getMotionChartDatasets: function (samples) {
            let datasets = [];
            samples.forEach(function (s) {
                datasets.push({
                    label: s.id,
                    pointRadius: 10,
                    pointStyle: 'circle',
                    showLine: false,
                    tension: 0,
                    data: []
                })
            });
            return datasets;
        },


        getMotionCanvasFor: function (id) {
            return $('<canvas>').attr('id', id).width(400).height(400);
        },

    };


    Dashboard.init();

})($);