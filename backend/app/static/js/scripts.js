document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('login-form');
  const username = document.getElementById('username');
  const password = document.getElementById('password');

  if (form && username && password) {
      form.addEventListener('keydown', function (event) {
          if (event.key === 'Enter') {
              if (document.activeElement === username) {
                  password.focus();
                  event.preventDefault();
              } else if (document.activeElement === password) {
                  if (password.value.trim() !== '') {
                      form.submit();
                  }
                  event.preventDefault();
              }
          }
      });
  }
});



/* ---------------------------------------------- */ 



function uploadImage() {
    let fileInput = document.getElementById('fileInput');
    let file = fileInput.files[0];

    if(!file){
        alert("CropLeaf : Please Select An Image First.");
        return;
    }

    let formData = new FormData();
    formData.append("image", file);

    fetch("{% url 'upload' %}", {  
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error("Error:", error));
}



/*---------------------------------------------------*/


