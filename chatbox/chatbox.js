(function () {
   const toggleButton = document.getElementById("chatbox_toggle");
   const sendButton = document.getElementById("send_btn");
   const chatField = document.getElementById("chat_msg");
   const chatBoxBody = document.getElementById("chatbox_body");
   const chatBox = document.getElementById("chatbox");
   const typeLoading = document.getElementById("typing");
   let chat_id;
   if (getCookie("chatSessionId")) {
      chat_id = getCookie("chatSessionId");
   } else {
      chat_id = "";
   }

   let inTrasition = false;
   let isTyping = false;
   const toggleChatBox = () => {
      if (inTrasition) return;
      inTrasition = true;
      const toggleClose = document.querySelectorAll(".toggle_close")[0];
      const toggleOpen = document.querySelectorAll(".toggle_open")[0];

      if (toggleOpen.style.display === "block") {
         toggleButton.style.animation = "rotateOut 0.5s ease-in-out forwards";
         chatBox.style.animation = "slideUp 0.5s ease-in-out forwards";
         setTimeout(() => {
            toggleOpen.style.display = "none";
            toggleClose.style.display = "block";
         }, 250);
         chatBox.style.display = "block";
         setTimeout(() => {
            inTrasition = false;
         }, 500);
      } else {
         toggleButton.style.animation = "rotateIn 0.5s ease-in-out forwards";
         setTimeout(() => {
            toggleOpen.style.display = "block";
            toggleClose.style.display = "none";
         }, 250);
         chatBox.style.animation = "slideDown 0.5s ease-in-out forwards";
         setTimeout(() => {
            chatBox.style.display = "none";
            inTrasition = false;
         }, 500);
      }
   };

   const sendMessage = async () => {
      if (chatField.value.trim().length < 1) return;
      if (isTyping) return;
      isTyping = true;
      const message = chatField.value;
      chatField.value = "";
      renderSentMessage(message);
      setTimeout(toggleTyping, 300);
      reply = await getReply(message);
      toggleTyping();
      setTimeout(()=>{
         renderReply(reply)
         isTyping = false
      }, 300);
   };

   const getReply = async (message) => {
      try {
         let body;
         if (chat_id == "" || chat_id == undefined || chat_id == null) {
            requestBody = { message };
         } else {
            requestBody = { message: message, chatSessionId: chat_id };
         }

         const response = await fetch("http://localhost:5000/chat", {
            method: "POST",
            headers: {
               "Content-Type": "application/json", // Set the appropriate content type
               authorization:
                  "bearer e571614c8c35e979ddabd1b8e358d4a34786705026d2ac91b2e8cf131ff5bb31",
            },
            body: JSON.stringify(requestBody), // Send your message as JSON data
         });

         if (!response.ok) {
            throw new Error(
               `Server returned ${response.status} ${response.statusText}`
            );
         }

         const replyJson = await response.json();
         chat_id = replyJson.chatSessionId;
         setCookie("chatSessionId", chat_id, 30);
         return replyJson.reply;
      } catch (error) {
         isTyping = false
         console.error("Error fetching the reply:", error);
         return "An error occurred"; // Handle the error as needed
      }
   };

   const toggleTyping = () => {
      const typeLoading = document.getElementById("typing");
      if (!typeLoading) {
         chatBoxBody.innerHTML += `         <div class="assistant chat" id="typing">
      <div class="message">
         <div class="typing">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
         </div>             
      </div>
   </div>`;
         chatBoxBody.scrollTop = chatBoxBody.scrollHeight;
      } else {
         typeLoading.remove();
      }
   };
   const renderSentMessage = (message) => {
      if (chatBoxBody) {
         const htmlToAppend = `
          <div class="user chat">
            <p class="sender_name">You</p>
            <p class="message">
              ${message}
            </p>
          </div>
        `;

         chatBoxBody.innerHTML += htmlToAppend;
         chatBoxBody.scrollTop = chatBoxBody.scrollHeight;
      }
   };

   const renderReply = (reply) => {
      if (chatBoxBody) {
         const htmlToAppend = `
          <div class="assistant chat">
            <p class="sender_name">Ai Assistant</p>
            <p class="message">
              ${reply}
            </p>
          </div>
        `;

         chatBoxBody.innerHTML += htmlToAppend;
         chatBoxBody.scrollTop = chatBoxBody.scrollHeight;
      }
   };

   function setCookie(name, value, minutes) {
      const expires = new Date();
      expires.setTime(expires.getTime() + minutes * 60 * 1000);
      document.cookie =
         name +
         "=" +
         value +
         ";expires=" +
         expires.toUTCString() +
         ";path=/" +
         ";samesite=none;secure";
   }

   function getCookie(name) {
      const cookieName = name + "=";
      const decodedCookie = decodeURIComponent(document.cookie);
      const cookieArray = decodedCookie.split(";");

      for (let i = 0; i < cookieArray.length; i++) {
         let cookie = cookieArray[i].trim();
         if (cookie.indexOf(cookieName) === 0) {
            return cookie.substring(cookieName.length, cookie.length);
         }
      }

      return null;
   }

   toggleButton.addEventListener("click", toggleChatBox);
   sendButton.addEventListener("click", sendMessage);
})();
