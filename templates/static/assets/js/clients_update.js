// А за JavaScript и JQuery можешь не спрашивать
// Ибо тут явно много говнокода :)

$(document).on("change", "input[class='checkbox']", function () {
    localStorage.setItem($(this).attr('id'), this.checked);
});

$(window).on('load', function() {
  if (feather) {
    feather.replace({
      width: 14,
      height: 14
    });
  }

  var timerInterval = 60000;
  $.get('/api/interval',function(data) {
    timerInterval = data["interval"];
  });

  update();
  var timerId = setInterval(function() {
    update();
  }, timerInterval);
});

function update() {
    $.get('/api/check_network',function(data){
        if (data["data"] == true) {
          $.get("/api/clients", function(data) {
            $('#laptopsTable > tbody').html("");
            $('#phonesTable > tbody').html("");
            $('#tabletsTable > tbody').html("");

            var $numL = 1;
            var $numP = 1;
            var $numT = 1;
            var $num = 0;
            var $onlineCount = 0;
            var $offlineCount = 0;

            $.each(data["data"], function(index, value) {
              var $online = '<td class="activeDevice">';

              if (value["online"] == false) {
                $online = '<td class="defaultDevice">';
                $offlineCount += 1;
              } else {
                $onlineCount += 1;
              }

              if (value["category"] == "phone") { $num = $numP; $numP += 1; }
              if (value["category"] == "laptop") { $num = $numL; $numL += 1; }
              if (value["category"] == "tablet") { $num = $numT; $numT += 1; }

              var $actions = `<div class="d-flex align-items-center col-actions">` +
                                  `<input class="checkbox" type="checkbox" id="` + index + `">` +
                              `</div>`;

              var $row = $('<tr>' +
                         $online + $num + '</td>' +
                         '<td>' + value["device"] + '</td>' +
                         '<td><a href="/client/' + value["ipv4"] + '">' + value["ipv4"] + '</a></td>' +
                         '<td>' + value["mac"] + '</td>' +
                         '<td>' + value["last_discovery"] + '</td>' +
                         '<td>' + value["last_check"] + '</td>' + 
                         '<td>' + $actions + '</td>' +
                         '</tr>');

              $('#' + value["category"] + 'sTable > tbody').append($row);
            });

            $('input:checkbox').each(function(){
              var checked = JSON.parse(localStorage.getItem($(this).attr('id')));
              this.checked = checked;
            });

            $("#onlineBar").html("Online: " + $onlineCount);
            $("#offlineBar").html("Offline: " + $offlineCount);
          });
        } else {
          $('#laptopsTable > tbody').html("");
          $('#phonesTable > tbody').html("");
          $('#tabletsTable > tbody').html("");

          var $row = $('<tr><td> Error, no network connection!</td></tr>');
          $('#laptopsTable tr:last').after($row);
          $('#phonesTable tr:last').after($row);
          $('#tabletsTable tr:last').after($row);
        }
      });
}