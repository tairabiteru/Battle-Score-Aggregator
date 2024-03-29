function decodeHTML(html) {
  var txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
}


// Read and serialize the information from the current table.
function readTable() {
  var table = document.getElementById("scoretable");
  var currentRound = "";
  var qnumber = 1;
  var output = {};
  for (i=1; i<table.rows.length; i++) {
    row = table.rows[i];


    if (row.innerHTML.includes("Round")) {
      currentRound = row.cells[0].innerHTML;
      output[currentRound] = {};
    } else {
      var q = {};
      for (j=1; j<row.cells.length; j++) {
        cell = row.cells[j];
        team = cell.firstChild.id.split("_")[0];
        q[team] = cell.firstChild.value;
      }
      output[currentRound][qnumber] = q;
      qnumber++;
    }
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
  var validScores = ["0", "1", "4", "5"];
  var valid = true;

  for (const [round, questions] of Object.entries(data)) {
    for (const [qnumber, answers] of Object.entries(questions)) {
      for (i=1; i<=Object.keys(answers).length; i++) {
        var team = document.getElementById("team_" + i).innerHTML;
        var box = document.getElementById(decodeHTML(team) + "_" + qnumber);
        if (box.value == "") {
          box.style = "background-color: inherit;";
        } else if (!validScores.includes(box.value)) {
          box.style = "background-color: #FF5C5C;";
          toastr.error("Invalid value '" + box.value + "' entered. Value must be one of '" + validScores.join("', '") + "'.");
          box.value = "";
          valid = false;
        } else {
          box.style = "background-color: #4CAF50;";
        }
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
      if (error['status'] == 401) {
        alert("Session has expired. Please log in again.");
        window.location.replace("/login");
      } else {
        alert("Communications failure!");
      }
    });
}


function setStatus(unscored) {
  var data = readTable();

  for (const [round, questions] of Object.entries(data)) {
    for (const [qnumber, answers] of Object.entries(questions)) {
      for (i=1; i<=Object.keys(answers).length; i++) {
        var question = document.getElementById(qnumber);
        if (unscored.includes(qnumber)) {
          question.innerHTML = "⚠️";
        } else {
          question.innerHTML = "✅";
        }
      }
    }
  }
}


function updateStatus() {
  var endpoint = "/api/update-judge";
  var button = document.getElementById("helpButton");

  result = communicate(endpoint, {}, method="GET")
    .then(function (result) {
      result = JSON.parse(result);
      setStatus(result['allUnscored']);
      if (result['helpFlag']) {
        if (button.innerHTML == "Help Me!") {
          button.innerHTML = "Help is coming!<br>(click to cancel)";
          button.style.animationPlayState = "running";
        }
      } else {
        if (button.innerHTML != "Help Me!") {
          button.innerHTML = "Help Me!";
          button.style.animationPlayState = "paused";
          button.style.animationName = "none";
          setTimeout(function() {button.style.animationName = "helpcolors";}, 100);
        }
      }
    })
    .catch(function (error) {
      console.warn("Communication failure:", error);
    });
}


function heartbeat() {
  var endpoint = "/api/heartbeat";

  result = communicate(endpoint, {}, method="POST")
    .then(function (result) {

    })
    .catch(function (error) {
      if (error['status'] == 401) {
        alert("Session has expired. Please log in again.");
        window.location.replace("/login");
      } else {
        alert("Communications failure!");
      }
    });
}


// HELP ME
function tasukete() {
  var button = document.getElementById("helpButton");
  if (button.innerHTML == "Help Me!") {
    sendForHelp(true);
  } else {
    sendForHelp(false);
  }
}


// Called to send for help
function sendForHelp(flag) {
  var endpoint = "/api/help-request";
  var data = {'helpFlag': flag};

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
      if (error['status'] == 401) {
        alert("Session has expired. Please log in again.");
        window.location.replace("/login");
      } else {
        alert("Communications failure!");
      }
    });
}


// Compute translation given table, the cell coordinates,
// and the delta coordinates which determine the translation.
// Values passed should be in terms of quadrant IV.
function translate(table, coord, delta) {
  var newCoord = [coord[0] + delta[0], coord[1] + delta[1]];

  var row = table.rows[newCoord[0]];
  if (row == null || newCoord[0] < 2) {
    newCoord[0] = coord[0];
  } else if (row.firstElementChild.colSpan != 1) {
    if (delta[0] > 0) {
      newCoord[0] = newCoord[0] + 1;
    } else if (delta[0] < 0) {
      newCoord[0] = newCoord[0] - 1;
    }
  }

  var cell = table.rows[newCoord[0]].cells[newCoord[1]];
  if (cell == null || newCoord[1] < 1) {
    newCoord[1] = coord[1];
  }

  return newCoord;
}


// Handle keypress event
function handleKeyPress(event) {
  // Current cell coordinate
  var cidx = event.srcElement.parentNode.cellIndex;
  // Current row coordinate
  var ridx = event.srcElement.parentNode.parentNode.rowIndex;

  var table = document.getElementById("scoretable");
  const validKeys = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter"];

  // Cancel all further actions if the key is not a valid key.
  if (!validKeys.includes(event.key)) {
    return;
  }

  // Use translate() to compute new coordinates given key input.
  if (event.key == "ArrowDown") {
    coords = translate(table, [ridx, cidx], [1, 0]);
  }
  if (event.key == "ArrowUp") {
    coords = translate(table, [ridx, cidx], [-1, 0]);
  }
  if (event.key == "ArrowRight") {
    coords = translate(table, [ridx, cidx], [0, 1]);
  }
  if (event.key == "ArrowLeft") {
    coords = translate(table, [ridx, cidx], [0, -1]);
  }
  if (event.key == "Enter") {
    coords = translate(table, [ridx, cidx], [0, 1]);
    if (coords[0] == ridx && coords[1] == cidx) {
      coords = translate(table, [ridx, 1], [1, 0]);
      if (coords[0] == ridx) {
        coords = [ridx, cidx];
      }
    }
  }

  // Focus the <input> element in the box at the computed coordinate pair.
  var box = table.rows[coords[0]].cells[coords[1]];
  box.firstElementChild.focus();
}


// Perform on page load
document.addEventListener('DOMContentLoaded', function(event) {
  validateScore();
});

document.addEventListener('keydown', handleKeyPress);

window.setInterval(function () {
  updateStatus();
  heartbeat();
}, 500);
