function toggleEditComment(commentId, type) {
    const getElement = (element, commentId) => {
        return document.getElementById(`${element}-${commentId}`);
    };

    const commentContent = getElement("comment-content", commentId);
    const editForm = getElement("edit-form", commentId);
    const buttons = getElement("comment-buttons", commentId);

    const action = {
        edit: () => {
            commentContent.classList.toggle("d-none");
            editForm.classList.toggle("d-none");
            buttons.classList.toggle("d-none")
        },

        cancel: () => {
            commentContent.classList.toggle("d-none");
            editForm.classList.toggle("d-none");
            buttons.classList.toggle("d-none")
        }
    };

    return action[type]();
}


function hideMessage(messageId, btnId = "", hideDelay = 4000, removeDelay = 2000) {
    const message = document.getElementById(messageId);
    const btnHideMessage = document.getElementById(btnId);
    
    if (!message) return false;

    const action = () => {
        message.classList.add("is-hidden");
    };

    const hideWithDelay = (delay) => {
        return new Promise((resolve) => setTimeout(resolve, delay));
    };

    btnHideMessage.addEventListener("click", () => {
        action();
        message.removeEventListener("click", this);
    });

    const hideMessageWithDelay = async () => {
        await hideWithDelay(hideDelay);
        action();
        await hideWithDelay(removeDelay);
        message.classList.add("d-none");
    };

    hideMessageWithDelay();
    return true;
}

hideMessage("message-alert", "btn-hide-message");