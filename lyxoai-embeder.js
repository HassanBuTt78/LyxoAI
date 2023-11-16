
const iframe = document.createElement("iframe");
const div = document.createElement("div");
div.id = "lyxoaichatbotembed";
div.style = "pointer-events: none; width: 500px; height: 100%; position: fixed; right: 0; bottom: 0; max-width: 100%; max-height: 100%;"
iframe.src = "http://localhost:5000/widget/654f6055ce3d3b2fbc76ccc2";
iframe.style =
   "pointer-events: all; background: none; border: 0px; float: none; position: absolute; inset: 0px; width: 100%; height: 100%; margin: 0px; padding: 0px; min-height: 0px;";
document.body.appendChild(div);
div.appendChild(iframe);
