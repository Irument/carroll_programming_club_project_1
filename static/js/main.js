function addImage(ctx, x, y, link) {
    // Was having some weird bugs with trying to use this API in Python
    img = document.createElement("img")
    img.setAttribute("src", link);
    img.onload = function() {
        ctx.drawImage(img, x, y);
    }
}
