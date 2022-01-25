$(window).on('load', function() {
  if (feather) {
    feather.replace({
      width: 14,
      height: 14
    });
  }

  var $ipv4 = window.location.pathname.split('?')[0].split('/').filter(function (i) { return i !== ""}).slice(-1)[0];
  get_info($ipv4);
});

function get_info(address) {
  $.get("/api/client", { ipv4: address }).done(function(data) {
    if (data["data"] != false) {
      $('#portsTable tbody tr').remove();
      $('#ipData').html(data["data"]["ipv4"]);
      $('#macData').html(data["data"]["mac"]);
      $('#lookupData').html(data["data"]["lookup"]);

      var $found = false;
      $.each(data["data"]["ports"], function(index, value) {
        $found = true;
        var $row = $('<tr>' +
                    '<td><b>' + value[0] + '</b></td>' +
                    '<td><b>' + value[1] + '</b></td>' +
                    '<td><b>' + value[2] + '</b></td>' +
                    '</tr>');

        $('table> tbody:last').append($row);
      });

      if ($found == false) {
        var $row = $('<tr><td> No open ports found!</td></tr>');
        $('table> tbody:last').append($row);
      }
    } else {
      $('#ipData').html('Error, no network connection!');

      $('#portsTable tbody tr').remove();    
    }
  });
}