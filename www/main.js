
$(document).ready(function () {
  $("#solveBtn").click(function () {
    let method = $("#lpMethod").val();
    let objective = $("#objective").val().split(",").map(Number);
    let constraints = $("#constraints").val().split("\n").map(row => row.split(",").map(val => isNaN(val) ? val : Number(val)));
    let rhs = $("#rhs").val().split(",").map(Number);

    let jsonData = {
      "objective": objective,
      "constraints": constraints,
      "rhs": rhs
    };

    $.ajax({
      url: `http://127.0.0.1:5000/api/solve/${method}`,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(jsonData),
      success: function (response) {
        $("#output").text(JSON.stringify(response, null, 4));
      },
      error: function (xhr, status, error) {
        $("#output").text("Error: " + xhr.responseText);
      }
    });
  });
});
