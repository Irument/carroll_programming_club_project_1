function loadImage(ctx, id, link, image_locations) {
    // Was having some weird bugs with trying to use this API in Python
    image_locations = JSON.parse(image_locations)
    img = document.createElement("img")
    img.setAttribute("src", link);
    img.setAttribute("id", id);
    document.getElementById("canvasImages").appendChild(img);
    img.onload = function() {
        imageLoaded = true;
        for (let i = 0; i < image_locations.length; i++) {
            if (image_locations[i].id == id) {
                if (image_locations[i].w == null && image_locations[i].h == null) {
                    ctx.drawImage(img, image_locations[i].x, image_locations[i].y);
                } else {
                    ctx.drawImage(img, image_locations[i].x, image_locations[i].y, image_locations[i].w, image_locations[i].h);
                }
            }
        }
    }
}
