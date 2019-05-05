var randomScalingFactor = function () {
    return Math.round(Math.random() * 100);
};

const getConfig = (type, dataArray) => {
    const backgroundColor = dataArray.map(_ => '#' + (Math.random() * 0xFFFFFF << 0).toString(16));
    const labels = dataArray.map((_, i) => `Label ${i}`);
    return {
        type: type,
        data: {
            datasets: [{
                data: dataArray,
                backgroundColor: backgroundColor,
                label: 'Dataset'
            }],
            labels: labels
        },
        options: {
            responsive: true
        },
    };
};

window.onload = function () {
    var chartEvaluation1 = document.getElementById('chart-evaluation-1').getContext('2d');
    var chartEvaluation2 = document.getElementById('chart-evaluation-2').getContext('2d');
    var chartEvaluation3 = document.getElementById('chart-evaluation-3').getContext('2d');
    var chartEvaluation4 = document.getElementById('chart-evaluation-4').getContext('2d');
    var chartEvaluation5 = document.getElementById('chart-evaluation-5').getContext('2d');
    var chartEvaluation6 = document.getElementById('chart-evaluation-6').getContext('2d');

    window.myPie = new Chart(chartEvaluation1, getConfig('pie', [
        randomScalingFactor(),
        randomScalingFactor(),
    ]));
    window.myPie2 = new Chart(chartEvaluation2, getConfig('pie', [
        randomScalingFactor(),
        randomScalingFactor(),
    ]));
    window.myPie3 = new Chart(chartEvaluation3, getConfig('bar', [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
    ]));
    window.myPie4 = new Chart(chartEvaluation4, getConfig('line', [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
    ]));
    window.myPie5 = new Chart(chartEvaluation5, getConfig('line', [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
    ]));
    window.myPie6 = new Chart(chartEvaluation6, getConfig('line', [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
    ]));
};
