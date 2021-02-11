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


function updateScores() {
  var endpoint = "/api/total";

  result = communicate(endpoint, "{}", method="GET")
    .then(function (result) {
      result = JSON.parse(result);
      for (const [place, team] of Object.entries(result)) {
        for (const [name, score] of Object.entries(team)) {
          document.getElementById(name + "_total").innerHTML = score;
          document.getElementById(name + "_name").innerHTML = name;
          document.getElementById(name + "_place").innerHTML = place;
        }
      }
    })
    .catch(function (error) {
      console.warn("Communication failure:", error);
    });
}


function sortTable() {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("scoretable");
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("td")[0];
      y = rows[i + 1].getElementsByTagName("td")[0];
      if (parseInt(x.innerHTML) > parseInt(y.innerHTML)) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}


function updateJudges() {
  var endpoint = "/api/update-judge";

  result = communicate(endpoint, {}, method="GET")
    .then(function (result) {
      var judges = JSON.parse(result)['judges'];
      for (const [judge, data] of Object.entries(judges)) {
        document.getElementById(judge + "_last_scored").innerHTML = data['lastScored'];
        if (data['loggedIn']) {
          if (data['helpFlag']) {
            document.getElementById(judge + "_status").innerHTML = "⚠️";
            document.getElementById(judge).classList.add("needsHelp");
            document.getElementById(judge).style.animationPlayState = "running";
          } else {
            document.getElementById(judge + "_status").innerHTML = "✔️";
            document.getElementById(judge).style.animationPlayState = "running";
            document.getElementById(judge).classList.remove("needsHelp");
          }
        } else {
          document.getElementById(judge + "_status").innerHTML = "⭕";
        }
      }
    })
    .catch(function (error) {
      console.warn("Communication failure:", error);
    });
}


window.setInterval(function () {
  updateScores();
  sortTable();
  updateJudges();
}, 500);
