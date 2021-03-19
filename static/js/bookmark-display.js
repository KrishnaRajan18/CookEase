function DisplayResult(results) {
  // returns list of img urls
  var recipeImages = results["images"];
  console.log(recipeImages);

  // empty the area
  $(".carousel-inner").html("");

  // get first image on carousel
  var firstImage =
    "<div class='item active'> <img class='carousel-image' src='" +
    recipeImages[0] +
    "' </div>";
  $(".carousel-inner").append(firstImage);

  // load rest of images
  for (var i = 1; i < recipeImages.length; i++) {
    var Images =
      "<div class='item'> <img class='carousel-image' src='" +
      recipeImages[i] +
      "' </div>";
    $(".carousel-inner").append(Images);
  } // end loop
} // end fn

$.get("/bookmark-display.json", DisplayResult);
