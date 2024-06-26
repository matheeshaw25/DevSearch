let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

let token = localStorage.getItem('token') // saving the token on the local storage and getting it from there


if (token){ //if user has  (a token will be issued)
    loginBtn.remove() // then remove the login button so the logout button will be displayed
}else{
    logoutBtn.remove() //if user has no login then remove the logout button
}

logoutBtn.addEventListener('click', (e) => { // when user presses logout button
    e.preventDefault()
    localStorage.removeItem('token') // remove the token
    window.location = 'file:///C:/Users/SEMANTEC/Desktop/frontend/login.html'

})


let projectsUrl = 'http://127.0.0.1:8000/api/projects/'

// #1 function
// create a function to get project
let getProjects = () => {

    fetch(projectsUrl)
    .then(response => response.json()) // convert response to json data
    .then(data => {
        console.log(data)
        buildProjects(data)
    })

}

// #2 function
// display projects in the template
let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById('projects--wrapper')
    projectsWrapper.innerHTML = '' //setting into an empty string


    for (let i = 0; projects.length > i; i++){ //looping through all projects
        let project = projects[i] // getting project object

        // creating html element
        let projectCard = ` 
                <div class = "project--card">
                    <img src="http://127.0.0.1:8000${project.featured_image}" />
                    <div>
                        <div class="card--header">
                            <h3>${project.title}</h3>
                            <strong class="vote--option" data-vote="up" data-project="${project.id}" >&#43;</strong> 
                            <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
                        </div>
                        <i>${project.vote_ratio}% Positive feedback</i>
                        <p>${project.description.substring(0,150)}</p>
                    </div>
                </div> 
        `
        // going into the innerHTML of projectsWrapper and appending projectCard
        projectsWrapper.innerHTML += projectCard

    }
    addVoteEvents()

    // Add on event listener

}
// Add event listeners to every single vote button
let addVoteEvents = () => {
    let voteBtns = document.getElementsByClassName('vote--option') //getting elements (the vote option)
    
    for (let i=0; voteBtns.length > i ; i++){
        voteBtns[i].addEventListener('click', (e) => { // acess  acess each element and add a event listener , works with a click event
            let token = localStorage.getItem('token') // saving the token on the local storage and getting it from there
            console.log('TOKEN',token)

            let vote = e.target.dataset.vote // up or down vote
            let project = e.target.dataset.project // the specific project

            fetch(`http://127.0.0.1:8000/api/projects/${project}/vote/`,{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization': `Bearer ${token}` // passing the authorization token here
                },
                body:JSON.stringify({'value':vote})
                    
                
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:',data)
                    getProjects()
                })
        })
    }
}

getProjects()