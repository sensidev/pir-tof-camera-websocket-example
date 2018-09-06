(function ($) {
    const Dashboard = {

        chartInstance: null,
        chartTimeAxisRangeInSeconds: 20,

        chartMotionDatasets: [],
        chartDistanceDatasets: [],

        init: function () {
            this.initLiveCamera();
            this.initSensors();
        },

        initSensors: function () {
            const sensorsClient = new WebSocket(`ws://${window.location.hostname}:${sensorsPort}/`);

            Dashboard.initChart();

            sensorsClient.onmessage = function (event) {
                const isCameraFrame = event.data instanceof Blob;

                if (!isCameraFrame) {
                    const payload = JSON.parse(event.data);

                    if (payload['type'] === 'distance') {
                        Dashboard.plotDistanceSensorsDataReadFor(payload['samples']);
                    } else if (payload['type'] === 'motion') {
                        Dashboard.plotMotionSensorsDataReadFor(payload['samples']);
                    }
                }
            };
        },

        initLiveCamera: function () {
            const cameraClient = new WebSocket(`ws://${window.location.hostname}:${cameraPort}/`);
            const canvas = document.getElementById('video-canvas');
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = color;
            ctx.fillText('Loading...', canvas.width / 2 - 30, canvas.height / 3);

            new jsmpeg(cameraClient, {canvas: canvas});
        },

        plotDistanceSensorsDataReadFor(samples) {
            this.addDistanceChartDatasetsFor(samples);
            this.updateDatasets(Dashboard.chartDistanceDatasets, samples);
        },

        plotMotionSensorsDataReadFor(samples) {
            this.addMotionChartDatasetsFor(samples);
            this.updateDatasets(Dashboard.chartMotionDatasets, samples);
        },

        updateChart: function () {
            Dashboard.chartInstance.data.datasets = [];
            Dashboard.chartInstance.data.datasets.push(...Dashboard.chartMotionDatasets);
            Dashboard.chartInstance.data.datasets.push(...Dashboard.chartDistanceDatasets);
            Dashboard.chartInstance.update();
        },

        removeOldSamples: function () {
            const endDate = new Date();
            const startDate = new Date(endDate.getTime() - Dashboard.chartTimeAxisRangeInSeconds * 1000);

            Dashboard.chartInstance.data.datasets.forEach(function (dataset) {
                dataset.data.forEach(function (s) {
                    if (s['x'] < startDate) {
                        dataset.data.shift();
                    }
                })
            });
        },

        updateDatasets: function (datasets, samples) {
            for (let i = 0; i < samples.length; i++) {
                const s = samples[i];
                let data = datasets[i].data;

                data.push(Dashboard.getPreparedSampleDataFor(s));
            }

            this.removeOldSamples();
            this.updateChart();
        },

        getPreparedSampleDataFor: function (sample) {
            return {
                x: new Date(sample['sample']['timestamp'] * 1000),
                y: sample['sample']['value']
            };
        },

        createChartInstance: function (canvasId) {
            Dashboard.chartInstance = new Chart(document.getElementById(canvasId).getContext('2d'), {
                type: 'line',
                data: {
                    datasets: [],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    tooltips: {
                        enabled: false,
                    },
                    title: {
                        display: true,
                        text: 'Movement and Distance Sensor data reads over time'
                    },
                    scales: {
                        xAxes: [{
                            type: 'time',
                            display: false,
                        }],
                        yAxes: [{
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Distance in millimeters'
                            },
                            ticks: {
                                min: 0,
                                max: 1750,
                            }
                        }]
                    }
                }
            })
        },

        initChart: function () {
            const sensorsWrapper = $('#sensors-wrapper');
            const canvasId = 'chart-canvas';
            sensorsWrapper.append(Dashboard.getNewChartCanvas(canvasId));
            this.createChartInstance(canvasId);
        },

        addMotionChartDatasetsFor: function (samples) {
            if (Dashboard.chartMotionDatasets.length === 0) {
                samples.forEach(function (s) {
                    const color = Dashboard.getRandomColor();
                    Dashboard.chartMotionDatasets.push({
                        label: s.id,
                        borderColor: color,
                        backgroundColor: color,
                        pointRadius: 25,
                        pointStyle: 'circle',
                        showLine: false,
                        tension: 0,
                        data: []
                    });
                });
            }
        },

        addDistanceChartDatasetsFor: function (samples) {
            if (Dashboard.chartDistanceDatasets.length === 0) {
                samples.forEach(function (s) {
                    const color = Dashboard.getRandomColor();
                    Dashboard.chartDistanceDatasets.push({
                        borderColor: color,
                        backgroundColor: color,
                        label: s.id,
                        showLine: false,
                        tension: 0,
                        data: []
                    })
                });
            }
        },
        getNewChartCanvas: function (id) {
            return $('<canvas>').attr('id', id).width(400).height(400);
        },

        getRandomColor: function () {
            const letters = '0123456789ABCDEF';
            let color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        }
    };

    Dashboard.init();

})($);