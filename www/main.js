$(document).ready(() => {
  $("#lpMethod").on('change', function () {
    if ($(this).val() === "goal-programming") {
      $("#goalProgrammingOptions").show();
      $("#objective").closest('.mb-3').hide(); // Hide single-objective field
    } else {
      $("#goalProgrammingOptions").hide();
      $("#objective").closest('.mb-3').show(); // Show single-objective field
    }
  });

  $("#solveBtn").on('click', function () {
    let method = $("#lpMethod").val();
    let jsonData = {};

    if (method === "goal-programming") {
      let objectives = $("#objectives").val().split("\n").map(row => row.split(",").map(Number));
      let priorities = $("#priorities").val().split(",").map(Number);
      jsonData = { "objectives": objectives, "priorities": priorities };
    } else {
      let objective = $("#objective").val().split(",").map(Number);
      jsonData = { "objective": objective };
    }

    let constraints_type = [];
    let constraints = [];
    let rhs = [];

    $("#constraints").val().split("\n").forEach(row => {
      let parts = row.split(",");
      let typeIndex = parts.findIndex(val => ["<=", ">=", "="].includes(val));

      if (method === 'simplex' && parts.includes('>='))
        alert('simplex cannot solve constraints with ">=" sign');

      if (typeIndex !== -1) {
        constraints_type.push(parts[typeIndex]);
        rhs.push(Number(parts[parts.length - 1]));
        constraints.push(parts.slice(0, typeIndex).map(Number));
      }
    });

    jsonData["constraints"] = constraints;
    jsonData["rhs"] = rhs;
    jsonData["constraints_type"] = constraints_type;

    $.ajax({
      url: `http://127.0.0.1:5000/api/solve/${method}`,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(jsonData),
      success: function (response) {
        $("#output").html("");

        let feasibilityHtml = `<h5>Solution Feasibility: 
          <span class="badge ${response.feasible ? 'bg-success' : 'bg-danger'}">
            ${response.feasible ? 'Feasible' : 'Infeasible'}
          </span>
        </h5>`;
        $("#output").append(feasibilityHtml);

        response.history.forEach((table, index) => {
          let tableHtml = `<h5>Iteration ${index + 1}</h5><table class="table table-bordered table-striped"><tbody>`;
          table.forEach(row => {
            tableHtml += "<tr>" + row.map(cell => `<td>${cell.toFixed(2)}</td>`).join("") + "</tr>";
          });
          tableHtml += "</tbody></table>";
          $("#output").append(tableHtml);
        });

        if (response.feasible) {
          let solutionHtml = `<h5>Optimal Solution</h5><table class="table table-bordered">
            <tr><th>Variable</th><th>Value</th></tr>`;
          response.solution.forEach((val, idx) => {
            solutionHtml += `<tr><td>x${idx + 1}</td><td>${val.toFixed(2)}</td></tr>`;
          });

          if (method === "goal-programming") {
            solutionHtml += `<tr><td><strong>Optimal Values</strong></td><td><strong>${response.optimal_value.map(v => v.toFixed(2)).join(", ")}</strong></td></tr>`;
          } else {
            solutionHtml += `<tr><td><strong>Optimal Value</strong></td><td><strong>${response.optimal_value.toFixed(2)}</strong></td></tr>`;
          }

          solutionHtml += `</table>`;
          $("#output").append(solutionHtml);
        } else {
          $("#output").append("<p class='text-danger'>No feasible solution found.</p>");
        }
      },
      error: function (xhr, status, error) {
        $("#output").text("Error: " + xhr.responseText);
      }
    });
  });
});
