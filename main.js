/* global $, hsvToHex */
var extrema = {}

// Coloring
function colorCell (row, hue, data, name, colIndex) {
  var range = extrema[colIndex].max - extrema[colIndex].min
  var weight = (data[name] - extrema[colIndex].min) / range
  var color = hsvToHex(hue, weight, 1)
  $(row).find(`td:eq(${colIndex})`).css('background-color', color)
}

// Filtering
$.fn.dataTable.ext.search.push(
  function (settings, data, dataIndex) {
    var validPositions = {
      'QB': $('#QB').prop('checked'),
      'RB': $('#RB').prop('checked'),
      'WR': $('#WR').prop('checked'),
      'TE': $('#TE').prop('checked'),
      'UNK': false
    }
    var pos = data[3] || 'UNK'
    return validPositions[pos]
  }
)

$(document).ready(function () {
  // Create table
  var table = $('#scores').DataTable({
    paging: false,
    order: [[ 5, 'desc' ]],
    scrollY: 'calc(100vh - 93.5px)',
    scrollCollapse: true,
    dom: '<"toolbar">frtip',
    bInfo: false,
    bAutoWidth: false,
    ajax: {
      url: '2017.json',
      dataSrc: ''
    },
    columns: [
      {
        data: null,
        orderable: false
      },
      { data: 'full_name' },
      { data: 'team' },
      { data: 'position' },
      { data: 'games_played' },
      {
        data: 'fantasy_points',
        render: $.fn.dataTable.render.number('', '.', 1, '')
      },
      { data: 'plays' },
      {
        data: 'points_per_play',
        render: $.fn.dataTable.render.number('', '.', 1, '')
      },
      { data: 'yards' },
      { data: 'touchdowns' },
      {
        data: 'value_over_replacement_player',
        render: $.fn.dataTable.render.number('', '.', 1, '')
      },
      {
        data: 'value_over_replacement_flex',
        render: $.fn.dataTable.render.number('', '.', 1, '')
      },
      { data: 'passing_yards' },
      { data: 'passing_attempts' },
      {
        data: 'passing_yards_per_attempt',
        render: $.fn.dataTable.render.number('', '.', 1, '')
      },
      { data: 'receiving_yards' },
      { data: 'receiving_targets' },
      {
        data: 'receiving_yards_per_target',
        render: $.fn.dataTable.render.number('', '.', 1, '')
      },
      { data: 'rushing_yards' },
      { data: 'rushing_attempts' },
      {
        data: 'rushing_yards_per_attempt',
        render: $.fn.dataTable.render.number('', '.', 1, '')
      }
    ],
    rowCallback: function (row, data, index) {
      var orangeHue = 0.12
      var i = 4
      colorCell(row, orangeHue, data, 'games_played', i++)
      colorCell(row, orangeHue, data, 'fantasy_points', i++)
      colorCell(row, orangeHue, data, 'plays', i++)
      colorCell(row, orangeHue, data, 'points_per_play', i++)
      colorCell(row, orangeHue, data, 'yards', i++)
      colorCell(row, orangeHue, data, 'touchdowns', i++)
      colorCell(row, orangeHue, data, 'value_over_replacement_player', i++)
      colorCell(row, orangeHue, data, 'value_over_replacement_flex', i++)
      colorCell(row, orangeHue, data, 'passing_yards', i++)
      colorCell(row, orangeHue, data, 'passing_attempts', i++)
      colorCell(row, orangeHue, data, 'passing_yards_per_attempt', i++)
      colorCell(row, orangeHue, data, 'receiving_yards', i++)
      colorCell(row, orangeHue, data, 'receiving_targets', i++)
      colorCell(row, orangeHue, data, 'receiving_yards_per_target', i++)
      colorCell(row, orangeHue, data, 'rushing_yards', i++)
      colorCell(row, orangeHue, data, 'rushing_attempts', i++)
      colorCell(row, orangeHue, data, 'rushing_yards_per_attempt', i++)
    }
  })

  // Toolbar
  $('div.toolbar').html(`
    <fieldset>
      <legend>Positions:</legend>
      <input type="checkbox" id="QB" name="position" value="QB" checked>
      <label for="QB">QB</label>
      <input type="checkbox" id="RB" name="position" value="RB" checked>
      <label for="RB">RB</label>
      <input type="checkbox" id="WR" name="position" value="WR" checked>
      <label for="WR">WR</label>
      <input type="checkbox" id="TE" name="position" value="TE" checked>
      <label for="TE">TE</label>
    </fieldset>`)

  $('.toolbar input').change(function () {
    table.draw()
  })

  // Add row numbers
  // Modified from https://datatables.net/examples/api/counter_columns.html
  table.on('search.dt', function () {
    table.column(0, {search: 'applied', order: 'applied'})
      .nodes().each(function (cell, i) {
        cell.innerHTML = i + 1
      })
  }).draw()

  // Selection
  $('#scores tbody').on('click', 'tr', function () {
    $(this).toggleClass('selected')
  })

  // Max
  table.on('preDraw', function () {
    for (var i = 4; i <= 20; i++) {
      extrema[i] = {
        max: maxInColumn(i),
        min: minInColumn(i)
      }
    }
  })

  function maxInColumn (colIndex) {
    return table.column(colIndex, {search: 'applied'}).data()
      .reduce(function (a, b) {
        return Math.max(a, b)
      })
  }

  function minInColumn (colIndex) {
    return table.column(colIndex, {search: 'applied'}).data()
      .reduce(function (a, b) {
        return Math.min(a, b)
      })
  }
})
