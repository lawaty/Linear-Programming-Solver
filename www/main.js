$(document).ready(function () {
  $("#solveBtn").click(function () {
    let method = $("#lpMethod").val();
    let objective = [...$("#objective").val().split(",").map(Number), 0];

    let constraints = $("#constraints").val().split("\n").map(row => {
      return row.split(",").filter(val => val !== "<=" && val !== ">=").map(Number);
    });

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
        console.log(response)
        $("#output").text(JSON.stringify(response, null, 4));
      },
      error: function (xhr, status, error) {
        $("#output").text("Error: " + xhr.responseText);
      }
    });
  });
});
