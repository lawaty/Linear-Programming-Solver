$(document).ready(() => {
  $("#solveBtn").on('click', function () {
    let method = $("#lpMethod").val();
    let objective = $("#objective").val().split(",").map(Number);

    let constraints_type = [];
    let constraints = [];
    let rhs = [];

    $("#constraints").val().split("\n").forEach(row => {
      let parts = row.split(",");
      let typeIndex = parts.findIndex(val => val === "<=" || val === ">=" || val === "="); // Find the constraint type index

      if(method == 'simplex' && parts.includes('>='))
        alert('simplex cannot solve constraints with ">=" sign')

      if (typeIndex !== -1) {
        constraints_type.push(parts[typeIndex]); // Store constraint type
        rhs.push(Number(parts[parts.length - 1])); // Extract the RHS value (last item)

        // Extract constraint coefficients (excluding type and RHS)
        let coeffs = parts.slice(0, typeIndex).map(Number);
        constraints.push(coeffs);
      }
    });

    let jsonData = {
      "objective": objective,
      "constraints": constraints,
      "rhs": rhs,
      "constraints_type": constraints_type
    };

    $.ajax({
      url: `http://127.0.0.1:5000/api/solve/${method}`,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(jsonData),
      success: function (response) {
        console.log(response);
        $("#output").html("");

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
