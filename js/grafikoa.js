/**
 * Created by xenki on 14/04/15.
 */
      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.1', {packages: ['line']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

        // Create the data table.
      var data = new google.visualization.DataTable();
      data.addColumn('number', 'Ordua');
      data.addColumn('number', 'Barruko tenperatura');
      data.addColumn('number', 'Kanpoko tenperatura');

      data.addRows([
          [10,  14,   6],
          [11,  17,   7],
          [12,  18,   7],
          [13,  20,   8],
          [14,  21,   8],
          [15,  21,   8],
          [16,  21,   9],
          [17,  21,   9],
          [18,  19,   8],
          [19,  18,   7],
          [20,  17,   6],


      ]);

        // Set chart options
        var options = {
        chart: {
          title: 'Etxeko tenperatura',
          subtitle: 'Gradu zentigradutan'
        },
        width: 900,
        height: 300
      };
        // Instantiate and draw our chart, passing in some options.
        var chart = new google.charts.Line(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
