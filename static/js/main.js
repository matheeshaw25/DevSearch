
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

