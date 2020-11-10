"use strict";
const BASE_URL = '/api/sales/summary/';

window.addEventListener('load', function () {
  let ctx = document.getElementById('myChart').getContext('2d');
  let myChart = new Chart(ctx, {
    type: 'bar',
    options: {
      maintainAspectRatio: true,
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
            callback: function (value, index, values) {
              return '$' + value.toLocaleString();
            }
          }
        }]
      },
      legend: {
        display: false
      },
      tooltips: {
        callbacks: {
          label: function (tooltipItem, data) {
            return '$' + tooltipItem.yLabel.toLocaleString() + ' USD';
          }
        }
      }
    }
  });

  function updateChart(url) {
    fetch(url)
      .then((resp) => resp.json())
      .then((resp) => {
        let data = {};
        data.labels = resp.result.map((o) => o.year);
        data.datasets = [{
          data: resp.result.map((o) => o.avg)
        }];
        myChart.data = data;
        myChart.update();
      })
      .catch((e) => {
        console.log(e);
      });
  }

  updateChart(BASE_URL);

  const form = document.getElementById('form');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = new FormData(e.target);

    let qs = [...formData.entries()].map(([name, value]) => {
      return encodeURIComponent(name) + "=" + encodeURIComponent(value);
    }).join("&");

    updateChart(BASE_URL + "?" + qs);
  });
});
