$(document).ready(function () {
  $("#solveBtn").click(function () {
    let method = $("#lpMethod").val();
    let inputData = $("#lpInput").val();

    try {
      let jsonData = JSON.parse(inputData);

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

    } catch (e) {
      alert("Invalid JSON input!");
    }
  });
});
