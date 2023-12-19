// modal
var modal = document.getElementById("modal");

// When the user clicks on the button, open the modal
window.onload = function(){
  document.getElementById("discard_btn").onclick = function() {
    modal.style.display = "block";
  }
  // When the user clicks on <span> (x), close the modal
  document.getElementsByClassName("close")[0].onclick = function() {
    modal.style.display = "none";
  }
  document.getElementById("back").onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
}
// end of modal
