setTimeout(function () {
   (function () {
      const iframe = document.createElement("iframe");
      const div = document.createElement("div");
      div.id = "lyxoaichatbotembed";
      div.style =
         "border: 0px; background-color: transparent; pointer-events: none; z-index: 2147483639; position: fixed; bottom: 0px; width: 100px; height: 100px; overflow: hidden; opacity: 1; max-width: 100%; right: 0px; max-height: 100%;";
      iframe.src = "http://localhost:5000/widget/{{ id }}";
      iframe.style =
         "pointer-events: all; background: none; border: 0px; float: none; position: absolute; inset: 0px; width: 100%; height: 100%; margin: 0px; padding: 0px; min-height: 0px;";
      document.body.appendChild(div);
      div.appendChild(iframe);

      window.addEventListener('message', function(event) {
         if (event.data === 'chatbotHidden') {
           const div = document.getElementById('lyxoaichatbotembed');
       
           div.style.width = '100px';
           div.style.height = '100px';
         }
         if (event.data === 'chatbotVisible') {
            const div = document.getElementById('lyxoaichatbotembed');
        
            div.style.width = '500px';
            div.style.height = '700px';
          }
       });

   })();
}, 2000);
