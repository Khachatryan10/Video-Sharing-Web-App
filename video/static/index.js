document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll("#videoSmall").forEach(video => {
        document.querySelectorAll("#video_anchor").forEach(a => {

            if (a.dataset.id1 === video.dataset.id2){
                video.addEventListener("mouseover", () => {
                    video.play()
                })

                video.addEventListener("mouseout", () => {
                    video.pause()
                })
            }
        })
    })
    
    document.querySelectorAll("#commentInput").forEach(input => {
        document.querySelectorAll("#addComment").forEach(button => {
            document.querySelectorAll("#comments").forEach(comment => {

            if (input.dataset.id3 === button.dataset.id4 && button.dataset.id4 === comment.dataset.id5){
                fetch(`/getComments/${comment.dataset.id5}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(elem => {
                            li = document.createElement("li")
                            li.setAttribute("id", "comment-li")

                            let hr = document.createElement("hr")
                            let prg = document.createElement("p")

                            prg.setAttribute("id", "comment-prg")

                            let dataTimePrg = document.createElement("p")
                            dataTimePrg.setAttribute("id", "dataTimePrg")

                            prg.setAttribute("id", "commentContent")
                            dataTimePrg.innerHTML = elem.date_and_time.slice(0,16).split("T").join(" at ").split("Z").join("").split("-").join("/")

                            li.innerHTML = `${elem.commenter}:`
                            prg.innerHTML = elem.comment
                            document.querySelector("#comments_ul").append(li, prg, dataTimePrg, hr)
                        })
                    })
                }
            })
        })
    })


    document.querySelectorAll("#commentInput").forEach(input => {
        document.querySelectorAll("#addComment").forEach(button => {
            document.querySelectorAll("#comments").forEach(comment => {

            if (input.dataset.id3 === button.dataset.id4 && button.dataset.id4 === comment.dataset.id5){
                button.addEventListener("click", async function() {

                if(input.value.length > 1){
                    
                await fetch(`/add_comment/${button.dataset.id4}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        comment: input.value
                    })
                })
                input.value = ""
                await fetch(`/getComments/${comment.dataset.id5}`)
                    .then(response => response.json())
                    .then(data => {

                        li = document.createElement("li")
                        li.setAttribute("id", "comment-li")

                        let prg = document.createElement("p")
                        let div = document.createElement("div")
                        let hr = document.createElement("hr")

                        let dataTimePrg = document.createElement("p")
                        dataTimePrg.setAttribute("id", "dataTimePrg")
                        dataTimePrg.innerHTML = data.at(0).date_and_time.slice(0,16).split("T").join(" at ").split("Z").join("").split("-").join("/")

                        prg.setAttribute("id", "commentContent")

                        li.innerHTML = `${data.at(0).commenter}:`
                        prg.innerHTML = data.at(0).comment
                        div.append(li, prg, dataTimePrg, hr)
                        document.querySelector("#comments_ul").insertBefore(div, document.querySelector("#comments_ul").children[0])
                
                    })
                        }
                    })
                } 
            })
        })
    })

        document.querySelectorAll("#likeBtn").forEach(likeBtn => {
            document.querySelectorAll("#unlikeBtn").forEach(unlikeBtn => {
                document.querySelectorAll("#likesCount").forEach(h3 => {


            if (likeBtn.dataset.id6 === unlikeBtn.dataset.id7 && unlikeBtn.dataset.id7 === h3.dataset.id8){

                let currentUsername = document.querySelector("#prgUsername").innerText

                fetch(`/getVideoLike/${likeBtn.dataset.id6}`)
                        .then(response => response.json())
                        .then(data => {
                            h3.innerHTML = `Likes ${data.length}`
                            data.forEach(obj => {
                                if(obj.liker === currentUsername){
                                    unlikeBtn.style.display = "block"
                                    likeBtn.style.display = "none"
                                }
                            })
                        })
            }
        })
    })
})

    document.querySelectorAll("#likeBtn").forEach(likeBtn => {
        document.querySelectorAll("#unlikeBtn").forEach(unlikeBtn => {
            document.querySelectorAll("#likesCount").forEach(h3 => {

        let currentUsername = document.querySelector("#prgUsername").innerText

            if (likeBtn.dataset.id6 === unlikeBtn.dataset.id7 && unlikeBtn.dataset.id7 === h3.dataset.id8){
                likeBtn.addEventListener("click", async function(){

                await fetch(`/getVideoLike/${likeBtn.dataset.id6}`,{
                        method: 'POST',
                            body: JSON.stringify({
                            liked_video_id: likeBtn.dataset.id6
                    })
                })

                await fetch(`/getVideoLike/${likeBtn.dataset.id6}`)
                        .then(response => response.json())
                        .then(data => {
                            data.forEach(obj => {

                            if(obj.liker === currentUsername){
                                unlikeBtn.style.display = "block"
                                likeBtn.style.display = "none"
                            }
                            else{
                                unlikeBtn.style.display = "none"
                                likeBtn.style.display = "block"
                            }

                    })
                })

                await fetch(`/getVideoLike/${h3.dataset.id8}`)
                    .then(response => response.json())
                    .then(data => { 
                        h3.innerHTML = `Likes ${data.length}`
                    })
            })

            unlikeBtn.addEventListener("click", async function(){
                    await fetch(`/getVideoLike/${unlikeBtn.dataset.id7}`,{
                            method: 'DELETE',
                                body: JSON.stringify({
                                liked_video_id: unlikeBtn.dataset.id7
                    })
                        })

                    await fetch(`/getVideoLike/${unlikeBtn.dataset.id7}`)
                        .then(response => response.json())
                        .then(data => {
                                if(data){
                                data.forEach(obj => {

                                    if(obj.liker !== currentUsername){
                                        unlikeBtn.style.display = "none"
                                        likeBtn.style.display = "block"
                                    }
                                    else {
                                    unlikeBtn.style.display = "none"
                                    likeBtn.style.display = "block"
                                }
                            })

                        }
                                    unlikeBtn.style.display = "none"
                                    likeBtn.style.display = "block"
                    })

                await fetch(`/getVideoLike/${h3.dataset.id8}`)
                    .then(response => response.json())
                    .then(data => { 
                        h3.innerHTML = `Likes ${data.length}`
                    })
            })
            }
        })
    })
})

document.querySelectorAll(".delteVideoBtn").forEach(btn => {
    document.querySelectorAll("#deleteDiv").forEach(delDiv => {
        document.querySelectorAll("#yesDelete").forEach(yesBtn => {
            document.querySelectorAll("#noCancel").forEach(noBtn => {

        if (btn.dataset.id10 === delDiv.dataset.id11 && delDiv.dataset.id11 === yesBtn.dataset.id12 && yesBtn.dataset.id12 === noBtn.dataset.id13){

            btn.addEventListener("click",function() {
            document.querySelector("#deleteDiv").style.display = "block"
            document.querySelector("body").style.backgroundColor = "rgb(97, 97, 97)"

                    noBtn.addEventListener("click", function(){
                        document.querySelector("#deleteDiv").style.display = "none"
                        document.querySelector("body").style.backgroundColor = ""
                    })

                    yesBtn.addEventListener("click", function(){
                        fetch(`/delete_video/${yesBtn.dataset.id12}`,{
                            method: "DELETE"
                        })
                        window.location.href = "/all_videos/1"
                    })
                    })
                }
            })
        })
    })
})
})