let total_donor_sink = JSON.parse(document.getElementById('d_sink_chart').textContent);
let chart_sink_kg = total_donor_sink.donor_sink;
let chart_sink_tonne = parseInt(chart_sink_kg / 1000);

let data = {
  labels: [
    'Ireland Emissions - Annual (Tonnes)',
    'Citizen Tree Sink - Annual (Tonnes)',
  ],
  datasets: [{
    label: 'Citizen Tree Sequestration',
    data: [60000000, chart_sink_tonne],
    backgroundColor: [
      'rgb(250, 250, 250)',
      'rgb(100, 0, 0)',
    ],
    hoverOffset: 4,
    cutout: '75%',
  }],
};
// https://www.chartjs.org/docs/latest/configuration/legend.html
// https://stackoverflow.com/questions/37292423/chart-js-label-color
let config = {
  type: 'doughnut',
  data: data,
  options: {
    plugins: {
      legend: {
        display: true,
        labels: {
          color: "white",
          font: {
            size: 20,
          }
        }
      }
    }
  }
};

let myChart = new Chart(
  document.getElementById('co2_doughnut'),
  config
);