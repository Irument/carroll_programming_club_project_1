function addImage(ctx, x, y, link) {
    // Was having some weird bugs with trying to use this API in Python

    if (document.getElementById(link) == null) {
        img = document.createElement("img")
        img.setAttribute("src", link);
        img.setAttribute("id", link);
        img.onload = function() {
            ctx.drawImage(img, x, y);
        }
        document.getElementById("canvasImages").appendChild(img);
    } else {
        img = document.getElementById(link);
        ctx.drawImage(img, x, y);
    }
}
