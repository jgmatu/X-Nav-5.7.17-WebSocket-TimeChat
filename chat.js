const inputBox = document.getElementById("message");
const output = document.getElementById("output");
const form = document.getElementById("form");
const host = "ws://localhost:8000/";

try {
      var s = new WebSocket(host);

      s.onopen = function (e) {
            setLine("Socket opened.");
      };

      s.onclose = function (e) {
            setLine("Socket closed.");
      };

      s.onmessage = function (e) {
            setLine("Receive : " + e.data);
      };

      s.onerror = function (e) {
            setLine("Socket error " + e);
      };

} catch (ex) {
      setLine("Socked exception");
}

form.addEventListener("submit", function (e) {
      e.preventDefault();

      if (inputBox.value == '') {
            return;
      }
      sendMessage(inputBox.value);
      inputBox.value = "";
}, false);

var sendMessage = function (data) {
      s.send(data);
      setLine("Send : " + data);
}

var setLine = function (line) {
      var p = document.createElement("p");

      p.innerHTML = line;
      output.appendChild(p);
}
