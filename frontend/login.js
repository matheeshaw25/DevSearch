let form = document.getElementById('login-form') // get login form

//Add event listener

form.addEventListener('submit', (e) => {//when form is submitted
    e.preventDefault()

    let formData = {
        'username': form.username.value, // get username
        'password': form.password.value, // get password
    }
    fetch('http://127.0.0.1:8000/api/users/token/',{ //pass the formData to this URL
        method:'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify(formData) // pass that data into the body
    })
    .then(response => response.json()) // then we want the response
    .then( data => {
        console.log('DATA:', data.access)
        if(data.access){ // if there is an access token
            localStorage.setItem('token',data.access) //set the token to the local storage
            window.location = 'file:///C:/Users/SEMANTEC/Desktop/frontend/project-list.html'
        }else{
            alert('Username or Password did not work')
        }
    })
}) 