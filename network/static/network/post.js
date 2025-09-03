document.addEventListener("DOMContentLoaded", () => {
    // Delegate events for like buttons
    document.body.addEventListener("click", (event) => {
        if (event.target.classList.contains("like-btn")) {
            const likeButton = event.target;
            const postID = likeButton.dataset.id;
            if (postID) {
                toggleLike(postID, likeButton);
            }
        }
    });

    // Delegate events for edit buttons
    document.body.addEventListener("click", (event) => {
        if (event.target.classList.contains("edit-btn")) {
            const editButton = event.target;
            const card = editButton.closest(".card");
            const postID = editButton.dataset.id;
            if (postID) {
                editPost(card, postID);
            }
        }
    });
});

const headers = {
    "Content-Type": "application/json"
};

function toggleLike(postId, likeButton) {
    fetch(`/toggle_like/${postId}`, { method: "POST", headers })
        .then(response => {
            if (response.status === 401) {
                response.json().then(data => {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                });
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data.likes !== undefined) {
                likeButton.innerHTML = `<i class="bi bi-heart-fill"></i> (${data.likes})`;
                likeButton.classList.toggle("btn-danger");
                likeButton.classList.toggle("btn-outline-danger");
            } else {
                throw new Error("Failed to update likes");
            }
        })
        .catch(error => {
            display_error("#error-posts", error);
        });
}

function editPost(postElement, postID) {
    const postElementCopy = postElement.cloneNode(true);
    const postContent = postElement.querySelector(".post-content");
    const postFooter = postElement.querySelector(".post-footer");

    // Replace content with a textarea
    const textarea = document.createElement("textarea");
    textarea.className = "form-control";
    textarea.value = postContent.textContent;

    // Replace footer with Save and Cancel buttons
    const saveButton = document.createElement("button");
    saveButton.className = "btn btn-sm btn-success me-2";
    saveButton.innerText = "Save";

    const cancelButton = document.createElement("button");
    cancelButton.className = "btn btn-sm btn-secondary";
    cancelButton.innerText = "Cancel";

    saveButton.addEventListener("click", () => savePost(postID, textarea.value, postElement, postElementCopy));
    cancelButton.addEventListener("click", () => resetPostView(postElement, postElementCopy));

    postContent.replaceWith(textarea);
    postFooter.innerHTML = "";
    postFooter.appendChild(saveButton);
    postFooter.appendChild(cancelButton);
}

function savePost(postId, content, postElement, postElementCopy) {
    fetch(`/edit_post/${postId}`, {
        method: "PUT",
        headers,
        body: JSON.stringify({ content }),
    })
        .then(response => {
            if (response.status === 401) {
                response.json().then(data => {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                });
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data.message) {
                // Update post content and reset view
                const postContent = postElementCopy.querySelector(".post-content");
                postContent.innerText = content; // Use updated content
                resetPostView(postElement, postElementCopy);
            } else {
                throw new Error("Failed to save post");
            }
        })
        .catch(error => {
            console.error("Error saving post:", error);
        });
}

function resetPostView(postElement, copy) {
    // Reset post content and footer to original view
    postElement.replaceWith(copy);
}
