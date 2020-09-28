"use strict";
(function(server_url) {
    
    window.onload = function(){
        const socket = new WebSocket(server_url);
        let input = $("input");
        input.focus()
    
        // message recieved
        socket.addEventListener('message', function (event) {
            message_recieved(event.data);
        });
    
        // enter in box
        document.onkeypress = function(e){
            if(e.code == "Enter" && input == document.activeElement) {
                send_message(socket);
            }
        };
    
        // send button
        $("send").addEventListener("click", function(ev) {
            send_message(socket);
        });
    };
    
    function send_message(socket) {
        let outgoing = input.value;
        input.value = "";
        if (outgoing.trim() != "") {
            socket.send(outgoing);
        }
    }
    
    function message_recieved(message) {
        console.log(message);
        let message_json = JSON.parse(message)
        let chatwindow = $("chatwindow");
    
        // scroll if we are at most recent or we sent the message
        let shouldScroll = scrollableBottomed(chatwindow) || mine;
        chatwindow.appendChild(get_message(message_json.body, message_json.origin));
        if (shouldScroll){
            chatwindow.scrollTop = chatwindow.scrollHeight;
        }
    }
    
    // Returns true if a scrollable element is at the bottom
    function scrollableBottomed(scrollable) {
        if (scrollable.scrollTop >= (scrollable.scrollHeight - scrollable.offsetHeight)) {
            return true;
        }
    }
    
    // Gets new message element for a given message
    function get_message(message, origin) {
        let new_message_element = document.createElement("div");
        new_message_element.classList.add("message");
        new_message_element.classList.add(origin);
    
        new_message_element.innerText = message;
        return new_message_element;
    }
    
    // Helper to return element by id
    function $(id){
        return document.getElementById(id);
    }

})(server_url);

