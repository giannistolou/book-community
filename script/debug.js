document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const newElement = "<div style='position:fixed; bottom:0;right:0;background-color:red;color:white;padding:1rem'>DEV MODE</div>";
    body.insertAdjacentHTML('beforeend', newElement);
});