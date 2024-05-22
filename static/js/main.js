
// GET SEARCH FORM AND PAGE LINKS 
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

// ENSURE SEARCH FORM EXISTS

if(searchForm){
for(let i=0;pageLinks.length > i; i++){
    pageLinks[i].addEventListener('click',function (e){ //everytime a button is clicked fire off the event
    e.preventDefault()
        
    // GET DATA ATTRIBUTE
    let page = this.dataset.page
        
    // ADD HIDDEN SEARCH INPUT TO FORM
    searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

    // SUBMIT FORM
    searchForm.submit()
    }) 
}

}



let tags = document.getElementsByClassName('project-tag ') //query all the tags in the page

    for(let i=0; tags.length > i; i++){
        tags[i].addEventListener('click',(e)=>{ //on click
            let tagId = e.target.dataset.tag //get tag ID
            let projectId = e.target.dataset.project // get project ID

            // console.log('TAG ID:', tagId )
            // console.log('PROJECT ID:', projectId)

            fetch('http://127.0.0.1:8000/api/remove-tag/',{
                method: 'DELETE',
                headers:{
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({'project':projectId, 'tag':tagId})
            })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
            })
        })
    }
