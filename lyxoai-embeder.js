fetch('http://127.0.0.1:5000/chatbox/chatbox.html')
  .then(response => response.text())
  .then(htmlContent => {
    const div =document.createElement('div')
    div.id = "AiChatBot"
    div.innerHTML = htmlContent;
    const css = document.createElement('link')
    css.rel = 'stylesheet';
    css.type = 'text/css';
    css.href = 'http://127.0.0.1:5000/chatbox/chatbox.css'
    const js =document.createElement('script')
    js.src = 'http://127.0.0.1:5000/chatbox/chatbox.js'
    document.head.appendChild(css)
    document.body.appendChild(div);
    document.body.appendChild(js)
  })
  .catch(error => {
    console.error('Error fetching and injecting HTML:', error);
  });


