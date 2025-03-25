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
        console.log(response);
        $("#output").html(""); // Clear previous output

        // Display history as Bootstrap tables
        response.history.forEach((table, index) => {
          let tableHtml = `<h5>Iteration ${index + 1}</h5><table class="table table-bordered table-striped"><tbody>`;
          table.forEach(row => {
            tableHtml += "<tr>";
            row.forEach(cell => {
              tableHtml += `<td>${cell.toFixed(2)}</td>`; // Formatting numbers to 2 decimal places
            });
            tableHtml += "</tr>";
          });
          tableHtml += "</tbody></table>";
          $("#output").append(tableHtml);
        });

        // Display final solution
        let solutionHtml = `
          <h5>Optimal Solution</h5>
          <table class="table table-bordered">
            <tr><th>Variable</th><th>Value</th></tr>`;
        response.solution.forEach((val, idx) => {
          solutionHtml += `<tr><td>x${idx + 1}</td><td>${val.toFixed(2)}</td></tr>`;
        });
        solutionHtml += `
            <tr><td><strong>Optimal Value</strong></td><td><strong>${response.optimal_value.toFixed(2)}</strong></td></tr>
          </table>`;

        $("#output").append(solutionHtml);
      },
      error: function (xhr, status, error) {
        $("#output").text("Error: " + xhr.responseText);
      }
    });
  });
});
