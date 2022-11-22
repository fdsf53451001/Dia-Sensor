/* globals Chart:false, feather:false */

/* globals Chart:false, feather:false */
// function createPieChart(){
//     var ctx = document.getElementById('pieChart').getContext('2d');
//     var myChart = new Chart(ctx, {
//       type: 'pie',
//       data: {
//         labels: ['正常人', '風險族群', '高度危險', '中度危險', '輕度危險'],
//         datasets: [{
//           label: '誤差值',
//           data: [80, 12.5, 12.5, 3, 2],
//           // borderColor: 'rgb(75, 192, 192)',
//           backgroundColor: ['#91C483','#FFE162','#9B0000','#FF6464','#FFAB76'],
//         }]
//       },
//       options: {
//         plugins:{
//         legend: {
//           display: true,
//           position: 'right',
          
//       },
//       },
//       }
//     });
// }


// function createScatterChart(){
//   console.log('text');
  
//   var ctx = document.getElementById("scatterChart").getContext('2d');
// console.log('text');
// axios.get('https://raw.githubusercontent.com/FreeCodeCamp/ProjectReferenceData/master/cyclist-data.json')
//   .then(function (response) {
//   // console.log(response);
//   var colouring = [];
//   var data = [];
//   var dopingData = [];
//   var notDopingData = [];

//   // console.log(time);
//   /*var description = document.getElementById("description");
//   description.innerText = response.data.description;*/
  
//   for (var i = 0; i < response.data.length; i++) {
//     if (response.data[i]["Doping"] === "") {
//       notDopingData.push({x: parseFloat(response.data[i]['Time'].replace(':','.')), y: response.data[i]['Place'], id: i});
//     } else {
//       dopingData.push({x: parseFloat(response.data[i]['Time'].replace(':','.')), y: response.data[i]['Place'], id: i});
//     }
//   }
//   var myChart = new Chart(ctx, {
//     type: 'scatter',
//     data: {
//       label: 'Scatter Dataset',
//       datasets: [{
//           data: notDopingData,
//           label: 'No Doping',
//           backgroundColor: 'rgba(255, 0, 0, 1)',
//         },
//         {
//           data: dopingData,
//           label: 'Doping',
//           backgroundColor: 'rgba(0, 0, 255, 1)'
//         }]
//     },
//     options: {
//       title: {
//         display: true,
//         text: "35 Fastest times up Alpe d'Huez"
//       },
//       legend: {
//         display: true,
//       },
      
//       showLines: false,
//       scales: {
//         yAxes: [{
//           display: true,
//           scaleLabel: {
//             display: true,
//             labelString: 'Rank',
//             fontSize: 16
//           },
//           ticks: {
//             beginAtZero:true,
//             fontSize: 14
//           }
//         }],
//         xAxes: [{
//           type: 'linear',
//           position: 'bottom',
//           display: true,
//           scaleLabel: {
//             display: true,
//             labelString: 'Time (Minutes)',
//             fontSize: 16
//           },
//           gridLines: {
//             display: true
//           },
//           ticks: {
//             beginAtZero:false,
//             fontSize: 14,
//           }
//         }]
//       },
//       tooltips: {
//         displayColors: false,
//         callbacks: {
//           title: function(tooltipItems, data) {
//             var index = tooltipItems[0].index;
//             var datasetIndex = tooltipItems[0].datasetIndex;
//             var dataset = data.datasets[datasetIndex];
//             var datasetItem = dataset.data[index];
            
//             var person = response.data[datasetItem.id];
//             return person.Name + " - " + person.Nationality;
//           },
//           label: function(tooltipItems, data) {
//             var output = "";
            
//             var index = tooltipItems.index;
//             var datasetIndex = tooltipItems.datasetIndex;
//             var dataset = data.datasets[datasetIndex];
//             var datasetItem = dataset.data[index];
            
//             var person = response.data[datasetItem.id];
            
//             output += "TIme: " + person.Time + "\n | \n";
//             output += "Place: " + person.Place + "\n | \n";
//             output += "Year: " + person.Year + "\n | \n";
//             if (person.Doping === "") {
//               output += "Doping: None";
//             } else {
//               output += "Doping: " + person.Doping;
//             }
//             return output;
//           }
//         }
//       }
//     }
//   });

// })
//   .catch(function (error) {
//   console.log(error);
// });
// }