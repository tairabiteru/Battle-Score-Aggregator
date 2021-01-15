
// Read and serialize the information from the current table.
function readTable() {
  var table = document.getElementById("scoretable");
  output = [];
  for (i=1; i<table.rows.length; i++) {
    row = table.rows[i];
    var rowdata = [];
    for (j=1; j<row.cells.length; j++) {
      cell = row.cells[j];
      rowdata.push(cell.firstChild.value);
    }
    output.push(rowdata);
  }
  return output;
}

// Do the AJAX SHUFFLE ( ﾟヮﾟ)
// (Facilitates communication between the server and the page)
function communicate(endpoint, data, method="POST", type="application/json") {
  var xhr = new XMLHttpRequest();
  return new Promise(function (resolve, reject) {
    xhr.onreadystatechange = function () {
      // We should only run the next code if the request is complete.
      if (xhr.readyState !== 4) {
        return;
      }

      // If all good, resolve response.
      if (xhr.status == 200) {
        resolve(xhr.responseText);
      } else {
        // else, reject it.
        reject({
          status: xhr.status,
          statusText: xhr.statusText
        });
      }
    };
    xhr.open(method, endpoint);
    xhr.setRequestHeader("Content-Type", type);
    xhr.send(data);
  });
}

// Validate scores.
function validateScore() {
  var data = readTable();
  var validScores = ["0", "1", "2", "4", "5"];
  var valid = true;

  for (i=0; i<data.length; i++) {
    for (j=0; j<data[i].length; j++) {
      var team = document.getElementById("team_" + (j + 1)).innerHTML;
      var box = document.getElementById(team + "_" + (i + 1));
      if (box.value == "") {
        box.style = "background-color: inherit;";
      } else if (!validScores.includes(box.value)) {
        box.style = "background-color: #ff5c5c;";
        toastr.error("Invalid value '" + box.value + "' entered. Value must be 0, 1, 2, 4 or 5.");
        box.value = "";
        valid = false;
      } else {
        box.style = "background-color: #4CAF50;";
      }
    }
  }

  if (valid) {
    saveScores();
  }
}

// Called to send scores to AJAX.
function saveScores() {
  var endpoint = "/api/save-scores";
  var data = readTable();

  data = JSON.stringify(data);
  result = communicate(endpoint, data)
    .then(function (result) {
      if (result.includes("Error")) {
        alert("Error!")
      } else {

      }
    })
    .catch(function (error) {
      console.warn("Communication failure:", error);
      alert("Communications failure!")
    });
}


// Perform on page load
document.addEventListener('DOMContentLoaded', function(event) {
  validateScore();
});
