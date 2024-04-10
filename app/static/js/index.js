const tabs = document.querySelectorAll(".nav .nav-item");
let postID = 0;
function Home_page() {
    // default open home page starting window.onload
    fetch("/home", {
        method: "GET",
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById("display").innerHTML = data;
            // after getting data and insert it into main container display
            // post upload
            const caption_btn = document.getElementById("caption-btn");
            const back = document.getElementById("back");
            caption_btn.addEventListener("click", () => {
                document.querySelector(".post-area").style.display = "block";
            })
            back.addEventListener("click", () => {
                document.querySelector(".post-area").style.display = "none";
            })
            document.getElementById('uploadForm').addEventListener('submit', function (event) {
                event.preventDefault();
                // disable submit btn for duplicated post by network errors
                document.getElementById("save").disabled = true;
                const post_data = {
                    "caption": document.getElementById("caption").value === "" ? " " : document.getElementById("caption").value
                }
                fetch("/action/post_upload", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(post_data)
                }).then(response => response.json())
                    .then(data => {
                        if (data.status === 200 || data.status === 204) {
                            // after uploading caption check if there is image need to upload or not 
                            if (document.getElementById('image').files[0]) {
                                upload_image(data.post_id);
                            }
                            Home_page();
                        }
                    })
                    .catch(error => {
                        console.error("Error: ", error);
                    });
            });

            function upload_image(post_id) {
                var formData = new FormData();
                formData.append('image_type', "post_image");
                formData.append("post_id", post_id);
                formData.append('image', document.getElementById('image').files[0]);

                fetch('/action/upload_image', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 200) {
                            Home_page();
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
            // add necessary listeners
            const comment_btns = document.querySelectorAll(".comments");
            comment_btns.forEach(comment_btn => {
                comment_btn.addEventListener("click", () => {
                    document.getElementById("comment-section").style.display = "block";
                    // assign post_id for inner comment submition
                    postID = comment_btn.id;
                    // fetching comments
                    showComment(postID);
                    document.getElementById("comment-display").innerHTML += ``;
                })
            })
        })
        .catch(error => console.error("Error: ", error));

}
// add onclick function for each comment submitted from outside of comment-section 
function submitComment(post_id) {
    requestComment(post_id, document.getElementById("comment_text"));
}

function submitCommentInSection() {
    const text = document.getElementById("comment-text-in-section");
    requestComment(postID, text);
}
Home_page();
// tab for switching pages
tabs.forEach(tab => {
    tab.addEventListener("click", (e) => {
        if (tab.id === "home") {
            Home_page();
        } else {
            fetch("/" + tab.id, {
                method: "GET",
            })
                .then(response => response.text())
                .then(data => {
                    document.getElementById("display").innerHTML = data;
                })
                .catch(error => console.error("Error: ", error));
        }
    });
})
function back(container_name){
    document.getElementById(container_name).style.display = "none";
}
// function for comment post request
function requestComment(post_id, text) {
    // const text = document.getElementById("comment_text");
    if (text.value != "") {
        const comment_data = {
            post_id: post_id,
            text: text.value
        }
        text.value = "";
        fetch("/action/comment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(comment_data)
        })
            .then(response => response.json())
            .then(data => {
                if( data.status === 200 ){
                    // update comment list
                    showComment(postID);
                }
            })
            .catch(error => console.error("Error: ", error));
    } else {
        text.focus();
    }
}

//  function for showing comment with related post 
function showComment(post_id) {
    const comment_display = document.getElementById("comment-display");
    comment_display.innerHTML = "";
    fetch("/get_all_comments?post_id=" + post_id, {
        method: "GET"
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 200) {
                data.comments.forEach(comment => {
                    comment_display.innerHTML += `<div class="comment">
                <div class="info">
                    <div class="profile">
                        <img src="${comment.profile_uri}" alt="">
                    </div>
                    <div class="username">${comment.username}</div>
                </div>
                <div class="text">${comment.comment_text}</div>
            </div>`;
                })
            }
        })
        .catch(error => console.error("Error: ", error));
}