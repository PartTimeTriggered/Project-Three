let trace1 = {
    x: c_week,
    y: c_confirmed,
    name: 'Covid Cases',
    xaxis:'x',
    yaxis:'y',
    type: "scatter"
  };

let trace2 = {
    x: f_week,
    y: f_count,
    name: 'Flu Cases',
    xaxis:'x',
    yaxis: 'y2',
    type: "scatter"
    };

var layout = {
  title: 'Coeficientes',
  showlegend: true,
  legend: {
      "orientation": "h"
  },
  width: 800,
  height: 580,
  autosize: true,
  // margin: {
  //     l: 50, r: 70, b: 50, t: 50, pad: 2
  // },
  xaxis: {title: 'Ângulo [graus]'},
  yaxis: {title: '[kN/(m/s)²]'},
  yaxis2 = {
      title: '[kN.m/(m/s)²]',
      overlaying: 'y',
      side: 'right'
  }
}


let plotData = [trace1, trace2];

Plotly.newPlot("plot", plotData);



function plot(value) {
 console.log(value);
  const url = "/api/refresh/<value>" //document.getElementById("input").value;

  fetch(url).then(function(response) {
  return response.json();
  }).then(function(data) {
  console.log(data);
  let trace1 = {
      x: data.c_week,
      y: data.c_confirmed,
      name: 'Covid Cases',
      xaxis:'x',
      yaxis:'y',
      type: "scatter"
    };

  let trace2 = {
      x: data.f_week,
      y: data.f_count,
      name: 'Flu Cases',
      xaxis:'x',
      yaxis: 'y2',
      type: "scatter"
      };
  let layout = {
    title: "A Plotly plot" //title
  };
 Plotly.newPlot("plot", [trace1, trace2], layout);
}); 
} 