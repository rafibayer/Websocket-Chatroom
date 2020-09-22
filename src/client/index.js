
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
            message_recieved(outgoing, true);
        }
    };

};

function message_recieved(message, mine) {
    chatwindow.appendChild(get_message(message, mine));
}

// Returns true if a scrollable element is at the bottom
function scrollableBottomed(scrollable) {
    if (scrollable.scrollTop >= (scrollable.scrollHeight - scrollable.offsetHeight)) {
        return true;
    }
}

// Gets new message element for a given message
function get_message(message, mine) {
    let new_message_element = document.createElement("div");
    new_message_element.classList.add("message");
    if (mine) {
        new_message_element.classList.add("mine");
    }
    new_message_element.innerText = message;
    return new_message_element;
}

// Helper to return element by id
function $(id){
    return document.getElementById(id);
}