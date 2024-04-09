const tabs = document.querySelectorAll(".nav .nav-item");
function Home_page(){
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
                caption_btn.addEventListener("click", ()=>{
                    document.querySelector(".post-area").style.display = "block";
                })
                back.addEventListener("click", ()=>{
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
                        fetch("/get_all_comments?post_id=" + comment_btn.id, {
                            method: "GET"
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (data.status === 200) {
                                    const comment_display = document.getElementById("comment-display");
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
                        document.getElementById("comment-display").innerHTML += ``;
                    })
                })
            })
            .catch(error => console.error("Error: ", error));
}

Home_page();
// tab for switching pages
tabs.forEach(tab => {
    tab.addEventListener("click", (e) => {
        if( tab.id === "home" ){
            Home_page();
        }else{
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