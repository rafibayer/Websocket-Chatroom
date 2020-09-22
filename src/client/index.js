
window.onload = function(){
    const socket = new WebSocket('ws://localhost:5000');
    let chatwindow = $("chatwindow");
    let input = $("input");

    socket.addEventListener('message', function (event) {
        let shouldScroll = scrollableBottomed(chatwindow);
        message_recieved(event.data);
        if (shouldScroll){
            chatwindow.scrollTop = chatwindow.scrollHeight;
        }
    });

    // When a new message is recieved, append to chat window,
    // and scroll down if we are already at the bottom of the window
    document.onkeypress = function(e){
        if(e.code == "Enter" && input == document.activeElement) {
            let outgoing = input.value;
            input.value = "";
            socket.send(outgoing);
        }
    };

};

function message_recieved(message) {
    chatwindow.appendChild(get_message(message));
}

// Returns true if a scrollable element is at the bottom
function scrollableBottomed(scrollable) {
    if (scrollable.scrollTop >= (scrollable.scrollHeight - scrollable.offsetHeight)) {
        return true;
    }
}

// Gets new message element for a given message
function get_message(message) {
    let new_message_element = document.createElement("div");
    new_message_element.className = "message";
    new_message_element.innerText = message;
    return new_message_element;
}

// Helper to return element by id
function $(id){
    return document.getElementById(id);
}