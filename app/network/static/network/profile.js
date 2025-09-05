document.addEventListener("DOMContentLoaded", () =>{
    const followBtn = document.querySelector("#follow-btn");
    if (followBtn)
        followBtn.addEventListener("click", () => {
            const username = document.querySelector("#username").textContent;
            const followersDiv = document.querySelector("#followers");
            if (username && followers)
                handleFollow(followBtn, followersDiv, username.substring(1));
        })
})

function handleFollow(followBtn, followersDiv, username) {
    fetch(`/toggle_follow/${username}`)
        .then(response => {
            if (response.status == 401) {
                response.json().then(data => {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                })
            }
            return response.json();
        })
        .then(data => {
            const followersValue = followersDiv.querySelector("p");
            if (followersValue) {
                followersValue.textContent = data.followers;
            }
            
            
            followBtn.classList.toggle("btn-primary");
            followBtn.classList.toggle("btn-secondary");
            
            followBtn.textContent = data.is_following ? "Unfollow":"Follow";
        })
}