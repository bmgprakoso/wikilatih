var randomArray = (length) => Array.from({length: length}, () => Math.floor(Math.random() * 100));

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
    window.myPie = new Chart(document.getElementById('chart-clarity').getContext('2d'), getConfig('pie', randomArray(2)));
    window.myPie2 = new Chart(document.getElementById('chart-retention').getContext('2d'), getConfig('pie', randomArray(2)));
    window.myPie3 = new Chart(document.getElementById('chart-dau').getContext('2d'), getConfig('bar', randomArray(10)));
    window.myPie4 = new Chart(document.getElementById('chart-test-score').getContext('2d'), getConfig('line', randomArray(10)));
    window.myPie5 = new Chart(document.getElementById('chart-wikimedia-project').getContext('2d'), getConfig('bar', randomArray(10)));
};
